# -*- coding: utf8 -*-

import datetime
import wget
from datetime import timedelta

now = datetime.datetime.now()
yesterday = datetime.datetime.now()-timedelta(days=1)
print('Beginning file download. Date is:'+now.strftime('%d.%m.%Y'))


url = 'https://raw.githubusercontent.com/semohr/risikogebiete_deutschland/master/assets/data/data_latest.csv'
wget.download(url, '/data/inzidenz'+now.strftime('%d.%m.%Y')+'.csv')

#from pandas import DataFrame, DatetimeIndex, read_csv, to_datetime, to_csv
#from datetime import timedelta
#import numpy as np
import pandas as  pd
import requests

datum = yesterday.strftime('%d.%m.%Y')

df_inzidenzen_Landkreise=pd.read_csv("https://raw.githubusercontent.com/semohr/risikogebiete_deutschland/master/assets/data/data_latest.csv")
df_inzidenzen_Landkreise['date']= datum
#print(df_inzidenzen_Landkreise)

df_Inzidenzen_Muenster=df_inzidenzen_Landkreise.loc[df_inzidenzen_Landkreise["Landreis ID"].isin([5515])]
#print(df_Inzidenzen_Muenster)

df_Inzidenzen_Muenster.to_csv('/data/inzidenzenMuenster.csv', encoding='utf-8', index=False, mode='a', header = False)
