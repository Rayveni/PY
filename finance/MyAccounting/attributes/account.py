class account():
    __slots__ ='document_id','transaction_id','document_date'
    def __init__(self,document_id :int,transaction_id :int,document_date):
        self.document_id=document_id
        self.transaction_id=transaction_id
        self.document_date=document_date
		

