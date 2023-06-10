from requests import Session
from pandas import DataFrame
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from datetime import datetime
from pandas import DataFrame
from json import dumps


class my_jira:
    def __init__(self, server: str,
                 auth_type: str,  # token, login_password"
                 auth_data,
                 api_version: str = r'/rest/api/2/',
                 agile_api_version: str = r'/rest/agile/1.0/',
                 verify_cert: bool = True
                 ):
        self.api_version, self.agile_api_version = api_version, agile_api_version
        self.server = server
        self.verify_cert = verify_cert
        self.endpoints = {'project': r'project',
                          'and_operator': '%20and%20',
                          'search_worklog': {'base': 'search?jql=',
                                             'author_list': 'worklogAuthor%20in%20({author_list})',
                                             'start_date': 'worklogDate%20>={start_date}',
                                             'end_date': 'worklogDate%20<{end_date}'
                                             },
                          'user_info': 'user/search?username={user_id}',
                          'issue': 'issue/{issue_key}',
                          'transition_issue': 'issue/{issue_key}/transitions',
                          'sprint_issue': 'sprint/{sprint_id}/issue',
                          'epic_issue': 'epic/{epic_id}/issue',
                          'find_issues': {'author_list': 'worklogAuthor%20in%20({})',
                                          'worklog_start_date': 'worklogDate%20>={}',
                                          'worklog_end_date': 'worklogDate%20<{}',
                                          'project_list': 'project%20in%20({})',
                                          'custom': '{}'
                                          }

                          }
        self.__session(auth_type, auth_data)

    def __session(self, auth_type: str, auth_data):
        self.session = Session()
        headers = {"content-type": "application/json"}
        if auth_type == 'login_password':
            self.session.headers.update(headers)
            self.session.auth = tuple(auth)
        else:
            headers.update(
                {'Authorization': 'Bearer {token}'.format(token=auth_data)})
            self.session.headers.update(headers)

    def _url(self, endpoint: str, api_version: str = None):
        if api_version is None:
            api_version = self.api_version
        return r"{server}{api}{endpoint}".format(server=self.server, api=api_version, endpoint=endpoint)

    def _get_json(self, _url: str,payload:dict=None):
        r = self.session.get(_url, verify=self.verify_cert,params=payload)
        return r.json()

    def issue_raw_info(self, issue_key: str,expand:str=None):
        url = self._url(self.endpoints['issue'].format(issue_key=issue_key))
        return self._get_json(url,payload={'expand':expand})

    def projects(self):
        url = self._url(self.endpoints['project'])
        return self._get_json(url)

    def find_issues(self, max_results: int = 1000, **kwargs):
        """Summary or Description of the Function:
        optional args:

        author_list:list
        worklog_start_date:str
        worklog_end_date:str
        project_list:list
        custom:str
        """
        def list_to_str(l): return ','.join(l) if isinstance(l, list) else l
        and_operator = self.endpoints['and_operator']
        jql_parts = [self.endpoints['find_issues'][key].format(
            list_to_str(kwargs[key])) for key in kwargs.keys()]
        endpoint_url = 'search?jql={body}&maxResults={max_results}'.format(
            body=and_operator.join(jql_parts), max_results=max_results)
        url = self._url(endpoint_url)
        # print(url)
        r = self._get_json(url)
        page_start, pag_size, page_total = r['startAt'], r['maxResults'], r['total']
        issues = r['issues']
        for start in list(range(page_start, page_total, pag_size))[1:]:
            page_url = f"{url}&startAt={start}"
            issues += self._get_json(page_url)['issues']
        return issues

    def get_worklog(self, **kwargs):
        """Summary or Description of the Function:
        optional args:

        author_list:list
        start_date:str
        end_date:str
        """
        url = self._url(self.__endpoint_builder(
            self.endpoints['search_worklog'], kwargs))
        return self._get_json(url)

    def user_info(self, user_id: str):
        url = self._url(self.endpoints['user_info'].format(user_id=user_id))
        _json = self._get_json(url)
        return {k: v for k, v in _json[0].items() if k in ['key', 'name', 'displayName', 'emailAddress', 'active']}

    def get_task_transitions(self, issue_key: str):
        url = self._url(
            self.endpoints['transition_issue'].format(issue_key=issue_key))
        return self._get_json(url)

    def transition_issue(self, issue_key: str, transition_id: int, resolution: str = None):
        url = self._url(
            self.endpoints['transition_issue'].format(issue_key=issue_key))
        data = {"transition": {"id": transition_id}}
        if resolution is not None:
            data['fields'] = {'resolution': {'name': resolution}}

        return self.session.post(url, data=dumps(data), verify=self.verify_cert).ok

    def create_issue(self, project: str, issue_type: str, task_summary: str, task_description: str, additional_keys: dict):
        url = self._url(self.endpoints['issue'].format(issue_key=''))
        base_dict = {'project': {'key': project},
                     'summary': task_summary,
                     'description': task_description,
                     'issuetype': {'name': issue_type}
                     }
        issue_data = {'fields': {**base_dict, **additional_keys}
                      }
        # print(issue_data)
        return self.session.post(url, data=dumps(issue_data), verify=self.verify_cert)

    def update_issue(self, issue_key: str, update_fields: dict):
        url = self._url(self.endpoints['issue'].format(issue_key=issue_key))

        issue_data = {'fields': {**update_fields}
                      }
        return self.session.put(url, data=dumps(issue_data), verify=self.verify_cert)

    def issue_to_sprint(self, sprint_id: int, issue_keys: list):
        url = self._url(self.endpoints['sprint_issue'].format(
            sprint_id=sprint_id), api_version=self.agile_api_version)
        issue_data = {'issues': issue_keys}
        return self.session.post(url, data=dumps(issue_data), verify=self.verify_cert)

    def issue_to_epic(self, epic_id: int, issue_keys: list):
        url = self._url(self.endpoints['epic_issue'].format(
            epic_id=epic_id), api_version=self.agile_api_version)
        issue_data = {'issues': issue_keys}
        return self.session.post(url, data=dumps(issue_data), verify=self.verify_cert)

    def get_issue(self, issue_key: str):
        url = self._url(self.endpoints['issue'].format(issue_key=issue_key))
        return self._get_json(url)


