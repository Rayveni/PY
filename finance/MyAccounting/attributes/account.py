class accounts():
    __slots__ ='account_id','transaction_date','value_beg_c','value_end_c','amount_beg','amount_end','analyticts4','currency','prod_id','measure_id','value_beg_d','value_end_d','last_record','bank_account','customer_id','report_type'
    def __init__(self,account_id :int,transaction_date,value_beg_c,value_end_c,value_beg_d,value_end_d,
                 amount_beg,amount_end,currency,prod_id=None,measure_id=None,last_record :int=0,
                 bank_account :int=-1,customer_id :int=-1,report_type:str ='M',analyticts4 :str=None  ):
        self.account_id=account_id
        self.transaction_date=transaction_date
        
        self.value_beg_d=value_beg_d
        self.value_end_d=value_end_d
        self.value_beg_c=value_beg_c
        self.value_end_c=value_end_c
        
        self.amount_beg=amount_beg
        self.amount_end=amount_end
        
        self.currency=currency
        self.prod_id=prod_id
        self.measure_id=measure_id
        self.last_record=last_record
        
        self.bank_account=bank_account
        self.customer_id=customer_id
        self.report_type=report_type   
        self.analyticts4 =analyticts4
	
		