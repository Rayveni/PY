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
        
        self.config={'currency': config['currency'],'exchange_rate': config['exchange_rate']}
        self.__add_indexes()
        self.__get_id_dict()
        
        self.mapping={'accounts_info':['account_id'],
                      'accounts':[None],
                      'documents':['document_id'],
                      'transactions':['trans_id'],
                      'currency':['currency_id'],
                      'exchange_rate':['exchange_rate_id']
                     }
        
    def __add_indexes(self) :
        if self.variables.find_one() is None:
            self.accounts.create_index([("document_date", ASCENDING),("document_id", ASCENDING)],unique=True)
            self.accounts_info.create_index([("account_number", ASCENDING)],unique=True)
            self.documents.create_index([("document_id", ASCENDING), ("date", ASCENDING)],unique=True)
            self.transactions.create_index([("'trans_id", ASCENDING), ("trans_date", ASCENDING)],unique=True)
            self.variables.create_index([("var", DESCENDING)],unique=True)
            self.db[self.config['currency']].create_index([("code", DESCENDING)],unique=True)
            self.db[self.config['exchange_rate']].create_index([("date", DESCENDING),("to_buy", DESCENDING),("to_sell", DESCENDING)],unique=True)			

    def __get_id_dict(self):
        res=self.variables.find_one({'var':'id_dict'})
        if res is None:
            dict_trn={'document_id':0,'account_id':0,'document_id':0,'trans_id':0}
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

    def __max_id(self,collection, column)-> int:
        res=collection.find_one({},sort=[(column,DESCENDING)])
        if res is None:
            res=-1
        else:
            res=res[column]
        return res
   
    def __collection_pointer(self,table):
        try:
            collection=getattr(self,table)
        except:
            collection=self.db[self.config[table]]
        return collection
    
    def add_row(self,operation_type,obj,creation_date=None,rare_operation=False)->str:
        res={key:getattr(obj, key) for key in obj.__slots__}
        attr=self.mapping[operation_type][0]
        return_message=(True,'Ok')
        
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
        except Exception as e: 
            return_message=(False,str(e))
        return return_message
        
    def get_data(self,table,condition=None,dataframe=True):

        collection=self.__collection_pointer(table)
        res=[x for x in collection.find({},{ "_id": False })]
        if dataframe:
            res=DataFrame(res)
        return res

    def get_element(self,table,column,value):
        collection=self.__collection_pointer(table)
        res=collection.find_one({column:value})
        return res

    def update_element(self,table,search_column,search_value,dict_with_new_values):
        collection=self.__collection_pointer(table)
        collection.update_one({search_column:search_value},{'$set':dict_with_new_values})  	

    def delete_element(self,table,search_column,search_value):
        collection=self.__collection_pointer(table)
        collection.delete_one({search_column:search_value})  