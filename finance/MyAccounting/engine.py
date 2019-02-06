from os import path,makedirs
import json
from MyAccounting.attributes import config,account,document,transaction,accounts_info,currency,exchange_rate
from MyAccounting.externaldata import cb
class MyAccounting():
    __slots__ ='config_path','config_empty','config','config_filename','driver'
    
    def __init__(self, config_path:str):
        self.config_filename='MyAccounting_settings.json'
        self.config_path= config_path     
        file_path,path_exists=self.__check_file_existance(config_path)      
        if path_exists:
            self.config_empty=False  
            self.config_filename=file_path
            self.__load_config()
            self.__load_driver()
            #self.default_currency=[default_currency,None]
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
            
    def drop_db(self):
        self.driver.drop_db()
        #self.default_currency[1]=None
        
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

    def __add_row_template(self,**kwargs):
        res=self.driver.add_row(**kwargs)
        if res[0]:
            print('success')
        else:
            print('Error: '+res[1])

    def add_account(self,account_number :str,account_descr_short :str,account_descr_long :str,account_parrent:int =None):
        acc=accounts_info(account_number,account_descr_short,account_descr_long,account_parrent)
        self.__add_row_template(operation_type='accounts_info',obj=acc)	

    def currency_hist(self,currency: str,date_from,date_to=None):
        try:
            currency_id=self.driver.get_element('currency','code',currency)['currency_id']
            currency_id_rur=self.driver.get_element('currency','code','RUR')['currency_id']
        except:
            print ('Error:{} not exist in currency table'.format(currency))
            return False
        
        cb_cl=cb()
        res=cb_cl.cb_russia_currency_hist(currency,date_from)
        if res[0]:
            for el in res[1]:
                row=exchange_rate(to_buy=currency_id_rur,to_sell=currency_id,value=el['Value'],date=el['Date'],nominal=el['Nominal'])
                self.__add_row_template(operation_type='exchange_rate',obj=row,rare_operation=True)
        


    def add_currency(self,code :str,symbol: str,description :str):
        new_currency=currency(code,symbol,description)
        self.__add_row_template(operation_type='currency',obj=new_currency,rare_operation=True)
        
    def transaction(self,id_account_from: int,id_account_to: int,trans_date,currency: int,debet_from: bool,value: float,document_id :int,description:str= None):
        new_trn=transaction(id_account_from,id_account_to,trans_date,currency,debet_from,value,document_id,description)
        self.__add_row_template(operation_type='transactions',obj=new_trn)        
