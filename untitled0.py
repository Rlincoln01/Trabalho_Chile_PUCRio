#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 09:09:15 2022

@author: rafaellincoln
"""



# Pacotes a serem utilizados

import pandas as pd
import os
import seaborn as sns
import requests
from bs4 import BeautifulSoup  
import re
from tqdm import tqdm
from sqlalchemy import create_engine
import datetime as dt

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

