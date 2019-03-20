import datetime
from pymongo import MongoClient,DESCENDING,ASCENDING
from pandas import DataFrame

class MongoDriver:
    __slots__ ='config'
    def __init__(self,config: dict):
        self.config=config
   
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
          
        
    def drop_db(self):
        self.__client.drop_database(self.db.name)
        self.__add_indexes()
        self.__get_id_dict()
         