#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:17:50 2020

@author: rafaellincoln
"""

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt



filedir = '/Users/rafaellincoln/Downloads/Latinobarometro/'

os.chdir(filedir)

# =============================================================================
# How do you inform yourself about politics
# =============================================================================

countries = {32: 'Argentina',
  68: 'Bolivia',
  76: 'Brazil',
  170: 'Colombia',
  188: 'Costa Rica',
  152: 'Chile',
  218: 'Ecuador',
  222: 'El Salvador',
  724: 'Spain',
  320: 'Guatemala',
  340: 'Honduras',
  484: 'Mexico',
  558: 'Nicaragua',
  591: 'Panama',
  600: 'Paraguay',
  604: 'Peru',
  214: 'Dominican Rep.',
  858: 'Uruguay',
  862: 'Venezuela'}

def create_time_value(question_dictionary,
                    year):
    # Name of variable
    colname = question_dictionary[year]
    # Tidying and preparing data
    df = pd.read_stata(f'Latinobarometro_{year}.dta',
                       convert_categoricals=False)\
        .rename(columns = {'IDENPA':'idenpa',
                           'WT':'wt',
                           'pais':'idenpa',
                           'pondera':'wt'})\
            [['idenpa',colname,'wt']]\
                .query("idenpa == 152")\
                .rename(columns = {'idenpa':'country'})\
                .assign(wt = lambda x: x['wt'].astype(float))\
                .assign(weighted_val = lambda x: x[colname]*x['wt'])\
                .drop([colname,'wt'],axis=1)\
                .groupby(['country']).mean().dropna()\
                .assign(year = lambda x: year)\
                .reset_index(drop=True)        
    return df


def create_database(question_dictionary,variable):
    ts = pd.DataFrame()
    for year in question_dictionary.keys():
        x = create_time_value(question_dictionary,
                              year)\
            .rename(columns = {'weighted_val':variable})
        ts = pd.concat([ts,x],axis=0)
        
    ts = ts.reset_index(drop=True)\
        .assign(year = lambda x: pd.to_datetime(x.year,
                                                format = '%Y'))\
        .set_index('year')
    return ts

def format_1_plotting(df,x_ax_title,y_ax_title,legend_box_title,title,source,style_list,
                      loc_legend_box):    
    fig,ax = plt.subplots(figsize = (15,7))
    df.plot(ax=ax, style = style_list)
    ax.legend(loc = loc_legend_box, title = legend_box_title,
                  fancybox=True,facecolor = 'white',
                  edgecolor = 'black',fontsize = 14)
    ax.set_title(title,fontdict = {'fontsize':22},
                 loc = 'left')
    ax.set_ylabel(y_ax_title, fontsize = 14)
    ax.set_xlabel(x_ax_title)
    ax.tick_params(axis = 'both',which = 'major',labelsize = 14)
    for counter, value in enumerate(df.tail(1).values.tolist()[0]):
            column = df.columns[counter]
            index = df[column].dropna(axis=0).tail(1).index[0]
            value = df.iloc[-1,counter]
            ax.text(index,value,"{:.2f}".format(value),
                     fontsize = 12)

    # Add source
    ax.annotate(f'Source: {source}', xy=(0.1, .05),
                xycoords='figure fraction', horizontalalignment = 'left',
                fontsize=12, color='#555555')
    plt.tight_layout()


# How do you inform yourself about politics: Internet

q1_dic = {2008:'p95st_g',
          2009:'p90st_g',
          2010:'P77ST_G',
          2016:'P26STH',
          2017:'P15ST_H',
          2018:'P19ST.G'}

q1_df = create_database(q1_dic,'Internet')

# How do you inform yourself about politics: Radio

q2_dic = {1996:'p35e',
            2000:'P55ST_E',
            2002:'p42ste',
            2008:'p95st_e',
            2009:'p90st_e',
            2010:'P77ST_E',
            2016:'P26STE',
            2017:'P15ST_E',
            2018:'P19ST.E'}

q2_df = create_database(q2_dic,'Radio')

# How do you inform yourself about politics: Newspapers

q3_dic = {1996:'p35f',
            2000:'P55ST_F',
            2002:'p42stf',
            2008:'p95st_f',
            2009:'p90st_f',
            2010:'P77ST_F',
            2016:'P26STF',
            2017:'P15ST_F',
            2018:'P19ST.F'}


q3_df = create_database(q3_dic,'Newspaper')


# How do you inform yourself about politics: Television

q4_dic = {1996:'p35g',
            2000:'P55ST_G',
            2002:'p42stg',
            2008:'p95st_g',
            2009:'p90st_g',
            2010:'P77ST_G',
            2016:'P26STG',
            2017:'P15ST_G',
            2018:'P19ST.G'}

q4_df = create_database(q4_dic,'Television')

# How do you inform yourself about politics: Social Media

q5_dic = {2016:'P26STG',
          2017:'P15ST_G'}

q5_df = create_database(q5_dic,'Social Media')


# All forms of informing itself about politics:

info_pol = pd.concat([q1_df,q2_df,q3_df,q4_df,q5_df],axis=1)*100


format_1_plotting(info_pol,'','% of mentions',
                  'How do you inform yourself?',
                  'How do you inform yourself? - % of mentions by media vehicle',
                  'Latinobarometro',
                  ['+-','o-','.--','s:','1-'],
                  loc_legend_box = 'upper right')

# =============================================================================
# Confidence towards institutions
# =============================================================================

# =============================================================================
# 1 - A lot of confidence
# 2 - Some confidence
# 3 - Little Confidence
# 4 - No confidence
# =============================================================================

# Confidence towards Armed forces

q1_dic = {1995:'p27b',
          1996:'p33b',
         1997:'sp63b',
         1998:'sp38b',
         2000:'P35ST_B',
         2001:'p61stb',
         2002:'p36stb',
         2003:'p21stg',
         2004:'p32stg',
         2005:'p42stb',
         2006:'p32st_e',
         2007:'p27st_d',
         2008:'p28st_d',
         2009:'p26st_d',
         2010:'P20ST_D',
         2011:'P22ST_D',
         2013:'P28TGB_A',
         2015:'P16TGB_A',2016:'P13STGBSA',
         2017:'P14STGBS_A',
         2018:'P15STGBSC.A'}

q1_df = create_database(q1_dic,'Armed Forces')

# Confidence towards Political Parties

q2_dic = {1995:'p27j',
          1996:'p33j',
          1997:'sp63g',
          1998:'sp38g',
          2000:'P35ST_G',
          2001:'p61stg',
          2002:'p34stf',
          2003:'p21std',
          2004:'p34std',
          2005:'p47stb',
          2006:'p24st_c',
          2007:'p27st_e',
          2008:'p28st_c',
          2009:'p26st_c',
          2010:'P20ST_C',
          2011:'P22ST_C',
          2013:'P26TGB_G',
          2015:'P19ST_C',
          2016:'P13STG',
          2017:'P14ST_G',
          2018:'P15STGBSC.G'}

q2_df = create_database(q2_dic,'Political Parties')

# Confidence towards Congress

q3_dic = {1995:'p27i',1996:'p33i',
          1997:'sp63f',
          1998:'sp38f',
          2000:'P35ST_F',
          2001:'p61stf',
          2002:'p36std',
          2003:'p21stf',
          2004:'p34stf',
          2005:'p45sta',
          2006:'p24st_f',
          2007:'p24st_f',
          2008:'p28st_a',
          2009:'p26st_a',
          2010:'P20ST_A',
          2011:'P22ST_A',
          2013:'P26TGB_C',
          2015:'P16ST_F',
          2016:'P13STD',
          2017:'P14ST_D',
          2018:'P15STGBSC.D'}

q3_df = create_database(q3_dic,'Congress')

# Confidence in the Judiciary

q4_dic = {1995:'p27d',1996:'p33d',1997:'sp63c',1998:'sp38c',2000:'P35ST_C',
          2001:'p61stc',2002:'p34stc',2003:'p21ste',2004:'p34stb',2005:'p42std',
          2006:'p24st_a',2007:'p24st_d',2008:'p28st_b',2009:'p26st_b',2010:'P20ST_B',
          2011:'P22ST_B',2013:'P26TGB_E',2015:'P16ST_H',2016:'P13STF',2017:'P14ST_F',
          2018:'P15STGBSC.F'}

q4_df = create_database(q4_dic,'Judiciary')

# Confidence in the TV

q5_dic = {1995:'p27l',1996:'p33l',
          1997:'sp63h',
          1998:'sp38h',
          2000:'P35ST_H',
          2001:'p63sta',2002:'p36sta',
          2003:'p21stc',
          2004:'p32stf',
          2005:'p45stb',
          2006:'p35st_c',
          2007:'p24st_i',
          2008:'p31st_e',
          2009:'p24st_e',
          2010:'P18ST_E',
          2011:'P20ST_E',
          2013:'P28TGB_D',
          2015:'P16TGB_D'}

q5_df = create_database(q5_dic,'TV')

# Confidence in Radio

q6_dic = {2001:'p63stf',2003:'p23stf',2005:'p47std',2006:'p35st_b',2007:'p27st_a',
          2008:'p31st_f',2009:'p24st_f',2010:'P18ST_F',2011:'P20ST_F',2013:'P28ST_I',
          2015:'P16ST_I'}

q6_df = create_database(q6_dic,'Radio')

# Confidence in Newspapers

q7_dic = {2001:'p63ste',2003:'p23ste',2004:'p34ste',2005:'p47stc',2006:'p32st_c',
          2007:'p24st_c',2008:'p31st_d',2009:'p24st_d',2010:'P18ST_D',2011:'P20ST_D',
          2013:'P28TGB_C',2015:'P16TGB_C'}

q7_df = create_database(q7_dic,'Newspapers')

# Support for democracy

q8_dic = {1995:'p20',1996:'p19',1997:'sp31',1998:'sp28',2000:'P29ST',2001:'p46st',2002:'p32st',
          2003:'p14st',2004:'p13st',2005:'p16st',2006:'p17st',2007:'p9st',2008:'p13st',2009:'p10st',
          2010:'P10ST',2011:'P13ST',2013:'P12STGBS',2015:'P11STGBS',2016:'P8STGBS',2017:'P8STGBS',2018:'P12STGBS'}


q8_df = create_database(q8_dic,'Democracy')

# Confidence on the gov

q9_dic = {1995:'p27m',1996:'p33m',2002:'p34std',2003:'p23stg',2004:'p32std',2005:'p45stc',
          2006:'p32st_a',2007:'p24st_a',2008:'p31s_ta',2009:'p24st_a',2010:'P18ST_A',2011:'P20ST_A',
          2013:'P26TGB_B',2015:'P16ST_G',2016:'P13STE',2017:'P14ST_E',2018:'P15STGBSC.E'}


q9_df = create_database(q9_dic,'Government')

## 1st) Confidence towards media vehicles

conf_media = pd.concat([q5_df,q6_df,q7_df],axis=1)

format_1_plotting(conf_media,'Index of confidence','Year','Media Vehicle',
                  'Confidence towards media vehicles in Chile',
                  'Latinobarometro',
                  ['+-','o-','.--','s:'],
                  'upper left')

## 2nd) Trust towards institutions

conf_ins = pd.concat([q1_df,q2_df,q3_df,q4_df,q8_df,q9_df],axis=1)


# 2.1 trust towards three branches of the state

conf_ins_2 = pd.concat([q2_df,q3_df,q4_df,q9_df],axis=1)

format_1_plotting(conf_ins_2,'','Index of confidence', 'Institution',
                  'Trust towards the main branches of the Chilean State',
                  'Latinobarometro',
                  ['+-','o-','.--','s:'],
                  'upper left')


# =============================================================================
# Google trends, social media and protests
# =============================================================================

from pytrends.request import TrendReq
import datetime as dt

# What were the main hashtags during the protests? #

# la marcha más grande de chile
# Chile Despertó
# Cacerolazo
# Evasion Masiva
# Pacos culiaos






pytrends = TrendReq(hl='es-CL', tz=180)

# Collect hashtag-like trend keywords

def get_keywords_database(keywords,timeframe,geo):
    '''
    keywords: list variable. Keywords searched on google
    
    timeframe: Specific dates, 'YYYY-MM-DD YYYY-MM-DD'
    
    geo: Geolocalisation, string variable
    '''
    pytrends.build_payload(keywords,
                                cat=0,
                                timeframe = timeframe,
                                geo=geo, gprop='')
    
    df = pytrends.interest_over_time()\
                .drop('isPartial',axis=1)
    return df
    

timeframe = '2019-10-07 2019-11-30'

keywords = [['la marcha mas grande de chile'],['chile desperto'],['cacerolazo'],
            ['Evasion Masiva']]

keywords_1 = [['cacerolazo'],['Evasion Masiva']]

keywords = [['la marcha mas grande de chile','chile desperto','cacerolazo','Evasion Masiva']]


df = pd.DataFrame()
for var in keywords_1:
    ts = get_keywords_database(var,timeframe,geo = 'CL')
    df = pd.concat([df,ts],axis=1)

fig, ax = plt.subplots()

df.plot(ax=ax)
for date in dates:
    plt.axvline(date,
                color = 'black',
                linestyle ="--")

# =============================================================================
# Web-scraping for twitter trends
# =====================================================
    
import requests
from bs4 import BeautifulSoup  
import re
from tqdm import tqdm
from sqlalchemy import create_engine
import datetime as dt

engine = create_engine('sqlite:////Users/rafaellincoln/Desktop/Sciences Po/Le prix de la démocratie/chile.db')

    
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

def get_hashtags_at_date_hour(date):
    '''
    date: datetime format
    hour: string from 0-23
    '''
    hour = date.hour
    
    day = date.strftime('%Y-%m-%d')

    link = f'https://getdaytrends.com/fr/chile/{day}/{hour}/'
    
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
    
dates = pd.date_range(start = '8/1/2019',end = '11/30/2019', freq = 'H')


db = pd.DataFrame()
for date in tqdm(dates):
    df_date = get_hashtags_at_date_hour(date)
    db = pd.concat([db,df_date],axis=0)
    

db.to_sql('twitter trends chile',engine,
                if_exists = 'replace',
                index = False)



# =============================================================================
# Political hashtags
# =============================================================================

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

# Probit model

from statsmodels.discrete.discrete_model import Probit
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
from statsmodels.tools.tools import add_constant

Y = reg['is_protest']

X = reg[['Values','pol_pct']]

X = add_constant(X)

model_1 = Probit(Y,X)
 
model_2 = Probit(reg['is_protest'],
       reg[['pol_pct','constant']])

results = model_1.fit()

results.summary()

# Jarque-Bera

name = ['Jarque-Bera', 'Chi^2 two-tail prob.', 'Skew', 'Kurtosis']
test = sms.jarque_bera(results.resid)
lzip(name, test)

df_plot = ind1[['Values','pol_pct']]\
            .rename(columns = {'Values':'Volume of Tweets',
                               'pol_pct':'Political Engagement Index (PEI)'})
            
df_plot = df_plot.reindex(pd.date_range(
    start = df_plot.index[0],
    end = df_plot.index[-1],
    freq = 'h'))
    

fig, ax = plt.subplots()

df_plot.plot(ax=ax, secondary_y = ['Political Engagement Index (PEI)'],
             fontsize = 14)

for date in dates_protest:
    ax.axvspan(date[0],date[1],
               facecolor = 'red', alpha = 0.25)


ax.right_ax.set_ylabel('% of hashtags with political background on top 50 TT',
                       fontsize = 14)
ax.set_ylabel('Top 50 Twitter Trends - Volume of Tweets',
              fontsize = 14)
ax.get_yaxis().set_major_formatter(
           FuncFormatter(lambda x, p: format(int(x), ',')))
ax.set_title('Volume of Tweets x Political Engagement Index',fontdict = {'fontsize':22},
                 loc = 'left')
ax.set_xlabel('')


plt.tight_layout()

# =============================================================================
# Selected hashtags
# =============================================================================
from matplotlib.ticker import FuncFormatter

# october 15th-20th
df = pd.read_sql('twitter trends chile',engine)

oct_1520 = df[(df.dates >= '2019-10-15 00:00:00') & (df.dates <= '2019-10-20 23:00:00')]

oct_1520 = oct_1520.merge(df_pol,on = 'hashtags',how = 'inner',sort = False).sort_values('dates')

oct_1520 = pd.pivot(oct_1520,values = 'Values',index = 'dates', columns = 'hashtags')

lista = list(oct_1520.sum(axis=0).sort_values(ascending=False).index)

oct_2126 = df[(df.dates >= '2019-10-21 00:00:00') & (df.dates <= '2019-10-26 23:00:00')]

oct_2126 = oct_2126.merge(df_pol,on = 'hashtags',how = 'inner',sort = False).sort_values('dates')

oct_2126 = pd.pivot(oct_2126,values = 'Values',index = 'dates', columns = 'hashtags')

lista = list(oct_2126.sum(axis=0).sort_values(ascending=False).index)


sep_date = dt.datetime(2019,10,24,0)
# Multiple plots
fig, ax = plt.subplots(2,2,figsize = (15,7),
                       sharex='col')
for i in range(0,4):
    s = 5*i
    e = 5*(i+1)
    hashtags = lista[s:e]
    if i < 2:
        oct_2126[hashtags].plot(ax=ax[0,i], style = ['+-','o-','.--','s:','1-'])
        ax[0,i].get_yaxis().set_major_formatter(
           FuncFormatter(lambda x, p: format(int(x), ',')))
        ax[0,i].legend(loc = 'upper right',
                       fontsize = 8)
        ax[0,i].axvline(sep_date,color = 'black',linestyle ="--", alpha = 0.5)
    else:
        oct_2126[hashtags].plot(ax=ax[1,i-2],
                                style = ['+-','o-','.--','s:','1-'])
        ax[1,i-2].get_yaxis().set_major_formatter(
           FuncFormatter(lambda x, p: format(int(x), ',')))
        ax[1,i-2].legend(loc = 'upper left',
                       fontsize = 8)
        ax[1,i-2].set_xlabel('')
        ax[1,i-2].axvline(sep_date,color = 'black',linestyle ="--", alpha = 0.5)
ax[0,0].set_title('Top 5')
ax[0,1].set_title('6th to 10th')
ax[1,0].set_title('11th to 15th')
ax[1,1].set_title('16th to 20th')
plt.tight_layout()


# Over 10k tweets and is a hashtag

# Check most busy hours 


hashtags = [text for text in db.hashtags if '#' in text]


# fig, ax = plt.subplots()
# d.plot(ax=ax)
# for date in dates_protest:
#     ax.axvspan(date[0],date[1],
#                facecolor = 'red', alpha = 0.25)


pd.Series(list(set([x for x in hashtags if 'metro' in x])))
