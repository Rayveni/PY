from requests import Session
from pandas import DataFrame
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from datetime import datetime
from pandas import DataFrame

class my_jira:
    def __init__(self,server:str,auth:tuple,api_version:str=r'/rest/api/2/'):
        self.api_version=api_version
        self.server=server
        self.endpoints={'project':r'project',
                       'search_worklog':'search?jql=worklogAuthor%20in%20({author_list})%20and%20worklogDate%20>={start_date}%20and%20worklogDate%20<{end_date}',
                       'user_info':'user/search?username={user_id}'}
        self.__session(auth)

    def __session(self,auth:tuple):
        self.session=Session()
        self.session.headers.update({"content-type": "application/json"})
        self.session.auth=auth
        
    def __url(self,endpoint:str):
        return r"{server}{api}{endpoint}".format(server=self.server,api=self.api_version,endpoint=endpoint)
    
    def __get_json(self,_url:str):  
        r=self.session.get(_url)
        return r.json()
    
    def projects(self):
        url=self.__url(self.endpoints['project'])
        return self.__get_json(url)

    def get_worklog(self,author_list:list,start_date:str,end_date:str):

        url=self.__url(self.endpoints['search_worklog']).format(author_list=author_list,
                                                                start_date=start_date,
                                                                end_date=end_date)       
        return self.__get_json(url)

    def user_info(self,user_id:str):
        url=self.__url(self.endpoints['user_info'].format(user_id=user_id))
        _json=self.__get_json(url)
        return {k:v for k,v in _json[0].items() if k in ['key','displayName','emailAddress','active']}


class my_jira_reports(my_jira):
    
    def get_bulk_issues(self,issue_list:list,n_threads:int=8):
        worker=lambda _url:(_url[1],self.session.get(_url[0]).json())
        res=[]
        for i in range(0, len(issue_list), n_threads):
            pool = ThreadPool(n_threads)
            results=pool.map(worker,issue_list[i:i + n_threads])
            pool.close()
            pool.join()
            res.extend(results)
            sleep(1)
        return res  
    
    def show_team(self,team_list:list):
        _team=[self.user_info(el) for el in team_list]
        return DataFrame(_team)
    
    def extract_issue_info(self,issue):
        _d={'key':issue['key']}
        _d['assignee']=issue['fields']['assignee']['displayName']
        _d['resolution']=issue['fields']['resolution']['name']
        _d['priority']=issue['fields']['priority']['name']
        _d['status']=issue['fields']['status']['name']    
        _d['creator']=issue['fields']['creator']['name']   
        _d['reporter']=issue['fields']['reporter']['name'] 
        _d['summary']= issue['fields']['summary']
        _d['duedate']= issue['fields']['duedate']    
        return _d    
    
    def worklog_rep(self,team_list:list,start_date:str,end_date:str='2099-01-01'):
        _worklog=self.get_worklog(','.join(team_list),start_date,end_date)
        assert  _worklog['total'] <= _worklog['maxResults']
        _worklog={(el['self']+r"/worklog"):(el['key'],el['fields']['summary']) for el in _worklog['issues']}
        worklog_by_issue,ravel_worklog=self.get_bulk_issues(list(_worklog.items())),[]
        for _row in worklog_by_issue:
            _temp=_row[1]['worklogs']
            _issue_key,summary=_row[0]
            assert  _row[1]['maxResults'] >= _row[1]['total']
            ravel_worklog.extend([ [_issue_key,
                                    summary,
                                   _el['updateAuthor']['name'],
                                    datetime.strptime(_el['started'][:10],'%Y-%m-%d'),
                                    _el['timeSpentSeconds']/3600,
                                    _el['comment']
                                   ] for _el in _temp if _el['updateAuthor']['name'] in team_list]) 
        
        columns=['key','summary','author','log_date','hours','comment']
        
        return DataFrame(ravel_worklog,columns=columns)