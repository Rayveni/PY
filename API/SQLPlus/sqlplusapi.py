import os
from shutil import rmtree
from subprocess import Popen,PIPE
from utilites import mylogger
from time import strftime
from multiprocessing.dummy import Pool
import pandas as pd
class SqlPlus:
    def __init__(self,projectdirectory,delimiter='|',sql_plus_options_new=None,printlog=False):
        sql_plus_options_default=[('ECHO','OFF'),
                  ('NEWPAGE','None'),
                 ( 'SPACE','0'),
                  ('pagesize','0 embedded on'),
                  ('FEEDBACK','OFF'),
                  ('trimspool','on'),
                  ('HEADING','on'),
                  ('headsep','off'),
                  ('UNDERLINE','off'),
                  ('HEADSEP','off'),
                  ('tab','off'),
                  ('wrap' ,'off'),
                  ('linesize' ,'9999'),
                  ('VERIFY' ,'off'),
                   ('NUMWIDTH' ,'13')]
        if sql_plus_options_new:sql_plus_options_default=sql_plus_options_new
        self.base_options='\n'.join(['SET %s %s'% (key[0],key[1]) for key in sql_plus_options_default])+'\n'
        self.delimiter=delimiter
        self.prefix='error_'
        self.project=projectdirectory
        self.__make_directory__(projectdirectory,False)
        logdirectory=os.path.join(projectdirectory,'log')
        self.default_loaddirectory=os.path.join(projectdirectory,'load')
        self.__make_directory__(self.default_loaddirectory,False)
        self.__make_directory__(logdirectory,False)
        log_name=strftime('%Y_%m_%d %H_%M_%S')+'.log'
        self.logger=mylogger(os.path.join(logdirectory,log_name),printlog)
        self.logger.info('Project initialisation')
        self.sql=b''
    
    def printlines(self,string):
        if type(string)==bytes:string=string.decode('utf-8')
        res=list(map(print,string.split('\n')))
        
    def set_sql_query(self,query_params={},sql_path=None,query=None):
        if sql_path:
            with open(sql_path, 'r') as f:
                sql=f.read()
        elif query:
            sql=query
        else:
            print('Необходимо задать путь к SQL файлу(переменная sql_path)')
            print('или ввести строку запроса в переменную query')
            return None
        var_options=''
        if query_params:
            var_options='\n'.join(['DEFINE %s=%s'% (key,query_params[key]) for key in query_params.keys()])+'\n'
        self.sql=str.encode(self.base_options+var_options+'SET colsep "%s"\n'%self.delimiter+sql)
        return self.sql
        
    def __make_directory__(self,directory,drop=True):
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif drop:
            rmtree(directory)
            os.makedirs(directory)
    def prepareload(self,path):
        self.__make_directory__(path)
        self.logger.info("Created load directory %s, content removed"%path)

    def write_query(self,path='default',query='',display=True):
        if path=='default':path=os.path.join( self.project,'tempsql.sql')
        if query=='':query=self.sql
        with open(path, 'w') as w:
            w.write(query.decode("utf-8")) 
        self.logger.info('write_query to %s' %path)
        if display:
            self.printlines(query)
            
    def FetchData(self,conn_str,savepath,sql=None):
        if sql==None:sql=self.sql
        with Popen(['sqlplus', '-S', conn_str], shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE) as session:
            session.stdin.write(sql)
            res = session.communicate()[0]
            prefix=''
            if res[:5]==b'ERROR' :
                prefix=self.prefix
        with open(os.path.join(os.path.dirname(savepath),prefix+os.path.basename(savepath)), 'w') as w:
            w.write(res.decode("utf-8"))
    
    def ThreadPool(self,f,applylist,n_threads=-1,asyncmap=True):
        if n_threads==-1:n_threads=len(applylist)
        msg='%s ThreadPool: threads:%s async:%s'
        with Pool(n_threads) as trpool:
            if asyncmap:
                self.logger.info(msg%('Start',n_threads,asyncmap))
                trpool.map_async(f, applylist)
                trpool.close()
                trpool.join()  

            else:
                self.logger.info(msg%('Start',n_threads,asyncmap))
                result=trpool.map(f, applylist) 
                trpool.close()
                trpool.join() 
                self.logger.info(msg%('Finished',n_threads,asyncmap)) 
                return result
        self.logger.info(msg%('Finished',n_threads,asyncmap))
		
    def read_loaded_csv(self,var):
        fullpath=var[1]
        filename=var[0]
        try:
            df=pd.read_csv(fullpath, sep=self.delimiter)
            df['filename']=filename
        except Exception as e:
            self.logger.warning='Error'+str(e)+filename
            return pd.DataFrame()
        return df
		