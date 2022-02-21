#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 08:45:38 2022

@author: rafaellincoln
"""

'''
In this file, we create all the variables that will be used on this research

1) Political Participation Index:

The PPI is an index based on the hourly witter trending topics (TT) in Chile.

The index is built by filtrating manually

the most influential keywords on the TT and then building the following metric:
    
PPI = (# of hashtags TT with political background)/(# of hashtags TT at that hour)

2) Big Protest Dummy:
    
Based on the most relevant dates for the estallido social found on the newspapers,

we build a dummy that assign these dates

3) Size of the protest:
    
The variable number of emergency accidents has a direct correlation to the size

of the protest, therefore, we use it as a proxy.





'''

#### Packages ####

import pandas as pd
from sqlalchemy import create_engine
import datetime as dt

# =============================================================================
# Assembly of the Political Participation Index
# =============================================================================

# Open the file with the selected hashtags with the political background
filepath = "/Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Bases de dados/Hashtags.xlsx"

# Hashtags of political background database
df_pol = pd.read_excel(filepath, sheet_name = 'DF')\
            .drop_duplicates()
            
# Reads databse from SQL and tidies data (below)

engine = create_engine(
    'sqlite:////Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Bases de dados/chile_tt.db')

db = pd.read_sql('twitter trends chile',engine)

# List assigning a dummy variable wether the variable is a hashtag (1) or not (0)
lista = [1 if '#' in text else 0 for text in db.hashtags]

# Assign a new column with dummy variable to the Database
db = db.assign(is_hashtag = lambda x: lista)

# Merge databases with political background to the hashtags
db = db.merge(df_pol,on = 'hashtags',how = 'outer',sort = False).sort_values('dates')

# Rolling 24 hour average of the volume of tweets in TT & political index as % of TT hashtags
ind1 = db.groupby(['dates']).sum()\
    .assign(pol_pct = lambda x: 100*(x.pol_dummy/x.is_hashtag))\
        .rolling(24).mean().dropna()[['pol_pct','Values']]

# =============================================================================
# Big protest Dummy
# =============================================================================

# dates of all the relevant protests of the estallido social

dates_protest = [(dt.datetime(2019,10,14,0),dt.datetime(2019,10,14,23)),
                     (dt.datetime(2019,10,18,0),dt.datetime(2019,10,26,23)),
                     (dt.datetime(2019,10,30,0),dt.datetime(2019,10,30,23)),
                     (dt.datetime(2019,11,10,0),dt.datetime(2019,11,10,23)),
                     (dt.datetime(2019,11,15,0),dt.datetime(2019,11,15,23)),
                     (dt.datetime(2019,11,19,0),dt.datetime(2019,11,19,23)),
                     (dt.datetime(2019,11,22,0),dt.datetime(2019,11,24,23))]

# Creates dataframe from the dates of the protests on an hourly frequency
dates = pd.DataFrame()
for date_tuple in dates_protest:
    start_date = date_tuple[0].strftime('%Y-%m-%d %H')
    end_date = date_tuple[1].strftime('%Y-%m-%d %H')
    date_range = pd.DataFrame(pd.date_range(start = start_date,
                               end= end_date,
                               freq = 'H'))
    dates = pd.concat([dates,date_range],axis=0)

dates.columns = ['dates'] # name  to the date column

# create dummy with protest
dates = dates.assign(is_protest = lambda x: 1)\
            .set_index('dates')

db_dummies = pd.concat([ind1,dates],axis=1).fillna(0)\
    .assign(Values = lambda x: x/1000000)


# =============================================================================
# Data About violence
# =============================================================================

data_violence = pd.read_excel(
    '/Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Dados violência.xlsx',
                              header = 2,
                              index_col = 1).dropna(
                                  axis = 1,how= 'all')

# =============================================================================
# Merge all the data in a single database                                 
# =============================================================================

df_final = db_dummies.merge(data_violence,how = 'outer', on = 'dates', sort= False, ).sort_values('dates')\
                .fillna(method = 'ffill', axis = 0)

# create engine to local database:
    
engine = create_engine('sqlite:////Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Bases de dados/all_vars_chile.db')


# Send data to local SQL database
df_final.to_sql('variaveis chile',
                engine,
                if_exists = 'replace',
                index= True)







