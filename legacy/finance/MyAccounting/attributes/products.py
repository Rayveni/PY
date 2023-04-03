class products():
    __slots__ ='code','description','default_measure_id'
    def __init__(self,code :str,default_measure_id :id,description :str):
        self.code=code
        self.description=description
        self.default_measure_id=default_measure_id