class exchange_rate():
    __slots__ ='to_buy','to_sell','value','date','nominal'
    def __init__(self,to_buy :int,to_sell: int ,value,date,nominal: int):
        self.to_buy=to_buy
        self.to_sell=to_sell
        self.value=value
        self.nominal=nominal		
        self.date=date

