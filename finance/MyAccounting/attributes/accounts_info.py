class accounts_info():
    __slots__ ='account_number','account_descr_short','account_descr_long','account_parrent'
    def __init__(self,account_number :str,account_descr_short :str,account_descr_long :str,account_parrent:int =None):
        self.account_number=account_number
        self.account_descr_short=account_descr_short
        self.account_descr_long=account_descr_long
        self.account_parrent=account_parrent
		

