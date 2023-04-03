class bank_accounts():
    __slots__ ='customer_id','account','account_short_name','currency_id','expire_date'
    def __init__(self,customer_id :int,account :str,account_short_name :str,currency_id :int,expire_date=None):
        self.customer_id=customer_id
        self.account_short_name=account
        self.account=account_short_name		
        self.currency_id=currency_id
        self.expire_date=expire_date