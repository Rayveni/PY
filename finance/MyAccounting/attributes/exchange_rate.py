class exchange_rate():
    __slots__ ='to_buy','description','to_sell','value','date'
    def __init__(self,to_buy :int,to_sell: int ,value,date):
        self.to_buy=to_buy
        self.to_sell=to_sell
        self.value=value
        self.date=date

