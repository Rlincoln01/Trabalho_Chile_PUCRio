#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 11:25:51 2022

@author: rafaellincoln
"""

''' 
This file has all the plot codes used in the research assignment

'''

### packages ###
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

# =============================================================================
# Data used on the plot - Imported from GitHub repository
# =============================================================================


# Data with variables of interest            
df_final = pd.read_csv('https://raw.githubusercontent.com/Rlincoln01/Trabalho_Chile_PUCRio/main/Bases%20de%20dados/base_completa_chile.csv')
            
df_final = df_final.assign(dates = pd.to_datetime(df_final.dates)).set_index('dates')

# Raw data
df_tt = pd.read_csv('https://raw.githubusercontent.com/Rlincoln01/Trabalho_Chile_PUCRio/main/Bases%20de%20dados/twitter_trends_chile.csv')\
    
df_tt.dates = pd.to_datetime(df_tt.dates)

# Hashtags of political background database
            
df_pol = pd.read_csv("https://raw.githubusercontent.com/Rlincoln01/Trabalho_Chile_PUCRio/main/Bases%20de%20dados/Hashtags.csv")\
            .drop('Unnamed: 0', axis =1)

# =============================================================================
# Plots
# =============================================================================


# ==== Plot 1 ==== #

# dates of all the relevant protests of the estallido social

dates_protest = [(dt.datetime(2019,10,14,0),dt.datetime(2019,10,14,23)),
                     (dt.datetime(2019,10,18,0),dt.datetime(2019,10,26,23)),
                     (dt.datetime(2019,10,30,0),dt.datetime(2019,10,30,23)),
                     (dt.datetime(2019,11,10,0),dt.datetime(2019,11,10,23)),
                     (dt.datetime(2019,11,15,0),dt.datetime(2019,11,15,23)),
                     (dt.datetime(2019,11,19,0),dt.datetime(2019,11,19,23)),
                     (dt.datetime(2019,11,22,0),dt.datetime(2019,11,24,23))]

df_p1 = df_final.loc['10/1/2019':]

fig,ax = plt.subplots(figsize=(20,6))

for date in dates_protest:
    ax.axvspan(date[0],date[1],
               facecolor = 'red', alpha = 0.25)



ax = df_p1['Atendimentos de emergência'].plot(
    kind = 'area', color = 'royalblue')

ax2 = df_p1['pol_pct'].plot(color = 'midnightblue',
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


'''
OBS: Plot two and three are similar, but vary in dates and hashtags explored

'''

# ==== Plot 2 ==== #

# october 15th-20th #

# Select dates
oct_1520 = df_tt[(df_tt.dates >= '2019-10-15 00:00:00') & (df_tt.dates <= '2019-10-20 23:00:00')]

# Choose the hashtags that have political background
oct_1520 = oct_1520.merge(df_pol,on = 'hashtags',how = 'inner',sort = False).sort_values('dates')

# pivot in order to plot it
oct_1520 = pd.pivot(oct_1520,values = 'Values',index = 'dates', columns = 'hashtags')

# List in descending order of top hashtags
lista = list(oct_1520.sum(axis=0).sort_values(ascending=False).index)


sep_date = dt.datetime(2019,10,18,0)
# Multiple plots
fig, ax = plt.subplots(2,2,figsize = (15,7),
                       sharex='col')
for i in range(0,4):
    s = 5*i
    e = 5*(i+1)
    hashtags = lista[s:e]
    if i < 2:
        oct_1520[hashtags].plot(ax=ax[0,i], style = ['+-','o-','.--','s:','1-'])
        ax[0,i].get_yaxis().set_major_formatter(
           FuncFormatter(lambda x, p: format(int(x), ',')))
        ax[0,i].legend(loc = 'upper left',
                       fontsize = 8)
        ax[0,i].axvline(sep_date,color = 'black',linestyle ="--", alpha = 0.5)
    else:
        oct_1520[hashtags].plot(ax=ax[1,i-2],
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

plt.suptitle('Volume de Tweets por Trending Topic - Top 20 Chile\n 15 a 20 de Outubro',
             fontsize = 25,
             ha = 'center')

plt.tight_layout()

# ==== Plot 3 ==== #

# Select dates
oct_2126 = df_tt[(df_tt.dates >= '2019-10-21 00:00:00') & (df_tt.dates <= '2019-10-26 23:00:00')]

# Choose the hashtags that have political background
oct_2126 = oct_2126.merge(df_pol,on = 'hashtags',how = 'inner',sort = False).sort_values('dates')

# pivot in order to plot it
oct_2126 = pd.pivot(oct_2126,values = 'Values',index = 'dates', columns = 'hashtags')

# List in descending order of top hashtags
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

plt.suptitle('Volume de Tweets por Trending Topic - Top 20 Chile\n 21 a 26 de Outubro',
             fontsize = 25,
             ha = 'center')

plt.tight_layout()

# ==== Plot 4 ==== #

# Sazonalidades do volume de tweets relacionados aos trendngs topics

df = df_tt.assign(horas = df_tt.dates.dt.hour)\
        .groupby(['horas']).mean()


fig, ax = plt.subplots(figsize = (8,6))

df.plot(ax = ax, kind = 'line',
        legend = False, color='midnightblue',
        style = ['o-'])

# formata o eixo de centenas
ax.get_yaxis().set_major_formatter(
           FuncFormatter(lambda x, p: format(int(x), ',')))

ax.set_xlabel('Hora do dia', fontdict = {'fontsize':14})
ax.set_ylabel('Volume de tweets', fontdict = {'fontsize':14})
ax.set_title('Volume médio de tweets nos \ntrending topics por hora do dia',fontdict = {'fontsize':18},
                loc = 'center')

ax.annotate('OBS: amostra de 1 de agosto a 18 de dezembro de 2019', xy=(0.05, .02),
                xycoords='figure fraction', horizontalalignment = 'left',
                fontsize=12, color='#555555')

plt.tight_layout















