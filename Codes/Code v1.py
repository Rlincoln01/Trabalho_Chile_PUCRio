#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 09:09:15 2022

@author: rafaellincoln
"""



# Pacotes a serem utilizados

import pandas as pd
import requests
from bs4 import BeautifulSoup  
import re
from tqdm import tqdm
from sqlalchemy import create_engine
import datetime as dt

# Libraries for plotting
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# =============================================================================
# Funções definidas para fazer web-scraping
# =============================================================================



# Useful for converting 1k = 1000, for example
def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

# Function for web-scraping
def get_hashtags_at_date_hour(date,city):
    '''
    date: datetime format
    hour: string from 0-23
    '''
    hour = date.hour
    
    day = date.strftime('%Y-%m-%d')

    link = f'https://getdaytrends.com/united-states/{city}/{day}/{hour}/'
    
    response = requests.get(link, headers=headers)

    soup = BeautifulSoup(re.sub('\s+(?=<)','',response.text),'lxml') # Grabs all html info from page
    
    
    # Getting all hashtags at a current hour and date
    href_tags = soup.findAll(href=True)
    
    values = [value.text for value in soup.findAll('span', {'class':'small text-muted'})]
    
    top_len = len(values)
    
    hashtags = [tag.text for tag in href_tags if '/fr/chile/trend/' in tag['href']][:top_len]

    #Assemble Dataframe
    df = pd.DataFrame({'hashtags':hashtags,
                  'Values':values})\
        .replace(['Moins de ',' tweets'],'', regex=True)\
            .assign(dates = lambda x: date)
        
    df['Values'] = df['Values'].apply(lambda x: convert_str_to_number(x))
    
    return df



headers = {
    'authority': 'getdaytrends.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,pt;q=0.8,fr;q=0.7',
    'cookie': '__cfduid=d6d5d1db2e9559eed65aa8ec8281ecf0e1606661256; sessionid=e9zlx7lqvlum1s5vgfepam42rv9akls3',
}


# =============================================================================
# Data wrangling
# =============================================================================

data_violence = pd.read_excel('/Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Dados violência.xlsx',
                              header = 2,
                              index_col = 1).dropna(
                                  axis = 1,how= 'all')

engine = create_engine('sqlite:////Users/rafaellincoln/Desktop/Sciences Po/Le prix de la démocratie/chile.db')


filepath = '/Users/rafaellincoln/Desktop/Sciences Po/Le prix de la démocratie/Hashtags.xlsx'


dates = pd.date_range(start = '10/1/2019',end = '11/30/2019', freq = 'H')


# Hashtags of political background database
df_pol = pd.read_excel(filepath, sheet_name = 'DF')\
            .drop_duplicates()

# Reads databse from SQL and tidies data (below)
db = pd.read_sql('twitter trends chile',engine)


lista = [1 if '#' in text else 0 for text in db.hashtags]

db = db.assign(is_hashtag = lambda x: lista)


db = db.merge(df_pol,on = 'hashtags',how = 'outer',sort = False).sort_values('dates')

# Rolling 24 hour average of the volume of tweets in TT & political index as % of TT hashtags
ind1 = db.groupby(['dates']).sum()\
    .assign(pol_pct = lambda x: 100*(x.pol_dummy/x.is_hashtag))\
        .rolling(24).mean().dropna()

# Significant dates for protests


dates_protest = [(dt.datetime(2019,10,14,0),dt.datetime(2019,10,14,23)),
                     (dt.datetime(2019,10,18,0),dt.datetime(2019,10,20,23)),
                     (dt.datetime(2019,10,25,0),dt.datetime(2019,10,25,23)),
                     (dt.datetime(2019,10,30,0),dt.datetime(2019,10,30,23)),
                     (dt.datetime(2019,11,10,0),dt.datetime(2019,11,10,23)),
                     (dt.datetime(2019,11,15,0),dt.datetime(2019,11,15,23)),
                     (dt.datetime(2019,11,19,0),dt.datetime(2019,11,19,23)),
                     (dt.datetime(2019,11,22,0),dt.datetime(2019,11,24,23))]


dates_protest = [(dt.datetime(2019,10,14,0),dt.datetime(2019,10,14,23)),
                     (dt.datetime(2019,10,18,0),dt.datetime(2019,10,26,23)),
                     (dt.datetime(2019,10,30,0),dt.datetime(2019,10,30,23)),
                     (dt.datetime(2019,11,10,0),dt.datetime(2019,11,10,23)),
                     (dt.datetime(2019,11,15,0),dt.datetime(2019,11,15,23)),
                     (dt.datetime(2019,11,19,0),dt.datetime(2019,11,19,23)),
                     (dt.datetime(2019,11,22,0),dt.datetime(2019,11,24,23))]


dates = pd.DataFrame()
for date_tuple in dates_protest:
    start_date = date_tuple[0].strftime('%Y-%m-%d %H')
    end_date = date_tuple[1].strftime('%Y-%m-%d %H')
    date_range = pd.DataFrame(pd.date_range(start = start_date,
                               end= end_date,
                               freq = 'H'))
    dates = pd.concat([dates,date_range],axis=0)

dates.columns = ['dates']

dates = dates.assign(is_protest = lambda x: 1)\
            .set_index('dates')


# Merge protest dummy

reg = pd.concat([ind1,dates],axis=1).fillna(0)\
    .assign(constant = lambda x: 1,
            Values = lambda x: x/1000000)

df_final = reg.merge(data_violence,how = 'outer', on = 'dates', sort= False, ).sort_values('dates')\
                .fillna(method = 'ffill', axis = 0)



# =============================================================================
# Gráficos
# =============================================================================

df_final = df_final.loc['10/1/2019':]

fig,ax = plt.subplots(figsize=(20,6))

for date in dates_protest:
    ax.axvspan(date[0],date[1],
               facecolor = 'red', alpha = 0.25)



ax = df_final['Atendimentos de emergência'].plot(
    kind = 'area', color = 'royalblue')

ax2 = df_final['pol_pct'].plot(color = 'midnightblue',
                               secondary_y = True,
                               ax = ax)


ax2.set_ylabel('% de hashtags de cunho político nos top 50 TT',
                       fontsize = 14)
ax.set_ylabel('# de Atendimentos de Emergência - Santiago',
              fontsize = 14)

# Legendas

ryb_patch = mpatches.Patch(color='royalblue', label='Atendimentos de emergência')
mdb_line = mlines.Line2D([], [], color='blue', label = 'Índice Político TT')
red_patch = mpatches.Patch(color='red',
                           alpha = 0.25,
                           label='Dias protestos principais')

plt.legend(handles = [mdb_line,ryb_patch,
                      red_patch],
           loc = 2)


# Arrumar datas eixo horizontal
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
# Rotates and right-aligns the x labels so they don't crowd each other.
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')


ax.set_title('Índice de engajamento político Twitter x Tamanho do Protesto',fontdict = {'fontsize':18},
                loc = 'left')
ax.set_xlabel('')

ax.annotate('OBS: Atendimentos de emergência é uma proxy para o tamanho do protesto', xy=(0.05, .05),
                xycoords='figure fraction', horizontalalignment = 'left',
                fontsize=12, color='#555555')

plt.tight_layout()

