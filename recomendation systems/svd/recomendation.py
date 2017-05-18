import numpy as np
class SvdDecomposition:
    """
    expected sorted input file with ordered columns :userid,itemid,score
    """
    def __init__(self, data, n_users,n_items):
        self.n_users = n_users
        self.n_items = n_items
        # get average scores
        self.avg_score =data.score.mean() 
        '''to speed up one element selection , using native python lists'''    
        self.train_data=data[['userid','itemid','score']].values.tolist()
        self.epoch_count=0
    def default_trunc_score_rule(self,p):
        if p > 5:p = 5
        elif p < 1:p = 1
        return p
        
    def train_ratings(self,algorithm='default' ,rank=30, lrate=0.035,alpha=0,regularizer=0.01,
                      stop_criteria = 0.001,n_iterations = 30,
                      trunc_score_rule='default',early_stop=False,minibatch_size=0.1,warm_start=False,print_steps=False): 
        
        
        # set initial values in U, V using square root of average/rank
        if self.epoch_count>0 and warm_start:
            pass
        else:
            init_val=np.sqrt(self.avg_score/rank)
            # U matrix
            self.U=np.ones((self.n_users,rank))*init_val
            # V matrix -- easier to store and compute than V^T
            self.V = np.ones((self.n_items,rank))*init_val
        '''setting truncation rule for scores,e.g  0.23->1,5.33->5,etc '''
        if trunc_score_rule=='default':
            self.trunc_score_rule=self.default_trunc_score_rule
        elif trunc_score_rule==None:
            self.trunc_score_rule=lambda p:p
        else:self.trunc_score_rule=trunc_score_rule  
            
        self.data_size=len(self.train_data)
        if algorithm=='default':
            train_method=self.__gradient_descent_train
        elif algorithm=='minibatch':
            train_method=self.__minibatch_train
            if minibatch_size<1:
                   self.minibatch_size = int(self.data_size*minibatch_size)
            else:self.minibatch_size=minibatch_size
            print('minibatch_size=',self.minibatch_size)


        flg=False
        # stub -- initial train error
        oldtrain_err = 1000000       
        
        for k in range(rank):
            if print_steps:print ("k=", k)
            learn_rate=lrate
            for iteration in range(n_iterations):
                
                train_err = train_method(k,self.train_data,learn_rate,regularizer)

                if print_steps:print ("iteration=", iteration, "; train_err=", train_err)               
                # check if train error is still changing
                if abs(oldtrain_err-train_err) < stop_criteria:
                    max_rank=k
                    if  algorithm=='default':
                        if iteration==0 and early_stop :flg=True 
                        break

                if oldtrain_err>train_err :
                    learn_rate=learn_rate/(1+alpha) 
                else:learn_rate=learn_rate*(1+alpha) 
                oldtrain_err = train_err
            if flg:break
        self.epoch_count+=1
        print('max_rank=',max_rank+1)
        
        
    def __minibatch_train(self, k,train_data,lrate,regularizer):
        n=self.minibatch_size
        rows_indexes=np.random.choice(range(self.data_size), n,replace=False)
        return self.__descent_train_iteration( k,train_data,lrate,regularizer,n,rows_indexes) 

    def __gradient_descent_train(self, k,train_data,lrate,regularizer):
        n = self.data_size
        rows_indexes=range(n)
        return self.__descent_train_iteration(k,train_data,lrate,regularizer,n,rows_indexes)

    
    def __descent_train_iteration(self, k,train_data,lrate,regularizer,batch_size,id_rows_generator):
        sse = 0.0
        for i in id_rows_generator:
            # get current score
            row_user_id,row_item_id,row_score=train_data[i]
            err =row_score -self.calc_score(row_user_id,row_item_id)
            #print(err-err_arr[i])
            sse += err**2
            uTemp = self.U[row_user_id,k]
            vTemp = self.V[row_item_id,k]
            self.U[row_user_id,k] += lrate * (err*vTemp - regularizer*uTemp)
            self.V[row_item_id,k] += lrate * (err*uTemp - regularizer*vTemp)
        return np.sqrt(sse/batch_size)  

    def calc_score(self, user_id, item_id):
        """
        Returns the estimated rating corresponding to userid for itemid
        Ensures returns rating is in range [1,5]
        """     
        p = np.dot(self.U[user_id], self.V[item_id])
        if self.trunc_score_rule==None:pass
        else: p=self.trunc_score_rule(p)
    
        return p

    def calc_rmse(self, data):
        """
        Calculates the RMSE using between arr
        and the estimated values in (U * V^T)
        """
        res= data.score- data[['userid','itemid']].apply(lambda row:self.calc_score(row[0], row[1]),axis=1)
        res=[el**2 for el in np.array(res)]
        return np.sqrt(np.sum(res)/data.shape[0])
    def predict_score(self,df):
        df.copy(deep=True)
        df['predicted_score']=df[['userid','itemid']].apply(lambda row:self.calc_score(row[0], row[1]),axis=1)
        return data