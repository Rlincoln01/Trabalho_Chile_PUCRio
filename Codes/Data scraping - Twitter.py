#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 20:56:39 2022

@author: rafaellincoln
"""

#### Packages ####

# Data cleaning and storage
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt
from tqdm import tqdm

# Web-scraping 
import requests
from bs4 import BeautifulSoup  
import re


# =============================================================================
# Functions used along the code
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

# Function for web-scraping (source: getdaytrends.com)

def get_hashtags_at_date_hour(date, headers):
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


# =============================================================================
# Web-scraping Twitter data from get day trends
# =============================================================================

# 1st - define headers of the website 

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

# 2nd - establish dates to collect data
dates = pd.date_range(start = '8/1/2019',end = '11/30/2019', freq = 'H')

dates = pd.date_range(start = '11/30/2019', end = '12/16/2019', freq = 'H')


# 3rd - Loop to collect data and assemble altogether into dataframe
db = pd.DataFrame()
for date in tqdm(dates): # tqdm establhises estimated time based on # of iterations
    df_date = get_hashtags_at_date_hour(date,headers)
    db = pd.concat([db,df_date],axis=0)
    
    
# 4th - Save as db archive in local SQL database

engine = create_engine(
    'sqlite:////Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Bases de dados/chile_tt.db')

db.to_sql('twitter trends chile',engine,
                if_exists = 'replace',
                index = False)



                                  
                                  
                                  
                                  
                                  
                                  








