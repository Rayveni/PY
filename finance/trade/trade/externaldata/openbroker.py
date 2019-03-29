from xlrd import open_workbook
from operator import itemgetter
import pandas as pd

class openbroker:
    __slots__ ='data_sheet','reports','default_symb'
    def __init__(self,file_path):
        self.default_symb:str=''
        self.data_sheet=open_workbook(file_path).sheet_by_name('broker_report')
        self.__get_reports()

    def __get_reports(self):
        report_mask:list=[self.default_symb]*(self.data_sheet.ncols-1)
        empty_row:list=[self.default_symb]*self.data_sheet.ncols

        start_row:int=-1  
        self.reports:dict={}
        for i in range(self.data_sheet.nrows):
            row=self.data_sheet.row_values(i)
            if row[1:]==report_mask and row[0]!=self.default_symb and (start_row==-1 or dict_key==self.default_symb):
                if i>start_row-1 :
                    start_row=i
                    dict_key=row[0].strip()
            if row==empty_row and dict_key!=self.default_symb:
                self.reports[dict_key]=(start_row+1,i)
                start_row=i
                dict_key=self.default_symb   
                
    def __nonempty_columns(self,header_id):
        return [i for i, e in enumerate(self.data_sheet.row_values(header_id)) if e != self.default_symb]
    
    def __process_table(self,rows_rng:tuple,columns_ids):
        #columns=self.__nonempty_columns(rows_rng[0])
        return [itemgetter(*columns_ids)(self.data_sheet.row_values(i)) for i in range(*rows_rng)]

    def __shift_columns(self,columns_dict:dict,header_id):
        first_row=self.data_sheet.row_values(header_id)
        column_names=[]
        column_indexes=[]
        for key,value in columns_dict.items():
            ind=first_row.index(key)
            suffix=0
            for elem in value['shift_col']:
                column_indexes.append(ind+elem)
                
                if suffix>0:
                    column_names.append(key+str(suffix)) 
                else:
                    column_names.append(key) 
                suffix+=1  
        return column_names,column_indexes
    
    def current_assets(self):
        report_name='Активы клиента (ценные бумаги и денежные средства) - Предварительное закрытие дня'
        columns={'Инструмент':{'shift_col':[0,1]},
                 'Активы на конец периода':{'shift_col':[0]},
                 'Оценка остатка (факт) по цене последней сделки, руб. (по Центральному курсу)':{'shift_col':[-1]} ,
                 'НКД на конец периода, руб. (по Центральному курсу)':{'shift_col':[-1]}      
                }

        report=self.reports[report_name]  
        column_names,column_indexes=self.__shift_columns(columns,report[0])

        array=self.__process_table(report,column_indexes)
        df=   pd.DataFrame(array[2:],columns=column_names)[['Инструмент', 
                                                           'Инструмент1', 
                                                           'Активы на конец периода',
                                                           'Оценка остатка (факт) по цене последней сделки, руб. (по Центральному курсу)',
                                                           'НКД на конец периода, руб. (по Центральному курсу)']]
        df.columns=['category','security','amount','rur_amount','НКД']
        category=list(df.category)
        filled_category=[]
        for  element in category:
            if element==self.default_symb:
                filled_category.append(filled_category[-1])
            else:
                filled_category.append(element)
   
    
        df['category']=filled_category
        df=df[(df.security!=self.default_symb)].reset_index(drop=True)
       
        return self.__add_tiker(df,'security')
 
    def __add_tiker(self,data,merge_column:str):
        sec_dict=self.security_dict()[['Инструмент','Тикер']]
        sec_dict.columns=['sec_from_dict','Тикер']
        merge_df=pd.merge(sec_dict,data,left_on=['sec_from_dict'],right_on=[merge_column],how='right')
        return merge_df.drop(['sec_from_dict'],axis=1)
    
    def security_dict(self):
        report_name='Справочник финансовых инструментов'
        report=self.reports[report_name]  
        columns=self.__nonempty_columns(report[0])
        array=self.__process_table(report,columns)

        return pd.DataFrame(array[1:],columns=array[0])
    
    def deals(self):
        report_name='Заключенные в отчетном периоде сделки купли/продажи с ценными бумагами'     
        columns={'Инструмент':{'shift_col':[1]},                 
                 'Дата\nзаключения':{'shift_col':[0]},
                 'Время заключения':{'shift_col':[0]},
                 'Куплено,\nшт.':{'shift_col':[0]},
                 'Продано,\nшт.':{'shift_col':[0]},
                 'Валюта цены (номинала для облигаций)':{'shift_col':[0]},
                 'Цена сделки\n(% для\nоблигаций)':{'shift_col':[0]},
                 'Валюта\nрасчетов':{'shift_col':[0]},
                 'Объем сделки\nв валюте\nрасчетов':{'shift_col':[0]}, 
                 'НКД \nпо сделке в валюте расчетов':{'shift_col':[0]},
                 'Комиссия Брокера/Доп. комиссия Брокера "Сборы ТС"':{'shift_col':[0]},
                 'Валюта комиссии Брокера':{'shift_col':[0]}
        }

        report=self.reports[report_name]  
        column_names,column_indexes=self.__shift_columns(columns,report[0])

        array=self.__process_table(report,column_indexes)
        df=pd.DataFrame(array[1:],columns=column_names)
        df=df[df['Инструмент']!=self.default_symb].reset_index(drop=True)
        return self.__add_tiker(df,'Инструмент')