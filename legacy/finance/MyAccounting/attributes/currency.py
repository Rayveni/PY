class currency():
    __slots__ ='code','symbol','description'
    def __init__(self,code :str,symbol :str,description :str):
        self.code=code
        self.symbol=symbol		
        self.description=description
