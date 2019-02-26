from os import walk
from  shutil import rmtree
import datetime
def run_scripts(acc):
    acc.drop_db()
    print('db dropped')
    acc.add_account('58','Финансовые вложения','Счет 58 «Финансовые вложения» предназначен для обобщения информации о наличии и движении инвестиций организации в государственные ценные бумаги, акции, облигации и иные ценные бумаги других организаций, уставные (складочные) капиталы других организаций, а также предоставленные другим организациям займы.')
    acc.add_account('58.1','паи и акции','На субсчете 58-1 "Паи и акции" учитываются наличие и движение инвестиций в акции акционерных обществ, уставные (складочные) капиталы других организаций и т.п.','58')
    acc.add_account('58.2','долговые ценные бумаги','На субсчете 58-2 "Долговые ценные бумаги" учитываются наличие и движение инвестиций в государственные и частные долговые ценные бумаги (облигации и др.).','58')
    acc.add_account('58.3','предоставленные займы','займы,депозиты и т.д.','58')
    acc.add_account('76','расчеты с разными дебиторами и кредиторами','Счет 76 "Расчеты с разными дебиторами и кредиторами" предназначен для обобщения информации о расчетах по операциям с дебиторами и кредиторами, не упомянутыми в пояснениях к счетам 60 - 75: по имущественному и личному страхованию; по претензиям; по суммам, удержанным из оплаты труда работников организации в пользу других организаций и отдельных лиц на основании исполнительных документов или постановлений судов, и др.')
    acc.add_account('91','прочие доходы и расходы','Счет 91 "Прочие доходы и расходы" предназначен для обобщения информации прочих доходов и расходов (операционных, внереализационных) отчетного периода, кроме чрезвычайных доходов и расходов.')
    acc.add_account('91.1','прочие доходы','На субсчете 91-1 "Прочие доходы" учитываются поступления активов, признаваемые прочими доходами (за исключением чрезвычайных).','91')
    acc.add_account('91.2','прочие расходы','На субсчете 91-2 "Прочие расходы" учитываются прочие расходы (за исключением чрезвычайных).','91')
    acc.add_account('91.9','сальдо прочих доходов и расходов','Субсчет 91-9 "Сальдо прочих доходов и расходов" предназначен для выявления сальдо прочих доходов и расходов за отчетный месяц.','91')
    acc.add_account('99','прибыли и убытки','Счет 99 "Прибыли и убытки" предназначен для обобщения информации о формировании конечного финансового результата деятельности организации в отчетном году.Конечный финансовый результат (чистая прибыль или чистый убыток) слагается из финансового результата от обычных видов деятельности, а также от прочих доходов и расходов, включая чрезвычайные. По дебету счета 99 "Прибыли и убытки" отражаются убытки (потери, расходы), а по кредиту - прибыли (доходы) организации. Сопоставление дебетового и кредитового оборота за отчетный период показывает конечный финансовый результат отчетного периода')
    acc.add_account('51','расчетные счета','Счет 51 "Расчетные счета" предназначен для обобщения информации о наличии и движении денежных средств в валюте Российской Федерации на расчетных счетах организации, открытых в кредитных организациях.По дебету счета 51 "Расчетные счета" отражается поступление денежных средств на расчетные счета организации. По кредиту счета 51 "Расчетные счета" отражается списание денежных средств с расчетных счетов организации. Суммы, ошибочно отнесенные в кредит или дебет расчетного счета организации и обнаруженные при проверке выписок кредитной организации, отражаются на счете 76 "Расчеты с разными дебиторами и кредиторами" (субсчет "Расчеты по претензиям").')
    acc.add_account('72','средства переданные и полученные','средства переданные и полученные')
    acc.add_account('72.1','вложение личных средств ИП','вложение личных средств ИП','72')
    acc.add_account('72.2','вывод в личные средства ИП','вывод в личные средства','72')
    acc.add_account('52','валютные счета','Счет 52 "Валютные счета" предназначен для обобщения информации о наличии и движении денежных средств в иностранных валютах на валютных счетах организации, открытых в кредитных организациях на территории Российской Федерации и за ее пределами.')
    acc.add_account('57','переводы в пути','Счет 57 "Переводы в пути" предназначен для обобщения информации о движении денежных средств (переводов) в валюте Российской Федерации и иностранных валютах в пути, т.е. денежных сумм (преимущественно выручка от продажи товаров организаций, осуществляющих торговую деятельность), внесенных в кассы кредитных организаций, сберегательные кассы или кассы почтовых отделений для зачисления на расчетный или иной счет организации, но еще не зачисленных по назначению.')
    print('счета созданы')
    acc.add_currency('RUR','₽','Российский рубль')
    acc.add_currency('USD','$','доллар США') 
    acc.add_currency('EUR','€','Евро') 
    print('Валюты добавлены')
    acc.add_measure('шт.','штук')
    acc.add_measure('л','литр')
    print('Добавлены единицы измерения')
    acc.add_customer('alfa_bank','Альфа-Банк')
    acc.add_customer('open_bank','Банк Открытие')
    acc.add_customer('open_broker','Открытие брокер')
    acc.add_customer('alpari','Альпари')
    print('Добавлены контрагенты')
    acc.add_bank_account('Альфа-Банк','40817978204430008255','Альфа-Банк(евро)','EUR')
    acc.add_bank_account('Альфа-Банк','40817840104430009301','Альфа-Банк(доллар)','USD')   
    acc.add_bank_account('Альфа-Банк','40817810504430040712','Альфа-Банк(зарплатный)','RUR') 
    acc.add_bank_account('Альфа-Банк','40817810004430041884','Альфа-Банк(накопилка)','RUR') 
    acc.add_bank_account('Альфа-Банк','42305840904430001349','Альфа-Банк(депозит доллар)','USD',datetime.datetime(2019,12,3)) 
    acc.add_bank_account('Альфа-Банк','42305978204430000378','Альфа-Банк(депозит евро)','EUR',datetime.datetime(2019,12,3)) 
    acc.add_bank_account('Альпари','USD12222691','Альпари ЛС','USD') 
    acc.add_bank_account('Альпари','4116565','Альпари FOX','USD') 
    acc.add_bank_account('Альпари','4066869','Альпари TARB-1','USD') 
    acc.add_bank_account('Открытие брокер','40701810700000000499','Открытие брокер(ЛС)','RUR')
    print('Добавлены лицевые счета')
    acc.invest_money(144100,datetime.datetime(2018,12,1),'Альфа-Банк(зарплатный)',document='Вложение личных средств для конвертации')
    acc.buy_currency('USD',1000,67500,'Альфа-Банк(зарплатный)','Альфа-Банк(депозит доллар)',datetime.datetime(2018,12,3),'Альфа-Банк')
    acc.buy_currency('EUR',1000,76600,'Альфа-Банк(зарплатный)','Альфа-Банк(депозит евро)',datetime.datetime(2018,12,3),'Альфа-Банк')
    acc.add_deposit(datetime.datetime(2018,12,3),'Альфа-Банк(доллар)','Альфа-Банк(депозит доллар)',1000)
    acc.add_deposit(datetime.datetime(2018,12,3),'Альфа-Банк(евро)','Альфа-Банк(депозит евро)',1000)	
	
    print('Добавлены депозиты евро/доллар')	
def del_pycache(CURRENT_DIR):
    for folder_path in [x[0] for x in walk(CURRENT_DIR) if '__pycache__'in x[0]]:
        rmtree(folder_path)