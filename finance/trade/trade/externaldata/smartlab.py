import requests
import pandas as pd
import lxml.html as lh
from collections import Counter
#import datetime
#from lxml import etree
#print(etree.tostring(tr_elements[-1][2], pretty_print=True))
class smartlab:
    __slots__='sources','link','http_headers'
    def __init__(self):
        self.link:str=r'https://smart-lab.ru'
        self.sources:dict={'bonds':{'ОФЗ':{'link':r'/q/ofz/','currency':'RUR'},
                               'Муниципальные':{'link':r'/q/subfed/','currency':'RUR'},
                               'Корпоративные':{'link':r'/q/bonds/','currency':'RUR'},
                               'Еврооблигации':{'link':r'/q/eurobonds/','currency':'USD'}
                              }
                     }
        self.http_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    def __table_from_html(self,url:str,extra_fields_dict:dict=None):
        mask="Unnamed: {}"
        """
        extra_fields_dict={field_text_val:[{'add_column_name':0,'xpath_text':"a/@href",'insert_position':0}]}
        """
        page=requests.get(url,headers=self.http_headers)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        header=[h.text_content() for h in tr_elements[0]]
        ununique_columns=[ key for key,value in Counter(header).items() if value>1]
        if len(ununique_columns)>0:
            for i in range(len(header)):
                if header[i] in ununique_columns:
                    header[i]=mask.format(i)
                
        if extra_fields_dict:
            keys= list(extra_fields_dict.keys())
            for key in keys:
                value=extra_fields_dict[key]

                extra_fields_dict[header.index(key)]=extra_fields_dict.pop(key)
                for condition in value:
                    header.insert(condition['insert_position'],condition['add_column_name'])

        res=[]

        for row in tr_elements[1:]:
            arr=[el.text_content() for el in row]
            if extra_fields_dict:
                for key,value in extra_fields_dict.items():
                    xml_element=row[key]
                    for condition in value:
                        arr.insert(condition['insert_position'],xml_element.xpath(condition['xpath_text']))

            res.append(arr)
        return  pd.DataFrame(res,columns=header)            
            
            
            
            
    def bonds_info(self,bonds_list:list=[])->dict:
        bonds_dict=self.sources['bonds']
        if len(bonds_list)==0:
            bonds_list=list(bonds_dict.keys())
            
        res={}
        currency_set=set([])
        for bond_group in bonds_list:
            info=bonds_dict[bond_group]
            url,currency=self.link+info['link'],info['currency']
            if currency not in currency_set:
                currency_set.add(currency)
                res.setdefault(currency,[])
            #df=pd.read_html(url, header=0)[0]
            tiker='Тикер'
            extra_fields_dict={'Имя':[{'add_column_name':tiker
                                       ,'xpath_text':"a/@href"
                                       ,'insert_position':1
                                      } 
                                     ]}           
            df=self.__table_from_html(url,extra_fields_dict=extra_fields_dict)
     
            df[tiker]=df[tiker].apply(lambda t:t[0].split('/')[-2])
            df.insert(0, 'bond_category', bond_group)
            if bond_group=='ОФЗ':          
                df.rename(columns={'!': 'Тип ОФЗ'},inplace=True)
                
            res[currency]+=[df]

        res={ currency:pd.concat(res[currency],axis=0, sort=False) for currency in currency_set}
        percents_str_to_float=lambda s:float(s.replace('%','').replace(' ',''))
        str_to_date=lambda t:pd.to_datetime(t, format='%Y-%m-%d')#, errors='ignore')
        
        for currency in currency_set:
            df=res[currency]
            drop_columns= [column for column in df.columns if 'Unnamed' in column]
            drop_columns.append('№')
            df.drop(drop_columns,axis=1,inplace=True)
            df['Доходн']=df['Доходн'].apply(lambda s:percents_str_to_float(s))
            df['Погашение']=df['Погашение'].apply(lambda s:str_to_date(s))
            df['Оферта']=df['Оферта'].apply(lambda s:str_to_date(s))			
            try:
                df['Тип ОФЗ'].fillna('',inplace=True)                
            except:
                pass
        return res