from os import path
from datetime import datetime,timedelta
import json
import pandas as pd
from trade.externaldata import smartlab,openbroker

class engine:
    def __init__(self,config_path,date_format='%Y-%m-%d'):
        self.config_filename=path.join(config_path,'trade_config.json')
        self.__load_config()
        self.date_format=date_format
        
    def __load_config(self):
        try:
            with open(self.config_filename) as f:
                data = json.load(f)
            self.config=data
        except:
            print('Error reading config file')
            
    def __date_from_str(self,str_date,date_format=None):
        if not date_format:
            date_format=self.date_format
        return datetime.strptime(str_date, date_format)


    def convert_str_to_float(self,string,replace_nan=None):
        
        if replace_nan is  not None and pd.isna(string):		
            res=replace_nan
        elif isinstance(string,int):
            res=float(string) 
        elif isinstance(string,float):
            res=string
        else:
            res=float(string.encode('ascii','ignore').decode('utf-8').replace(',','.'))			
        return res
		
    def __date_interval_from_str(self,date_from:str=None,date_to:str=None):
        now=datetime.now()
        if date_from is None:
            date_from=now
        else:
            date_from=self.__date_from_str(date_from)
        if date_to is None:
            date_to=now+timedelta(days=36525)
        else:
            date_to=self.__date_from_str(date_to)
        return date_from,date_to


    def bond_analysis_from_quik(self,file_path,date_from:str=None,date_to:str=None):
        df=pd.read_excel(file_path)	
        date_from,date_to=self.__date_interval_from_str(date_from,date_to)		
        df['Погашение']=  pd.to_datetime(df['Погашение'])
        df['Предл.']= df['Предл.'].apply(lambda s:self.convert_str_to_float(s,0))
        df=df[(df['Погашение']>date_from) & (df['Погашение']<date_to)& (df['Предл.']>=0)]#.reset_index(drop=True)
        df['Доходность']= df['Доходность'].apply(lambda s:self.convert_str_to_float(s,0)) 

        df['Доход.пред.оц.']= df['Доход.пред.оц.'].apply(lambda s:self.convert_str_to_float(s,0))
        df['Доходность сводная']= df[['Доход.пред.оц.','Доходность']].apply(lambda row:0 if row[1]+row[0]==0 else min([el for el in [row[1],row[0]] if el>0]),axis=1)
        df.sort_values(by='Доходность сводная',ascending=True,inplace=True)      
        df.drop('Доходность сводная',axis=1,inplace=True)  		
        return df.reset_index(drop=True) 
		
    def smartlab_bonds(self,bonds_list:list=[],date_from:str=None,date_to:str=None,
                       sort_values:bool=False,profit_limit:float=100.,no_oferta:bool=False):
        sl=smartlab()
        bonds=sl.bonds_info(bonds_list)
		
        if date_from is None and date_to is None :
            pass
        else:
            date_from,date_to=self.__date_interval_from_str(date_from,date_to)
            for currency in bonds.keys():
                df=bonds[currency]
                bonds[currency]=df[(df['Погашение']>=date_from) & (df['Погашение']<=date_to)].reset_index(drop=True)
                  
        for currency in bonds.keys():
            df=bonds[currency]

            if sort_values:
                df.sort_values(by=['bond_category','Доходн'],ascending=[True,False],inplace=True)
			
            if profit_limit>0:
                df=df[df['Доходн']<profit_limit]   

            if no_oferta:		
                df=df[~df['Оферта'].notnull()]    
     

            try:
                columns=list(df.columns)
                duraction,oferta='Дюр-я, лет','Оферта'
                columns.remove(duraction)
                columns.insert(columns.index('Доходн')+1,duraction)
                columns.remove(oferta)
                columns.insert(columns.index('Погашение')+1,oferta)
                df=df[columns]
            except:pass
            bonds[currency]=df
		
        return bonds
		
    def openbroker(self,file_path):
        return openbroker(file_path)		