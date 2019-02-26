from MyAccounting import engine
import datetime
from math import ceil
import pandas as pd
class MyAccounting(engine):

    def __bulk_transaction(self,trans_array):
        arr=[]
        for trn in trans_array:
            inserted_id=self.add_transaction(**trn)
            if inserted_id is not None:
                arr.append(inserted_id)
            else:
                for el in arr:
                    self.__del_trns(inserted_id)
                return False
        return True
    
    def __uround(self,num,precision=2):
        multiplier=10**precision
        return ceil(num*multiplier)/multiplier

    def __get_bank_acc(self,acc_name,return_fields=['bank_account_id']):      
        return self.driver.get_element('bank_accounts','account', acc_name,return_fields=return_fields)
  
    def __check_existance(self,table,column,keys):
        arr=self.get_values(table,column,keys,[column])
        arr=[el[column] for el in arr]
        return (set(arr)==set(keys),set(arr)-set(keys))

    def __get_currency_id(self,currency):
        return self.driver.get_element('currency','code',currency,['currency_id'])['currency_id']   

    def __get_acc_id(self,account_name):
        return self.driver.get_element('accounts_info','account_number',account_name,['account_id'])['account_id']
    

    
    def exchange_time_range(self,currency_to_buy :str='RUR',currency_to_sell : str=None):
        currency_to_buy_id=self.driver.get_element('currency','code',currency_to_buy,['currency_id'])['currency_id']
        currency_to_sell_id=self.driver.get_element('currency','code',currency_to_sell,['currency_id'])['currency_id']
        
        conditions=self.driver.where_multiple_conditions([('to_buy',[currency_to_buy_id]),('to_sell',[currency_to_sell_id])])
        return self.driver.range_id('exchange_rate','date',conditions)
    
    def update_exchange(self,date,currency_to_buy :str='RUR',currency_to_sell : str=None):
        currency_to_buy_id=self.driver.get_element('currency','code',currency_to_buy,['currency_id'])['currency_id']
        currency_to_sell_id=self.driver.get_element('currency','code',currency_to_sell,['currency_id'])['currency_id']              
        date_range=self.exchange_time_range(currency_to_buy,currency_to_sell)	
        if date_range[0] is None:
            self.currency_hist(currency_to_sell,date)
		
        elif date <date_range[0]:
            print(		date,date_range[0]+datetime.timedelta(days=-1))
            self.currency_hist(currency_to_sell,date,date_range[0]+datetime.timedelta(days=-1))	    
        elif date >date_range[1]:
            self.currency_hist(currency_to_sell,date_range[1]+datetime.timedelta(days=1))          
        conditions=self.driver.where_multiple_conditions([('to_buy',[currency_to_buy_id]),('to_sell',[currency_to_sell_id])])    
        return  self.driver.get_element('exchange_rate','date',date,['value'],conditions)['value']
    
    def buy_currency(self,currency,amount,value,bank_acc_from,bank_acc_to,date,customer,currency_to_sell="RUR",default_currency="RUR",document='Покупка валюты',doc_id=None):
        accounts=['52','51','91.2','57']
        flg=self.__check_existance('accounts_info','account_number',accounts)
        
        customer_id= self.driver.get_element('customers','description',customer,return_fields=['customer_id'])
        if customer_id is None:
            return 'Неизвестный контрагент'
        exchange_rate=self.update_exchange(date,currency_to_sell,currency)

        if flg[0]==False:
            print ('Отсутсвуют счета {}'.format(','.join(flg[1])))
        elif exchange_rate is None:
            print('Нет значения курса валюты на дату')
        else:
            acc_52=self.__get_acc_id('52')
            acc_51=self.__get_acc_id('51')
            acc_912=self.__get_acc_id('91.2')
            acc_57=self.__get_acc_id('57')  
            if not doc_id:
                doc_id=self.add_document(document,date)
            
            currency_id=self.__get_currency_id(currency)
            currency_id_default=self.__get_currency_id(default_currency)
            commission= self.__uround(value-amount*exchange_rate)
            
            bank_id_from=self.__get_bank_acc(bank_acc_from)['bank_account_id']
            bank_id_to=self.__get_bank_acc(bank_acc_to)['bank_account_id']
            trn_list=[ {'trans_date':date,
                       'currency':currency_id_default,
                       'debet_from':False,
                       'id_account_from':acc_51
                       ,'id_account_to':acc_57,
                       'value':value,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':0,
                       'description':'Покупка валюты'
                       ,'bank_acc_from':bank_id_from
       
                       ,'customer_id_to':customer_id['customer_id']
                    
                      },
                                                                
                     {'trans_date':date,
                       'currency':currency_id,
                       'debet_from':False,
                       'id_account_from':acc_57
                       ,'id_account_to':acc_52,
                       'value':value,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':amount,
                       'description':'Покупка валюты'
                       ,'customer_id_from':customer_id['customer_id']
                       ,'bank_acc_to':bank_id_from
                  
                      },
                      {'trans_date':date,
                       'currency':currency_id_default,
                       'debet_from':False,
                       'id_account_from':acc_52
                       ,'id_account_to':acc_912,
                       'value':commission,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':0,
                       'description':'Комиссия контрагента (покупка валюты)'
                       ,'bank_acc_from':bank_id_from
    
                       ,'customer_id_to':customer_id['customer_id']
                
                      }
                     ]
          
            if self.__bulk_transaction(trn_list):
                print('Successful')
            else:
                print('Error')

    def invest_money(self,money,date,bank_acc,currency='RUR',document='Вложение личных средств',doc_id=None):
        acc_51=self.__get_acc_id('51')
        acc_721=self.__get_acc_id('72.1')
        currency_id=self.driver.get_element('currency','code',currency,['currency_id'])['currency_id']
        
        if not doc_id:
            doc_id=self.add_document(document,date)
        
        bank_id=self.__get_bank_acc(bank_acc)['bank_account_id']

        trn_list=[{'trans_date':date,
                       'currency':currency_id,
                       'debet_from':False,
                       'id_account_from':acc_721
                       ,'id_account_to':acc_51,
                       'value':money,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':0,
                       'description':'Вложение личных средств'
                       ,'bank_acc_to':bank_id
                  
                      }
                 ]
        if self.__bulk_transaction(trn_list):
            print('Successful')
        else:
            print('Error')
            
    def get_values(self,table,column,array_,return_fields):
        condition=self.driver.where_condition(column,array_)
        return self.driver.get_data(table,condition,False,return_fields)    

    def add_deposit(self,date,acc_from,acc_to,amount,document='Перевод средств на депозит',doc_id=None):
        accounts=['52','51','58.3']
        
        acc_from_obj=self.__get_bank_acc(acc_from,return_fields=['bank_account_id','currency_id'])
        acc_to_obj=self.__get_bank_acc(acc_to,return_fields=['bank_account_id','currency_id'])
        currency_id=acc_from_obj['currency_id']
        if currency_id!=acc_to_obj['currency_id']:
            print('Ошибка:валюта счетов не совпадает')
            return None

        flg=self.__check_existance('accounts_info','account_number',accounts)
        currency_id_rur=self.__get_currency_id('RUR')
        if currency_id==currency_id_rur:
            acc_5251=self.__get_acc_id('51')
            value=amount
            amount=0
        else:
            acc_5251=self.__get_acc_id('52') 
            value=0
        acc_583=self.__get_acc_id('58.3')  
        if not doc_id:
            doc_id=self.add_document(document,date)

        trn_list=[ {'trans_date':date,
                       'currency':currency_id,
                       'debet_from':False,
                       'id_account_from':acc_5251
                       ,'id_account_to':acc_583,
                       'value':value,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':amount,
                       'description':'Перевод средств на депозит'
                       ,'bank_acc_from':acc_from_obj ['bank_account_id']
                       ,'bank_acc_to':acc_to_obj ['bank_account_id'],'analyticts4_to':'тело депозита'
                  
                      }
                     ]
           
        if self.__bulk_transaction(trn_list):
            print('Successful')
        else:
            print('Error')
    def transactions_info_pretty(self,return_fields=None,currency_names=True,account_names=True,
                                 amount_with_measures=True,trans_pretty=True,drop_id=True,
                                 drop_columns=['trans_id', 'account_to', 'currency_name', 'creation_date',
                                               'account_from', 'document_id', 'is_currency', 'debet_from','bank_account_to', 'customer_to_bank',
											   'customer_id_to','account_from1', 'customer_from_bank', 
											   'customer_id_from','bank_acc_from','bank_acc_to', 'account_to1', 'bank_account_from']):
        pair=['Дт','Кт']
        template='{2}{0}-{3}{1}'
        pref_order=['transaction','trans_date','value','amount','product_id','description',
                    'analytics_from1','analytics_from2','analytics_from3','analyticts4_from','analytics_to1',
                    'analytics_to2','analytics_to3','analyticts4_to']
        look_up_arr=[]
        if drop_columns:
            pass
        else:
            drop_columns=[]
        if currency_names:
            cur_symbol='cur_symbol'
            look_up_arr.append({'collection':'currency',
                                'match':[('currency','currency_id',[('description','currency_name'),
                                                                    ('symbol',cur_symbol)])]})
            if return_fields:
                if cur_symbol not in return_fields:
                    drop_columns.append(cur_symbol)
            if drop_id:
                drop_columns.append(cur_symbol)
                drop_columns.append('currency')
        if account_names:
            look_up_arr.append({'collection':'accounts_info',
                                'match':[('id_account_from','account_id',[('account_number','account_from')])]})
            look_up_arr.append({'collection':'accounts_info',
                                'match':[('id_account_to','account_id',[('account_number','account_to')])]})                                                        
            if drop_id:
                drop_columns=drop_columns+['id_account_from','id_account_to']
        ############################
        look_up_arr=look_up_arr+[{'collection':'bank_accounts',
                            'match':[('bank_acc_from','bank_account_id',[('account','bank_account_from'),
                                                                         ('account_short_name','account_from1'),
                                                                         ('customer_id','customer_from_bank')])]},
                           {'collection':'bank_accounts',
                            'match':[('bank_acc_to','bank_account_id',[('account','bank_account_to'),
                                                                         ('account_short_name','account_to1'),
                                                                         ('customer_id','customer_to_bank')])]}]
        
        df=self.driver.look_up_tables('transactions',look_up_arr) 
        customers=list(set(df[['customer_to_bank','customer_from_bank',
                              'customer_id_to','customer_id_from']].values.ravel())-set([-1]))
        customers=self.get_values('customers','customer_id',customers,return_fields=['customer_id','description'])
        customers={el['customer_id']:el['description'] for el in customers}	
        def f(row):
            ff=lambda x:-1 if x is None else x 		
            el1=ff(row[0])
            el2=ff(row[1])				
            if el1>-1:	
                r=customers[el1]
            elif el2>-1:			
                r=customers[el2]
            else:
                r=None
            return r	
        df['analytics_from1']=df[['customer_from_bank','customer_id_from']].apply(lambda row:f(row),axis=1)
        df['analytics_from2']=df['bank_account_from']
        df['analytics_from3']=df['account_from1']
        df['analytics_to1']=df[['customer_to_bank','customer_id_to']].apply(lambda row:f(row),axis=1)
        df['analytics_to2']=df['bank_account_to']
        df['analytics_to3']=df['account_to1']			
        if amount_with_measures:
            isNone=lambda x:'0' if x is None or x=='' else str(x)
            df['amount']=df[['amount',cur_symbol]].apply(lambda row:isNone(row[0])+' '+row[1],axis=1)
       
        if trans_pretty:
            f=lambda row,pair:template.format(*row[:2],*pair)
            df['transaction']=df[['account_from',
                                  'account_to',
                                  'debet_from']].apply(lambda row:f(row,pair) if row[2] else f(row,pair[::-1]),axis=1)
            
            

        
        df.drop(drop_columns,axis=1,inplace=True)
        res_order=[]
        cols=df.columns
        for el in pref_order:
            if el in cols:
                res_order.append(el)
        res_order=res_order+list(set(cols)-set(res_order))
        return df[res_order]

    def accounts_pretty(self,return_fields=None,currency_names=True,account_names=True,
                                 amount_with_measures=True,drop_id=True,
                                 drop_columns=['account_id', 'account_row_id', 'creation_date', 'currency',
                                               'measure_id', 'prod_id', 'updated','currency_name','account_from1',
											   'bank_account_from',	'bank_account'	,'customer_id'	,'customer_from_bank']):
        pair=['Дт','Кт']
        template='{2}{0}-{3}{1}'
        pref_order=['account','analytics1','analytics2','analytics3','analyticts4','transaction_date','value_beg_d','value_beg_c','amount_beg','amount_end','value_end_d','value_end_c','last_record']
        look_up_arr=[]
        if drop_columns:
            pass
        else:
            drop_columns=[]
        if currency_names:
            cur_symbol='cur_symbol'
            look_up_arr.append({'collection':'currency',
                                'match':[('currency','currency_id',[('description','currency_name'),
                                                                    ('symbol',cur_symbol)])]})
            if return_fields:
                if cur_symbol not in return_fields:
                    drop_columns.append(cur_symbol)
            if drop_id:
                drop_columns.append(cur_symbol)
                drop_columns.append('currency')
        if account_names:
            look_up_arr.append({'collection':'accounts_info',
                                'match':[('account_id','account_id',[('account_number','account')])]})
                                                     
            if drop_id:
                drop_columns=drop_columns
        look_up_arr=look_up_arr+[{'collection':'bank_accounts',
                            'match':[('bank_account','bank_account_id',[('account','bank_account_from'),
                                                                         ('account_short_name','account_from1'),
                                                                         ('customer_id','customer_from_bank')])]}]
        df=self.driver.look_up_tables('accounts',look_up_arr)  
        df=self.driver.look_up_tables('accounts',look_up_arr)  
        customers=list(set(df[['customer_id','customer_from_bank']].values.ravel())-set([-1]))
        customers=self.get_values('customers','customer_id',customers,return_fields=['customer_id','description'])
        customers={el['customer_id']:el['description'] for el in customers}
        def f(row):
            ff=lambda x:-1 if x is None else x 		
            el1=ff(row[0])
            el2=ff(row[1])
            if el1>-1:	
                r=customers[el1]
            elif el2>-1:			
                r=customers[el2]
            else:
                r=None
            return r
        df['analytics1']=df[['customer_from_bank','customer_id']].apply(lambda row:f(row),axis=1)
        df['analytics2']=df['bank_account_from']
        df['analytics3']=df['account_from1']	

        if amount_with_measures:
            isNone=lambda x:'0' if x is None or x=='' else str(x)
            df['amount_beg']=df[['amount_beg',cur_symbol]].apply(lambda row:isNone(row[0])+' '+row[1],axis=1)
            df['amount_end']=df[['amount_end',cur_symbol]].apply(lambda row:isNone(row[0])+' '+row[1],axis=1)       
        drop_columns=[el for el in drop_columns if el in df.columns]
        df.drop(drop_columns,axis=1,inplace=True)
        res_order=[]
        cols=df.columns
        for el in pref_order:
            if el in cols:
                res_order.append(el)
        res_order=res_order+list(set(cols)-set(res_order))
        return df[res_order]
    def deposit_percents(self,money,date,bank_acc,document='Начисление процентов(капитализация)',doc_id=None):
        acc_583=self.__get_acc_id('58.3')
        acc_911=self.__get_acc_id('91.1')
        if not doc_id:
            doc_id=self.add_document(document,date)
        
        bank_obj=self.__get_bank_acc(bank_acc,return_fields=['bank_account_id','currency_id','customer_id'])
        currency_id_rur=self.__get_currency_id('RUR')
        if bank_obj['currency_id']==currency_id_rur:
            amount=0
            value=money
        else:
            amount=money
            value=0
        trn_list=[{'trans_date':date,
                       'currency':bank_obj['currency_id'],
                       'debet_from':True,
                       'id_account_from':acc_583
                       ,'id_account_to':acc_911,
                       'value':value,
                       'document_id':doc_id,
                       'is_currency':True,
                       'amount':amount,
                       'description':'Начисление процентов(капитализация)',
                       'bank_acc_from':bank_obj['bank_account_id'],
                        'customer_id_to':bank_obj['customer_id'],'analyticts4_from':'Проценты на депозит'
                           
                  
                      }
                 ]
        if self.__bulk_transaction(trn_list):
            print('Successful')
        else:
            print('Error')	
			
    def process_alfa(self,file_path,exclude_date=True):
        import datetime
        from ntpath import basename
        df=pd.read_csv(file_path,sep=';',encoding='utf-8')
        #return df
        doc_id=self.add_document(basename(file_path)[:-4],datetime.datetime.now())
        df['Дата операции']=df['Дата операции'].apply(lambda t:datetime.datetime.strptime(t, '%d.%m.%Y'))
        if exclude_date:
            exclude_date=datetime.datetime.strptime(file_path[-14:-4], '%Y-%m-%d')
            df.drop(df[df['Дата операции']==exclude_date].index,inplace=True)
        df['Приход']=df['Приход'].apply(lambda t :float(t.replace(',','.'))) 
        
        get_account=lambda acc_name:self.driver.get_element('bank_accounts',
                                                              'account',
                                                               acc_name,
                                                              ['account_short_name','bank_account_id'])

        salary_deposit_obj=get_account('Альфа-Банк(накопилка)')                                                
        salary_acc_obj=get_account('Альфа-Банк(зарплатный)')  
        salary_deposit=salary_deposit_obj['account_short_name']


        for i,row in df[df['Номер счёта']==salary_deposit].iterrows():
            income=row['Приход']
            operation_date=row['Дата операции']
            if row['Описание операции'][:20]=='Выплата проц. на ост':
                self.deposit_percents(income,operation_date,'Альфа-Банк(накопилка)',doc_id=doc_id)
            else:
                self.invest_money(income,operation_date,'Альфа-Банк(зарплатный)',doc_id=None)
                self.add_deposit(operation_date,'Альфа-Банк(зарплатный)'
                                 ,'Альфа-Банк(накопилка)',income,doc_id=doc_id)
        
        for deposit_acc_name in ['Альфа-Банк(депозит евро)','Альфа-Банк(депозит доллар)']:
            depost_acc=get_account(deposit_acc_name)['account_short_name']
            for i,row in df[df['Номер счёта']==depost_acc].iterrows():
                income=row['Приход']
                operation_date=row['Дата операции']
                if row['Описание операции'][:20]=='Выплата проц по деп.':
                    self.deposit_percents(income,operation_date,deposit_acc_name,doc_id=doc_id)                