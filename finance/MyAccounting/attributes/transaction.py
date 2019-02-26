class transaction():
    __slots__ ='id_account_from','id_account_to','debet_from','value','trans_date','currency','analyticts4_from','analyticts4_to','description','document_id','product_id','amount','is_currency','bank_acc_from','customer_id_from','bank_acc_to','customer_id_to','measure_id'
    def __init__(self,
                  id_account_from: int
                 ,id_account_to: int
                 ,trans_date
                 ,currency: int
                 ,debet_from: bool
                 ,value: float
                 ,document_id :int                  
                 ,description:str= None
                 ,product_id : int=None
                 ,amount :float =None
                 ,is_currency: bool=None
                 ,bank_acc_from :int=None
                 ,customer_id_from :int=None
                 ,bank_acc_to :int=None
                 ,customer_id_to :int=None   
                 ,measure_id :int=None 
                 ,analyticts4_from :str=None 
                 ,analyticts4_to :str=None 				 
                 ):
        self.id_account_from=id_account_from
        self.id_account_to=id_account_to
        self.debet_from=debet_from
        self.value=value
        self.currency=currency
        self.description=description
        self.document_id=document_id
        self.trans_date=trans_date
        self.product_id=product_id
        self.amount=amount
        self.is_currency=is_currency
        
        self.bank_acc_from =bank_acc_from
        self.customer_id_from =customer_id_from

        self.bank_acc_to =bank_acc_to
        self.customer_id_to =customer_id_to

        self.measure_id =measure_id
        self.analyticts4_from =analyticts4_from
        self.analyticts4_to =analyticts4_to		