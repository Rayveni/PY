import requests
from xml.etree import ElementTree
import datetime
class cb():
    __slots__='sources','text'
    def __init__(self):
        self.sources={'cb_russia':{'get_currency':'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_from}&date_req2={date_to}&VAL_NM_RQ={currency}',
                                  'currency_dict':r'http://www.cbr.ru/scripts/XML_val.asp?d=0',
                                  'currency_mapping':{'USD':'Доллар США','EUR':'Евро'},
                                  'date_format':("%d/%m/%Y","%d.%m.%Y")}
                     }

    def __get_element_by_text(self,text_xml,el_text):
        for child in ElementTree.fromstring(text_xml):
            for element in child.getiterator() :
              
                if element.text == el_text:
                    return child.attrib    
        return None         

    def __convert(self,dict_,date_format):
        dict_['Date']=datetime.datetime.strptime(dict_['Date'],date_format)
        dict_['Nominal']=int(dict_['Nominal'])
        dict_['Value']=float(dict_['Value'].replace(',','.'))
        return dict_
    
    def cb_russia_currency_hist(self,currency,date_from,date_to=None):
        currency_search=self.sources['cb_russia']['currency_mapping'][currency]
        return_message=(False,'Error')
    
        try:
            link=self.sources['cb_russia']['currency_dict']
            r=requests.get(link)
    
            if r.status_code==200:
                r= r.text
            else:
                return (False,'Error requeting {} , code {1}'.format(link,r.status_code))
            currency_id=self.__get_element_by_text(r,currency_search)['ID']
            date_format=self.sources['cb_russia']['date_format'][0]
            date_from =date_from.strftime(date_format)
            if date_to is None:
                date_to=datetime.datetime.now()
            date_to =date_to.strftime(date_format)    
            link =self.sources['cb_russia']['get_currency']    
            link=link.format(currency=currency_id,date_from=date_from,date_to=date_to)		
            r=requests.get(link)
            res=[]

            for child in ElementTree.fromstring(r.text):
                row={'Date':child.attrib['Date']} 
                for element in child.getiterator() :
                    key=element.tag
                    if key in ['Nominal','Value']:
                        row[key]=element.text

                res.append(row)
            date_format=self.sources['cb_russia']['date_format'][1]                
            map_f=lambda d:self.__convert(d,date_format)
            
            res=list(map(map_f,res))
            return_message=(True,res)
        except Exception as e: 
            return_message=(False,str(e))
   
        return return_message
    