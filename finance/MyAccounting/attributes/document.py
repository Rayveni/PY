class document():
    __slots__ ='document_descr','date','customer_id'
    def __init__(self,document_descr :str,date,customer_id: int=None):
        self.document_descr=document_descr
        self.date=date 
        self.customer_id=customer_id
 