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
from sqlalchemy import create_engine

# statistics pakages for regression
from statsmodels.discrete.discrete_model import Probit
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
from statsmodels.tools.tools import add_constant
import statsmodels.api as sm

#engine from database

engine = create_engine('sqlite:////Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Bases de dados/all_vars_chile.db')


# =============================================================================
# Model 1
# =============================================================================

'''
The first model consists of a regression of the number of hospitalizations by

the PPI variable, of the functional form: NoH(t) = b0 + b1PPI(t) + e(t)
    
'''

model1 = pd.read_sql('variaveis chile', engine)\
    [['dates','pol_pct','Atendimentos de emergência']]\
        .set_index('dates').dropna(axis = 0)

# Variável exógena
Y = model1['Atendimentos de emergência']

# Variável endôgena
X = model1.pol_pct

# add constant (b0)
X = add_constant(X)

results = sm.OLS(Y,X).fit()

# =============================================================================
# Model 2
# =============================================================================

'''
The second model consists of a probit of the probability of a mass protest

given by the PPI variable, of the functional form: 
    
P(Y=1|PPI(t)) = b0 + b1PPI(t) + e(t)
    
'''

model2 = pd.read_sql('variaveis chile',engine)\
    [['dates','pol_pct','is_protest']]

Y = model2['is_protest']

X = model2[['pol_pct']]

X = add_constant(X)

model_1 = Probit(Y,X)
 
results = model_1.fit()






