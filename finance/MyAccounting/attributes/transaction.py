class transaction():
    __slots__ ='id_account_from','id_account_to','debet_from','value','trans_date','currency','description','document_id'
    def __init__(self,
                  id_account_from: int
                 ,id_account_to: int
                 ,trans_date
                 ,currency: int
                 ,debet_from: bool
                 ,value: float
                 ,document_id :int                  
                 ,description:str= None
                 ):
        self.id_account_from=id_account_from
        self.id_account_to=id_account_to
        self.debet_from=debet_from
        self.value=value
        self.currency=currency
        self.description=description
        self.document_id=document_id
        self.trans_date=trans_date
