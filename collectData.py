# -*- coding: utf8 -*-
#Collect Data
import datetime
#import wget
from datetime import timedelta
import os

now = datetime.datetime.now()
yesterday = datetime.datetime.now()-timedelta(days=1)
print('Beginning file download. Date is:'+now.strftime('%d.%m.%Y'))


#url = 'https://raw.githubusercontent.com/semohr/risikogebiete_deutschland/master/assets/data/data_latest.csv'
#wget.download(url, '/data/inzidenz'+now.strftime('%d.%m.%Y')+'.csv')

#from pandas import DataFrame, DatetimeIndex, read_csv, to_datetime, to_csv
#from datetime import timedelta
#import numpy as np
import pandas as  pd
import requests

datum = yesterday.strftime('%d.%m.%Y')

df_inzidenzen_Landkreise=pd.read_csv("https://raw.githubusercontent.com/semohr/risikogebiete_deutschland/master/assets/data/data_latest.csv")
df_inzidenzen_Landkreise.to_csv('data/inzidenz'+now.strftime('%d.%m.%Y')+'.csv', encoding='utf-8', index=False, header = True)
df_inzidenzen_Landkreise['date']= datum
#print(df_inzidenzen_Landkreise)

df_Inzidenzen_Muenster=df_inzidenzen_Landkreise.loc[df_inzidenzen_Landkreise["Landreis ID"].isin([5515])]
print(df_Inzidenzen_Muenster)

#df_Inzidenzen_Muenster.to_csv('/data/inzidenzenMuenster.csv', encoding='utf-8', index=False, mode='a', header = False)
#path = '/data'

files = os.listdir(path)

for f in files:
	print(f)

#build website
from pandas import DataFrame, DatetimeIndex, read_csv, to_datetime
from datetime import timedelta
import numpy as np
import altair as alt
import pandas as  pd
import requests
#import seaborn as sns
#alt.data_transformers.disable_max_rows()
#alt.renderers.enable('notebook')

df=pd.read_csv("data/inzidenzenMuenster.csv")
df['date'] =pd.to_datetime(df['date'], format='%d.%m.%Y')
df.set_index('date')
df.rename(columns = {'inzidenz':'Gesamtbevölkerung',
                     'inzidenz_A00-A04':'00 bis 04 Jahre',
                     'inzidenz_A05-A14':'05 bis 14 Jahre',
                     'inzidenz_A15-A34':'15 bis 34 Jahre',
                     'inzidenz_A35-A59':'35 bis 59 Jahre',
                     'inzidenz_A60-A79':'60 bis 79 Jahre',
                     'inzidenz_A80+':'> 80 Jahre',
                     'date':'Datum'
                    }, inplace = True)
df=df.round(decimals=2)

df_long=df.drop(['Landreis ID','weekly_cases','weekly_cases_A00-A04','weekly_cases_A05-A14','weekly_cases_A15-A34','weekly_cases_A35-A59','weekly_cases_A60-A79','weekly_cases_A80+','weekly_cases_unbekannt','inzidenz_unbekannt'], axis=1)

df_long=pd.melt(frame=df_long, id_vars="Datum", var_name='Altersgruppe', value_name='Wert')
df_long=df_long.sort_values('Datum', ascending=[True])

plot=alt.Chart(df_long).mark_rect().encode(
    #x='monthdate(Datum):O',
    alt.X('monthdate(Datum):O', title='Datum'),
    y='Altersgruppe:O',
    color='Wert:Q',
    tooltip=['Datum:T','Altersgruppe:O','Wert:Q',]
).properties(
    title='Inzidenzen in Münster aufgeschlüsselt nach Altergruppen'
)

text = plot.mark_text().encode(
    text='Wert:Q',
    color=alt.condition(
        alt.datum.Wert < 50,
        alt.value('black'),
        alt.value('white')
    )
)

#plot=plot+text
plot.save('website/Inzidenzen_Altergruppen.html')
