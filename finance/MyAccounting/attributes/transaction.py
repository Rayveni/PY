class transaction():
    __slots__ ='id_account_from','id_account_to','debet_from','value','amount','analytic1','analytic2','analytic3','analytic4','trans_id','trans_date'
    def __init__(self,
                  id_account_from: int
                 ,id_account_to: int
                 ,trans_date
                 ,debet_from: bool
                 ,value: float
                 ,amount: float
                 ,analytic1: str=None
                 ,analytic2: str=None
                 ,analytic3: str=None
                 ,analytic4: str=None):
        self.id_account_from=id_account_from
        self.id_account_to=id_account_to
        self.debet_from=debet_from
        self.value=value
        self.amount=amount
        self.analytic1=analytic1
        self.analytic2=analytic2
        self.analytic3=analytic3
        self.analytic4=analytic4
  