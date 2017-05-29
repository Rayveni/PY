from os import makedirs,path,mkdir,listdir
import datetime
import pickle
import json
import time
import pandas as pd
from sklearn import model_selection,metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns

class ML_competitions:
    def __init__(self,projectdirectory):
        try:
            makedirs(projectdirectory)
        except:pass
        self.project_dir=projectdirectory
        try:
            makedirs(path.join(self.project_dir,'save'))
        except:pass
        self.project_save=path.join(self.project_dir,'save')
    def load_data(self,X_train,y_train,X_test):
        self.X_train=X_train
        self.y_train=y_train
        self.X_test=X_test
        self.X_merged=pd.concat([X_train,X_test],axis=0).reset_index(drop=True)		
    def transform(self,f_transfrom=None):
        X=self.X_train
        y=self.y_train
        X_test=self.X_test
        if f_transfrom!=None:
            X_merged=pd.concat([X,X_test],axis=0).reset_index(drop=True)
            X_merged=f_transfrom(X_merged)
            X=X_merged.ix[:X.shape[0]-1]
            X_test=X_merged.ix[X.shape[0]:].reset_index(drop=True)
        print(X_test.shape)
        return X,y,X_test		
	
		
    def save_cv(self,cv,name='cv'):
        try:
            makedirs(path.join(self.project_dir,'pickle'))
        except:pass	
        with open(path.join(self.project_dir,'pickle',name), 'wb') as f:
            pickle.dump(cv, f) 
        self.cv=cv
    def load_cv(self,name='cv'):
        with open(path.join(self.project_dir,'pickle',name), 'rb') as f:
            res = pickle.load(f) 
        self.cv=res
        return res
    def add_experiment(self,model,scoring,f_transform=None,comment='default_params'):
        x_train,y_train,x_test=self.transform(f_transform)
        start = time.time()
        cur_time=datetime.datetime.now().isoformat().split('.')[0]
        scores=model_selection.cross_val_score(model,x_train,y_train,cv=self.cv,scoring=scoring)
        midle = time.time()
        folder=path.join(self.project_save,datetime.datetime.now().isoformat().replace(':','_').split('.')[0])
        
        mkdir(folder)
        
 
        model.fit(x_train,y_train)
        y_pred=model.predict(x_test)
        end = time.time()

        try:
            save_dict=model.get_params()
            save_dict['model_name']=str(model).split('(')[0]
        except:
            save_dict={'model_name':'custom_model'}
        save_dict['cv_time']=midle-start
        save_dict['model_time']=end-midle
        save_dict['date_created']=cur_time		
        save_dict['cv_score_mean']=scores.mean()	
        save_dict['cv_score_std']=scores.std()	
        save_dict['comment']=comment		
        with open(path.join(folder,'params.json'), "w")  as f:
            json.dump(save_dict, f)
        with open(path.join(folder,'public.txt'), "w")  as f:
            pass
			
			
        with open(path.join(folder,'y_test.txt'), "w")  as f:
            f.write("\n".join(list(map(str,y_pred))))

    def get_statistics(self,project_path='default'):
  
        if project_path=='default':project_path= self.project_save
        folders=listdir(project_path)

        res=[]
        for folder in folders:
            with open(path.join(project_path,folder,'params.json'),'r') as data_file:    
                data = json.load(data_file)
            with open(path.join(project_path,folder,'public.txt'), "r")  as f:
                public_score=f.read()		
            
            df=pd.DataFrame([list(data.values())],columns=list(data.keys()))
            df['public_score']=public_score
            res.append(df)
        return pd.concat(res)
def ex_describe(X):
    unique_count=[X[col].nunique() for col  in X.columns]
    res=pd.concat([X.describe(),pd.DataFrame([unique_count],columns=X.columns,index=['unique_count'])],axis=0)
    return res
def oversampling(X,y):
    X_merged=X.copy(deep=True)
    X_merged['target']=y
    unique_items, counts = np.unique(y, return_counts=True)
    max_count=np.max(counts)
    
    unique_items=list(zip(unique_items,counts))
    print('uniqe items counts',unique_items)
    add_df=[X_merged[X_merged.target==el[0]].sample(max_count-el[1],replace=True) for el in unique_items if el[1]<max_count]
    add_df=pd.concat(add_df+[X_merged],axis=0).reset_index(drop=True)
    return add_df.drop('target',axis=1),np.array(a.target)	

def forest_feature_importance(X,y,n_trees=200,fig_size=(20,10)):
    res=[]
    forest = RandomForestClassifier(n_estimators=n_trees)
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)  
    indices = np.argsort(importances)[::-1]
    
    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
        res.append([indices[f], importances[indices[f]],std[indices[f]]])

    # Plot the feature importances of the forest
    plt.figure(figsize=fig_size)
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()	
    return res
	
def pairplot(data,hue=None,hue_y=None):
    data.is_a_copy=False
    if hue_y is not None: 
        data['target']=hue_y
        hue='target'
    sns.pairplot(data,hue=hue)

def single_feature_visualisation(y_data,fig_size=(12,8),y_label='',font_size=12,n_bins=50,sup_title='',transform=(None,None)):
    plt.figure(figsize=fig_size)
    
    ax1=plt.subplot(221)
    ax1.scatter(range(len(y_data)), np.sort(y_data))
    ax1.set_ylabel(y_label, fontsize=font_size)
    ax1.axes.get_xaxis().set_ticks([])

    ax2=plt.subplot(222)
    sns.boxplot(y_data,ax=ax2)
    ax2.set_xlabel(y_label)

    ax3=plt.subplot(212)
    if transform!=(None,None ):
        y_trans=transform[0](y_data)
        ax3.set_title(transform[1])
        sns.distplot(y_trans, bins=n_bins, kde=True,ax=ax3)
    else:sns.distplot(y_data, bins=n_bins, kde=True,ax=ax3)
    ax3.set_xlabel(y_label)
    plt.suptitle(sup_title, fontsize=font_size+2)