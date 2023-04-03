import datetime
from pymongo import MongoClient,DESCENDING,ASCENDING
from pandas import DataFrame

class MongoDriver():
    __slots__ ='db','accounts_info','accounts','documents','transactions','variables','__client','id_dict','mapping','config'
    def __init__(self,config: dict):
        
        self.__client=MongoClient(config['host'],config['port'])
        self.db=self.__client[config['db_name']]
        self.accounts_info=self.db[config['accounts_info']]
        self.accounts=self.db[config['accounts']]
        self.documents=self.db[config['documents']]
        self.transactions=self.db[config['transactions']]        
        self.variables=self.db[config['variables']]   
        
        self.config={'currency': config['currency'],
                     'exchange_rate': config['exchange_rate'],
                     'measures':config['measures'],
                     'products':config['products'],
                     'customers':config['customers'],'bank_accounts':config['bank_accounts'],'constants':config['constants']
                    }

        
        self.mapping={'accounts_info':['account_id'],
                      'accounts':['account_row_id'],
                      'documents':['document_id'],
                      'transactions':['trans_id'],
                      'currency':['currency_id'],
                      'exchange_rate':['exchange_rate_id'],
                      'products':['product_id'],
                      'measures':['measure_id'],
                      'customers':['customer_id'],'bank_accounts':['bank_account_id'],'constants':['constants_id']
                     }
        self.__add_indexes()
        self.__get_id_dict()
        
    def __add_indexes(self) :
        if self.variables.find_one() is None:
            self.accounts_info.create_index([("account_number", ASCENDING)],unique=True)
            self.documents.create_index([("document_id", ASCENDING), ("date", ASCENDING)],unique=True)
            self.transactions.create_index([("'id_account_from", ASCENDING)],unique=False)
            self.transactions.create_index([("'id_account_to", ASCENDING)],unique=False)			           
            self.variables.create_index([("var", DESCENDING)],unique=True)
            self.db[self.config['currency']].create_index([("code", DESCENDING)],unique=True)
            self.db[self.config['exchange_rate']].create_index([("date", DESCENDING),("to_buy", DESCENDING),("to_sell", DESCENDING)],unique=True)	
            self.db[self.config['measures']].create_index([("code", DESCENDING)],unique=True)
            self.db[self.config['products']].create_index([("code", DESCENDING)],unique=True)
            self.db[self.config['customers']].create_index([("code", DESCENDING)],unique=True)
            self.db[self.config['bank_accounts']].create_index([("account", DESCENDING)],unique=True)
            self.db[self.config['bank_accounts']].create_index([("account_short_name", DESCENDING)],unique=True)

            self.accounts.create_index([("transaction_date", DESCENDING),("last_record", DESCENDING),("account_id", DESCENDING) ,("bank_account", DESCENDING) ,("customer_id", DESCENDING) ,("report_type", DESCENDING) ],unique=False)		
            self.accounts.create_index([("report_type", DESCENDING),("last_record", DESCENDING)],unique=False)				
            self.__add_indexes_id()
          
    def __add_indexes_id(self) :
        for key,value in self.mapping.items():
            val=value[0]
            if val is not None:
                collection=self.__collection_pointer(key)
                collection.create_index([(val, DESCENDING)],unique=True)   

    def __get_id_dict(self):
        res=self.variables.find_one({'var':'id_dict'})
        if res is None:
            dict_trn={'document_id':0,'account_id':0,'document_id':0,'trans_id':0,'account_row_id':0}
            ins_id=self.variables.insert_one({'var':'id_dict','value':dict_trn}).inserted_id
            self.id_dict=(ins_id,dict_trn)
        else:
            self.id_dict=(res['_id'],res['value'])
            
    def drop_db(self):
        self.__client.drop_database(self.db.name)
        self.__add_indexes()
        self.__get_id_dict()
        
        
    def __increment_id(self,id_attr)-> int:
        next_attr_value=self.id_dict[1][id_attr]+1
        self.variables.update_one({'_id':self.id_dict[0]},{'$set':{'value.'+id_attr:next_attr_value}})   
        self.id_dict[1][id_attr]=next_attr_value
        return next_attr_value

    def __max_id(self,collection, column,condition={},int_res=True)-> int:
        res=collection.find_one(condition,sort=[(column,DESCENDING)])
        if res is None and int_res:
            res=-1
        elif res is None:
            res=None
        else:
            res=res[column]
        return res
		
    def __min_id(self,collection, column,condition={},int_res=True)-> int:
        res=collection.find_one(condition,sort=[(column,ASCENDING)])
        if res is None and int_res:
            res=-1
        elif res is None:
            res=None
        else:
            res=res[column]
        return res 
		
    def range_id(self,collection, column,condition={}):
        collection=self.__collection_pointer(collection)
        return self.__min_id(collection, column,condition,False),self.__max_id(collection, column,condition,False)
		
    def __collection_pointer(self,table):
        try:
            collection=getattr(self,table)
        except:
            collection=self.db[self.config[table]]
        return collection
    
    def add_row(self,operation_type,obj,creation_date=None,rare_operation=False)->str:
        res={key:getattr(obj, key) for key in obj.__slots__}
        attr=self.mapping[operation_type][0]
        
        
        collection=self.__collection_pointer(operation_type)
       
        try:           
            if attr is not None:
                if not rare_operation:
                    res[attr]=self.__increment_id(attr)
                else:
                    res[attr]=self.__max_id(collection, attr)+1                 
            if creation_date is None:
                res['creation_date']=datetime.datetime.now()
            else:
                res['creation_date']=creation_date
                print(res)
            collection.insert_one(res)
            return_message=(True,res[attr])
        except Exception as e: 
            return_message=(False,str(e))
        return return_message

    def where_condition(self,column,array_,operand='$in'):
        return {column:{operand:array_}}

    def where_multiple_conditions(self,array_conditions,operand='$in'):
        res={}
        for condition in array_conditions:
            res.update(self.where_condition(condition[0],condition[1],operand))
        return res
     
    def __process_condition_return_fields(self,condition,return_fields):
        if condition:
            pass
        else:
            condition={}      
        r_fields={ "_id": False }
        if return_fields:
            for field in return_fields:
                r_fields[field]=True
        return condition,r_fields
  
    def get_data_pointer(self,table,condition=None,return_fields=None,sort_arr=None):

        collection=self.__collection_pointer(table)
        condition,r_fields=self.__process_condition_return_fields(condition,return_fields)
        f=lambda t: ASCENDING if t=='asc' else DESCENDING
        if sort_arr:  
            sort_arr=[(el[0],f(el[1])) for el in sort_arr]
            res=collection.find(condition,r_fields).sort(sort_arr)  
        else:
            res=collection.find(condition,r_fields)  
        return res


    def get_data(self,table,condition=None,dataframe=True,return_fields=None,sort_arr=None):

        cursor=self.get_data_pointer(table,condition=condition,return_fields=return_fields) 
        res=[x for x in cursor]
        if dataframe:
            res=DataFrame(res)
        return res

    def get_element(self,table,column,value,return_fields=None,ext_condition=None):
        collection=self.__collection_pointer(table)
        r_fields={ "_id": False }
        if return_fields is not None:
            for field in return_fields:
                r_fields[field]=True
        condition={column:value}
        if ext_condition:
            condition.update(ext_condition)
        res=collection.find_one(condition,r_fields)
        return res

    def update_element(self,table,search_column,search_value,dict_with_new_values,operator='$set'):
        collection=self.__collection_pointer(table)
        collection.update_one({search_column:search_value},{operator:dict_with_new_values})      
        collection.update_one({search_column:search_value},{'$set':{'updated':datetime.datetime.now()}}) 

    def delete_element(self,table,search_column,search_value):
        collection=self.__collection_pointer(table)
        collection.delete_one({search_column:search_value})  

    def used_tables(self):
        return self.db.list_collection_names() 
    
    def look_up_tables(self,main_table,look_up_dict,dataframe=True,return_fields=None,condition=None,ignore_id=-1):
        collection=self.__collection_pointer(main_table)
        condition,r_fields=self.__process_condition_return_fields(condition,return_fields)
        hash_tab={}
        res=[]
        n=len(look_up_dict)
        for i in range(n):
            look_up_dict[i]['collection_pointer']=self.__collection_pointer(look_up_dict[i]['collection'])  
            r=[]
			
            for el in [[el2[0] for el2 in el[2] ]for el in look_up_dict[i]['match']]:
                r=r+el
      
            hash_tab[look_up_dict[i]['collection']]={ignore_id:{el:None for el in set(r)}}


        for row in collection.find(condition,r_fields):  
            for i in range(n):
                col=look_up_dict[i]['collection_pointer']
                for pair_ in look_up_dict[i]['match']:
                    search_id=row[pair_[0]]
                    col_name=look_up_dict[i]['collection']
                    try:
                        search_res=hash_tab[col_name][search_id]
                    except:
                        search_res=self.get_element(col_name,pair_[1],search_id)
                        hash_tab[col_name][search_id]=search_res
                    for el_ in pair_[2]:
                        row[el_[1]]=search_res[el_[0]]
                
            res.append(row)
          
        if dataframe:
            res=DataFrame(res)
        return res