class my_jira_reports(my_jira):

    def get_bulk_issues(self, issue_list: list, n_threads: int = 8):
        def worker(_url): return (_url[1], self.session.get(_url[0]).json())
        res = []
        for i in range(0, len(issue_list), n_threads):
            pool = ThreadPool(n_threads)
            results = pool.map(worker, issue_list[i:i + n_threads])
            pool.close()
            pool.join()
            res.extend(results)
            sleep(1)
        return res

    def show_team(self, team_list: list):
        _team = [self.user_info(el) for el in team_list]
        return DataFrame(_team)

    def extract_issue_info(self, issue):
        _d = {'key': issue['key']}
        _d['assignee'] = issue['fields']['assignee']['displayName']
        _d['resolution'] = issue['fields']['resolution']['name']
        _d['priority'] = issue['fields']['priority']['name']
        _d['status'] = issue['fields']['status']['name']
        _d['creator'] = issue['fields']['creator']['name']
        _d['reporter'] = issue['fields']['reporter']['name']
        _d['summary'] = issue['fields']['summary']
        _d['duedate'] = issue['fields']['duedate']
        return _d

    def worklog_rep(self, team_list: list, start_date: str, end_date: str = '2099-01-01'):
        _worklog = self.get_worklog(','.join(team_list), start_date, end_date)
        assert _worklog['total'] <= _worklog['maxResults']
        _worklog = {(el['self']+r"/worklog"): (el['key'],
                                               el['fields']['summary']) for el in _worklog['issues']}
        worklog_by_issue, ravel_worklog = self.get_bulk_issues(
            list(_worklog.items())), []
        for _row in worklog_by_issue:
            _temp = _row[1]['worklogs']
            _issue_key, summary = _row[0]
            assert _row[1]['maxResults'] >= _row[1]['total']
            ravel_worklog.extend([[_issue_key,
                                   summary,
                                   _el['updateAuthor']['name'],
                                   datetime.strptime(
                                       _el['started'][:10], '%Y-%m-%d'),
                                   _el['timeSpentSeconds']/3600,
                                   _el['comment']
                                   ] for _el in _temp if _el['updateAuthor']['name'] in team_list])

        columns = ['key', 'summary', 'author', 'log_date', 'hours', 'comment']

        return DataFrame(ravel_worklog, columns=columns)

    def sec_to_day_weeks(self, sec: int) -> str:
        days = sec/3600/8
        weeks = days//5
        rest_days = days % 5
        if weeks == 0:
            res = ''
        else:
            res = '{}w'.format(weeks)
        if rest_days != 0:
            res = '{0} {1}d'.format(res, rest_days)
        return res.strip().replace('.0d', 'd').replace('.0w', 'w')

    def __try_get_el_from_dict(self, _dict, fields_sequence):
        try:
            for field in fields_sequence:
                _dict = _dict[field]
        except:
            _dict = None
        return _dict

    def extract_issue_info(self, issue):
        def conv_to_date(s): return None if s is None else datetime.strptime(
            s, '%Y-%m-%d').date()
        res = {'key': issue['key']}
        fields = issue['fields']
        res['assignee'] = self.__try_get_el_from_dict(
            fields, ['assignee', 'displayName'])
        res['parent'] = self.__try_get_el_from_dict(fields, ['parent', 'key'])
        res['resolution'] = self.__try_get_el_from_dict(
            fields, ['resolution', 'name'])
        res['issuelinks'] = fields['issuelinks']
        res['priority'] = fields['priority']['name']
        res['creator'] = fields['creator']['name']
        res['reporter'] = fields['reporter']['name']
        res['duedate'] = fields['duedate']
        res['summary'] = fields['summary']
        res['status'] = fields['status']['name']
        res['timeestimate'] = self.sec_to_day_weeks(fields['timeestimate'])
        res['timeoriginalestimate'] = self.sec_to_day_weeks(
            fields['timeoriginalestimate'])
        res['start_date'] = conv_to_date(
            self.__try_get_el_from_dict(fields, ['customfield_11164']))
        res['end_date'] = conv_to_date(
            self.__try_get_el_from_dict(fields, ['customfield_11163']))
        try:
            sprint = dict(map(lambda s: s.split("="),
                          fields['customfield_10100'][0].split(',')))
            res['sprint_state'] = sprint['state']
            res['sprint_name'] = sprint['name']
            res['sprint_startdate'] = conv_to_date(sprint['startDate'][:10])
            res['sprint_enddate'] = conv_to_date(sprint['endDate'][:10])
        except:
            pass
        return res

    def undone_custom_report(self, project: str):
        def update_status(status: str, start_date, end_date):
            _now = datetime.now().date()
            if end_date <= _now:
                res = 'close'
            elif _now >= start_date and status == 'Создано':
                res = 'work'
            else:
                res = "ok"
            return res
        undone_sprint_issues = self.find_issues(
            project_list=[project], custom='statusCategory!=Done%20', max_results=1000)
        df = DataFrame(map(self.extract_issue_info, undone_sprint_issues))
        df['term'] = df['timeestimate'] + '/'+df['timeoriginalestimate']
        df['update_state'] = df[['status', 'start_date', 'end_date']].apply(
            lambda row: update_status(*row), axis=1)

        df.sort_values(by=['sprint_state', 'end_date'],
                       ascending=(True, False), inplace=True)
        df.reset_index(drop=True, inplace=True)
        # report_columns=['key','assignee','update_state','status','start_date','end_date','sprint_state','sprint_name','term']
        return df  # [report_columns]

    def color_undone_custom_report(self, color_df):
        def highlight_cols(value):
            if value == 'ok':
                color = '#e6ffe6'
            elif value == 'ACTIVE':
                color = '#E3F6F5'
            elif value == 'FUTURE':
                color = '#EFEEB4'
            else:
                color = '#ffe6e6'
            return 'background-color: {}'.format(color)

        def color_term(value):
            arr = map(float, value.replace('d', '').split('/'))
            if 'w' in value or max(arr) > 3:
                color = '#ffe6e6'
            else:
                color = 'white'
            return 'background-color: {}'.format(color)
        report_columns = ['key', 'assignee', 'update_state', 'status',
                          'start_date', 'end_date', 'sprint_state', 'sprint_name', 'term']
        c_df = color_df[report_columns]
        style1 = c_df.style.applymap(highlight_cols, subset=[
                                     'update_state', 'sprint_state'])
        style2 = c_df.style.applymap(color_term, subset=['term'])
        style2.use(style1.export())
        return style2

    def mass_transition(self, df) -> list:
        _arr = df[(df.sprint_name.notnull()) & (df.update_state != "ok")][[
            'key', 'update_state', 'status']].values.tolist()

        def worker(issue_key: str, transition_scenarion: str, status: str) -> tuple:
            if transition_scenarion == 'work':
                return (issue_key, self.transition_issue(issue_key, 11))
            else:
                if status == 'Создано':
                    self.transition_issue(issue_key, 11)
                response = self.transition_issue(issue_key, 91)
                if response is not True:
                    return (issue_key, response)
                else:
                    return (issue_key, self.transition_issue(issue_key, 121, 'Готово'))

        res = map(lambda args: worker(*args), _arr)
        # print(list(res))
        return DataFrame(res, columns=['issue', 'update_state'])
