from os import path,makedirs
import json
from MyAccounting.attributes import config,account,document,transaction,accounts_info

class MyAccounting():
    __slots__ ='config_path','config_empty','config','config_filename','driver'
    
    def __init__(self, config_path:str ):
        self.config_filename='MyAccounting_settings.json'
        self.config_path= config_path     
        file_path,path_exists=self.__check_file_existance(config_path)      
        if path_exists:
            self.config_empty=False  
            self.config_filename=file_path
            self.__load_config()
            self.__load_driver()
        else:
            self.config_empty=True
            print('Config file requed:use add_config function')
            
    def __check_file_existance(self,config_path: str)-> (str,bool):
        file_path=path.join(config_path,self.config_filename)
        return file_path,path.exists(file_path)
 
    def __load_config(self):
        try:
            with open(self.config_filename) as f:
                data = json.load(f)
            self.config=data
        except:
            print('Error reading config file')
            
    def __load_driver(self):
        if self.config['driver']=='mongo':
            from MyAccounting.drivers import MongoDriver
            self.driver=MongoDriver(self.config)
            print ("driver loaded")
        else:
            print('Unknown driver')
            

    def add_config(self,**kwargs):

        if self.config_empty:
            if not path.exists(self.config_path):
                makedirs(self.config_path)
            filename=path.join(self.config_path,self.config_filename)   
            self.config_filename=filename
            
            conf=config(**kwargs)

            with open(filename,'w') as f:
                json.dump(conf.data, f)
            self.config_empty=False
            self.__load_config()

    def add_account(self,account_number :str,account_descr_short :str,account_descr_long :str,account_parent :str =None):
        account_parent_id=None
        if account_parent:
            parent=self.driver.get_element('accounts_info','account_number',account_parent )
            if parent is None:
                print('No parent account found')
                return None
            account_parent_id=parent['account_id']
        acc=accounts_info(account_number,account_descr_short,account_descr_long,account_parent_id)
        res=self.driver.add_row('accounts_info',acc)
        if res[0]:
            print('success')
        else:
            print('Error: '+res[1])