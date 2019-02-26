from os import path,makedirs
import json
from MyAccounting.attributes import *
from MyAccounting.externaldata import cb
import datetime
class engine():
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
            return None
        return res[1]

    def add_account(self,account_number :str,account_descr_short :str,account_descr_long :str,account_parrent:int =None):
        acc=accounts_info(account_number,account_descr_short,account_descr_long,account_parrent)
        r=self.__add_row_template(operation_type='accounts_info',obj=acc)
        return r
    
    def currency_hist(self,currency: str,date_from,date_to=None):
        try:
            currency_id=self.driver.get_element('currency','code',currency)['currency_id']
            currency_id_rur=self.driver.get_element('currency','code','RUR')['currency_id']
        except:
            print ('Error:{} not exist in currency table'.format(currency))
            return False
        
        cb_cl=cb()
        res=cb_cl.cb_russia_currency_hist(currency,date_from,date_to)
        if res[0]:
            add_flg=0
            for el in res[1]:
                row=exchange_rate(to_buy=currency_id_rur,to_sell=currency_id,value=el['Value'],date=el['Date'],nominal=el['Nominal'])
                self.__add_row_template(operation_type='exchange_rate',obj=row,rare_operation=True)
        if date_from.weekday() in (6,0):
            if date_from.weekday()==6:
                add_days=-1
            else:
                add_days=-2
            res=cb_cl.cb_russia_currency_hist(currency,date_from+datetime.timedelta(days=add_days),date_to)
            el=res[1][0]		
            row=exchange_rate(to_buy=currency_id_rur,to_sell=currency_id,value=el['Value'],date=el['Date']+datetime.timedelta(days=-add_days),nominal=el['Nominal'])
            self.__add_row_template(operation_type='exchange_rate',obj=row,rare_operation=True)    
        


    def add_currency(self,code :str,symbol: str,description :str):
        new_currency=currency(code,symbol,description)
        r=self.__add_row_template(operation_type='currency',obj=new_currency,rare_operation=True)
        return r
    
    def add_customer(self,code :str,description :str):
        new_customer=customers(code,description)
        r=self.__add_row_template(operation_type='customers',obj=new_customer,rare_operation=True) 
        return r
    
    def add_measure(self,code :str,description :str):
        new_measure=measures(code,description)
        r=self.__add_row_template(operation_type='measures',obj=new_measure,rare_operation=True)
        return r

    def add_product(self,code :str,default_measure: str,description :str):
        default_measure_id=self.driver.get_element('measures','code',default_measure)['measure_id']
        new_product=products(code,default_measure_id,description)
        r=self.__add_row_template(operation_type='products',obj=new_product,rare_operation=True)
        return r



    def add_document(self,document_descr :str,date,customer_id: int=None):
        new_doc=document(document_descr,date,customer_id)
        r=self.__add_row_template(operation_type='documents',obj=new_doc) 
        return r

    def add_transaction(self,
                        id_account_from: int ,
                        id_account_to: int,
                        trans_date,
                        currency: int,
                        debet_from: bool,
                        value: float,
                        document_id :int,
                        description:str= None,
                        product_id : int=None,
                        amount :float =None,
                        is_currency: bool=None,
                        bank_acc_from :int=-1,
                        bank_acc_to :int=-1,
                        customer_id_from :int=-1,
                        customer_id_to :int=-1,
                        measure_id=None,analyticts4_to :str=None,analyticts4_from:str=None):
        
        new_trn=transaction(id_account_from,
                            id_account_to
                            ,trans_date
                            ,currency
                            ,debet_from
                            ,value
                            ,document_id                
                            ,description
                            ,product_id 
                            ,amount 
                            ,is_currency
                            ,bank_acc_from =bank_acc_from 
                            ,bank_acc_to= bank_acc_to 
                            ,customer_id_from=customer_id_from 
                            ,customer_id_to= customer_id_to 
                            ,measure_id=measure_id,analyticts4_to=analyticts4_to,analyticts4_from=analyticts4_from
                           )
			   
										   
        r=self.__add_row_template(operation_type='transactions',obj=new_trn)  
        if r is None:
            self.__del_trns([r])
            return None,None,None
        r2=self.add_account_rec(id_account_from,trans_date,value,amount,is_currency,
                                debet_from,currency,product_id,measure_id,bank_acc_from,customer_id_from,analyticts4_from)
        
        if r2 is None:
            self.__del_trns([r,r2])
            
        r3=self.add_account_rec(id_account_to,trans_date,value,amount,is_currency,
                                not debet_from,currency,product_id,measure_id,bank_acc_to,customer_id_to,analyticts4_to)
        
        if r3 is None:
            self.__del_trns([r,r2,r3])      
            
        return [r,r2,r3]
    
    def add_acc_report(self,account_id,transaction_date,value,amount,
                        is_currency,is_debet,currency,prod_id,measure_id,
                        bank_account,customer_id,analyticts4):
        report_date=datetime.datetime(transaction_date.year,12,31)
        if is_currency:
            search_pair= [('account_id',[account_id]),('currency',[currency])]
        else:
            search_pair=[('account_id',[account_id]),('prod_id',[prod_id])]
        search_pair=search_pair+[('report_type',['Y']),('analyticts4',[analyticts4])]        
        conditions=self.driver.where_multiple_conditions(search_pair)
        conditions_copy=conditions.copy()     
        
        if amount is None:
            amount=0
        if is_debet:
            dict_with_new_values={'value_beg_d':value,'value_end_d':value}
        else:
            dict_with_new_values={'value_beg_c':value,'value_end_c':value}
            amount =-amount
        if amount!=0:
            dict_with_new_values.update({'amount_beg':amount,'amount_end':amount})
        
        
        exist_year= self.driver.get_element('accounts','transaction_date',report_date,ext_condition=conditions,
                                            return_fields=['account_row_id'])
 
        if exist_year is None:
            row=None  
            value_beg_c,value_beg_d,amount_beg=0,0,0			
            conditions_copy.update(self.driver.where_condition('transaction_date',report_date,'$lt'))
            generator=self.driver.get_data_pointer('accounts',conditions_copy,
                                                  return_fields=['value_end_c',
                                                                 'value_end_d','amount_end','transaction_date'],
                                                  sort_arr=['transaction_date','desc'])    
											  

            new_acc=accounts(account_id=account_id,
                             transaction_date=report_date,
                              value_beg_c=value_beg_c,
                              value_end_c=value_beg_c,
                              value_beg_d=value_beg_d,
                              value_end_d=value_beg_d,
                              amount_beg=amount_beg,
                              amount_end=amount_beg,
                              currency=currency,
                              prod_id=prod_id,
                              measure_id=measure_id,
                             last_record=0,
                              bank_account=bank_account,
                              customer_id=customer_id,
                             report_type='Y',
                             analyticts4=analyticts4) 
            exist_year_row_id=self.__add_row_template(operation_type='accounts',obj=new_acc)
        else:
            exist_year_row_id=exist_year['account_row_id'] 		
        self.driver.update_element('accounts','account_row_id',
                                   exist_year_row_id,
                                   {k:v for k, v in dict_with_new_values.items() if '_beg' not in k}  
                                   ,operator='$inc')
        conditions_copy=conditions.copy() 
        conditions_copy.update(self.driver.where_condition('transaction_date',report_date,'$gt'))
        generator=self.driver.get_data_pointer('accounts',conditions_copy,return_fields=['account_row_id'])
        for row in generator:
            row_id=row['account_row_id']
            self.driver.update_element('accounts','account_row_id',row_id,dict_with_new_values,operator='$inc')
        return exist_year_row_id
       

        
    def add_account_rec(self,account_id :int,transaction_date,value,amount,
                        is_currency,is_debet,currency,prod_id=None,measure_id=None,
                        bank_account=-1,customer_id=-1,analyticts4=None):
        
        def get_last_month_day(any_day):
            next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  
            return next_month - datetime.timedelta(days=next_month.day)

        transaction_date=get_last_month_day(transaction_date)
      
        if is_currency:
            search_pair= [('account_id',[account_id]),('currency',[currency])]
        else:
            search_pair=[('account_id',[account_id]),('prod_id',[prod_id])]
        conditions=self.driver.where_multiple_conditions(search_pair+[('report_type',['M']),('analyticts4',[analyticts4])])
        last_record=self.driver.get_element('accounts','last_record',1,ext_condition=conditions)
        conditions.update(self.driver.where_condition('transaction_date',transaction_date,'$gte'))
       
        if amount is None:
            amount=0
        if is_debet:
            dict_with_new_values={'value_beg_d':value,'value_end_d':value}
        else:
            dict_with_new_values={'value_beg_c':value,'value_end_c':value}
            amount =-amount
        if amount!=0:
            dict_with_new_values.update({'amount_beg':amount,'amount_end':amount})
        row_id=None
        new_acc=False
        #вставка первой записи
        if last_record is None:
            if is_debet:
                value_end_c=0
                value_end_d=value
            else:
                value_end_c=value
                value_end_d=0  
           
            new_acc=accounts(account_id=account_id,
                             transaction_date=transaction_date,
                             value_beg_c=0,
                             value_end_c=value_end_c,
                             value_beg_d=0,
                             value_end_d=value_end_d,
                             amount_beg=0,
                             amount_end=amount,
                             currency=currency,
                             prod_id=prod_id,
                             measure_id=measure_id,last_record=1,
                             bank_account=bank_account,
                             customer_id=customer_id,analyticts4=analyticts4)          
        else:
            #ищем транзакции после текущей
            flg=False

            generator=self.driver.get_data_pointer('accounts',conditions,return_fields=['account_row_id','transaction_date'],sort_arr=['transaction_date','desc'])

            row_id=None
            for row in generator:
                row_date=row['transaction_date']
                row_id=row['account_row_id']
                if row_date==transaction_date:
                    dict_with_new_values={k:v for k, v in dict_with_new_values.items() if '_beg' not in k}  
                    r=row_id
                    flg=True
                self.driver.update_element('accounts','account_row_id',row['account_row_id'],dict_with_new_values,operator='$inc')

            if not flg and row_id is not None:
                #если после текущей были транзакции но в этот день их не было
                row=self.driver.get_element('accounts','account_row_id',row_id,return_fields=['value_beg_c','value_beg_d','amount_beg'])
                if is_debet:
                    value_beg_c=row['value_beg_c']
                    value_beg_d=row['value_beg_d']-value
                else:
                    value_beg_d=row['value_beg_d']
                    value_beg_c=row['value_beg_c']-value
                new_acc=accounts(account_id=account_id,
                                 transaction_date=transaction_date,
                                 value_beg_c=value_beg_c,
                                 value_end_c=row['value_beg_c'],
                                 value_beg_d=value_beg_d,
                                 value_end_d=row['value_beg_d'],
                                 amount_beg=row['amount_beg']-amount,
                                 amount_end=row['amount_beg'],
                                 currency=currency,
                                 prod_id=prod_id,
                                 measure_id=measure_id,bank_account=bank_account,customer_id=customer_id,analyticts4=analyticts4) 
            #если  транзакции после текущей отсутсвуют
            if row_id is None:
                if is_debet:
                        value_end_c=0
                        value_end_d=value
                else:
                    value_end_c=value
                    value_end_d=0  
                new_acc=accounts(account_id=account_id,transaction_date=transaction_date,
                                     value_beg_c=last_record['value_end_c'],
                                     value_end_c=last_record['value_end_c']+value_end_c,
                                     value_beg_d=last_record['value_end_d'],
                                     value_end_d=last_record['value_end_d']+value_end_d,
                                     amount_beg=last_record['amount_end'],
                                     amount_end=last_record['amount_end']+amount,
                                     currency=currency,
                                     prod_id=prod_id,
                                     measure_id=measure_id,last_record=1,bank_account=bank_account,customer_id=customer_id,analyticts4=analyticts4) 
                self.driver.update_element('accounts','account_row_id',last_record['account_row_id'],{'last_record':0})            
            
      
        if new_acc:
            r=self.__add_row_template(operation_type='accounts',obj=new_acc) 
        self.add_acc_report(account_id ,transaction_date,value,amount,
                        is_currency,is_debet,currency,prod_id,measure_id,
                        bank_account,customer_id,analyticts4)

        """
        last_trn_date=self.driver.get_element('constants','key','last_trn_date')
        first_trn_date=self.driver.get_element('constants','key','first_trn_date')
        if last_trn_date is None:
            self.driver.add_row('constants',constants('last_trn_date',transaction_date),rare_operation=True)
            self.driver.add_row('constants',constants('first_trn_date',transaction_date),rare_operation=True)
        else:
            last_trn_date_old=last_trn_date['value']
            if last_trn_date_old<transaction_date:
                self.driver.update_element('constants','key','last_trn_date',{'value':transaction_date})
        """
        return r
 

    def add_bank_account(self,bank_name :str,account: str,account_short_name :str,currency :str,expire_date=None):
        currency_id=self.driver.get_element('currency','code',currency)['currency_id']	
        new_acc=bank_accounts(self.driver.get_element('customers','description',bank_name,['customer_id'])['customer_id'],account,account_short_name,currency_id,expire_date=expire_date)
        
        r=self.__add_row_template(operation_type='bank_accounts',obj=new_acc,rare_operation=True) 
        return r

    def used_tables(self):
        return self.driver.used_tables()