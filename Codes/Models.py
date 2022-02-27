#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 20:11:45 2022

@author: rafaellincoln
"""

'''
In this file, we try to implement simple models in order to see the effect of

our Political Participation Index in the size of the protest and its occurence

due to imperfect data or the complete lack of it, it is needed to make some

hypthesis and assumptions.

'''

### Packages ###
import pandas as pd


# statistics pakages for regression
from statsmodels.discrete.discrete_model import Probit
from statsmodels.tools.tools import add_constant
import statsmodels.api as sm



# =============================================================================
# Model 1
# =============================================================================

'''
The first model consists of a regression of the number of hospitalizations by

the PPI variable, of the functional form: NoH(t) = b0 + b1PPI(t) + e(t)
    
'''

# Read variables used in this model
data = pd.read_csv('https://raw.githubusercontent.com/Rlincoln01/Trabalho_Chile_PUCRio/main/Bases%20de%20dados/base_completa_chile.csv')
            
data = data.assign(dates = pd.to_datetime(data.dates)).set_index('dates')\
             [['pol_pct','Atendimentos de emergência','is_protest']].dropna(axis=0)


# Variável exógena
Y = data['Atendimentos de emergência']

# Variável endôgena
X = data.pol_pct

# add constant (b0)
X = add_constant(X)

results = sm.OLS(Y,X).fit()

# ==== Model 1 with lags on PPI variable ==== #

#Create lagged variables
for x in range(1,25):
    var_name = f'lag_{x}'
    data[var_name] = data.pol_pct.shift(-x)

# Base model

columns = ['Coeficiente','P-Valor T','P-Valor F','RSquared']

df_results = pd.DataFrame(data = 
                          [[round(results.params['pol_pct'],4),
                           round(results.pvalues['pol_pct'],4),
                           round(results.f_pvalue,4),
                           results.rsquared]],
                        columns = columns)


# Add lags and compare models
for x in range(1,25):
    
    X = data[f'lag_{x}'].dropna()
    
    # add constant (b0)
    X = add_constant(X)

    # 
    Y = data[['Atendimentos de emergência',f'lag_{x}']].dropna(axis=0)['Atendimentos de emergência']

    results = sm.OLS(Y,X).fit()
    
    row = [[round(results.params[f'lag_{x}'],4),
                           round(results.pvalues[f'lag_{x}'],4),
                           round(results.f_pvalue,4),
                           results.rsquared]]
    
    df_results = df_results.append(pd.DataFrame(row, columns = columns),
                                                ignore_index = True)
    


# =============================================================================
# Model 2
# =============================================================================

'''
The second model consists of a probit of the probability of a mass protest

given by the PPI variable, of the functional form: 
    
P(Y=1|PPI(t)) = b0 + b1PPI(t) + e(t)
    
'''


Y = data['is_protest']

X = data[['pol_pct']]

X = add_constant(X)

model_2 = Probit(Y,X)
 
results = model_2.fit()

# ==== Model 2 with lags on PPI variable ==== #

#Create lagged variables
for x in range(1,25):
    var_name = f'lag_{x}'
    data[var_name] = data.pol_pct.shift(-x)

# Base model

columns = ['Coeficiente','P-Valor T','Pseudo-RSquared']

df_results = pd.DataFrame(data = 
                          [[round(results.params['pol_pct'],4),
                           round(results.pvalues['pol_pct'],4),
                           results.prsquared]],
                        columns = columns)

# Add lags and compare models
for x in range(1,25):
    
    X = data[f'lag_{x}'].dropna()
    
    # add constant (b0)
    X = add_constant(X)

    # 
    Y = data[['is_protest',f'lag_{x}']].dropna(axis=0)['is_protest']

    results = Probit(Y,X).fit()
    
    row = [[round(results.params[f'lag_{x}'],4),
                           round(results.pvalues[f'lag_{x}'],4),
                           results.prsquared]]
    
    df_results = df_results.append(pd.DataFrame(row, columns = columns),
                                                ignore_index = True)
    

