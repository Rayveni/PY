class config():
    __slots__ ='data'
    def __init__(self,driver:str,db_name: str,variables: str,accounts_info :str 
                 ,accounts: str ,documents: str,transactions: str,exchange_rate: str,currency :str,schema_name=None,host=None,port=None):
        self.data={}
        flg=True
        for input_var in (driver,db_name,accounts_info,accounts,documents,transactions,variables):
            if len(input_var) ==0:
                print('Error:input_var lenth=0')
                break
        if flg:

            self.data['driver']=driver
            self.data['host']=host
            self.data['port']=port
            self.data['schema_name']=schema_name
            self.data['db_name']=db_name
            self.data['accounts_info']=accounts_info
            self.data['accounts']=accounts
            self.data['documents']=documents
            self.data['transactions']=transactions
            self.data['variables']=variables
            self.data['currency']=currency
            self.data['exchange_rate']=exchange_rate