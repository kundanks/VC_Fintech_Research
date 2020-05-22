#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:51:03 2019

@author: kundan
"""

import pandas as pd
import datetime as dt

df = pd.read_csv('fintech_output_updated2.csv')

df['Round Date']= pd.to_datetime(df['Round Date'])
df['Year'] = df['Round Date'].dt.year
df = df.drop(['Unnamed: 0','Unnamed: 0.1'], axis = 1)

df.loc[df['Name'] == 'National City Corporation', 'Industry'] = 'Others'
df.loc[df['Name'] == 'Washington Mutual, Inc.', 'Industry'] = 'Others'
df.loc[df['Name'] == 'National City Corporation', 'Fintech'] = False
df.loc[df['Name'] == 'Washington Mutual, Inc.', 'Fintech'] = False
#df.to_csv('fintech_output_most_updated.csv')

df1 = df[df['Company MSA'].isin(['San Francisco, CA','San Jose, CA','Boston, MA-NH','New York, NY','Chicago, IL','San Diego, CA','Los Angeles-Long Beach, CA','Washington, DC-MD-VA-WV','Seattle-Bellevue-Everett, WA','Dallas, TX'])]
df1 = df1.loc[df1['Industry'] == 'Fintech']
df1 = df1.groupby(['Company MSA','Year']).size().reset_index()
df1 = df1.rename(columns = {0: 'Deal Number'})

pop = pd.read_csv('population.csv')
#https://stackoverflow.com/questions/27764378/how-to-reverse-a-2-dimensional-table-dataframe-into-a-1-dimensional-list-using
pop1 = pd.melt(pop, id_vars='Unnamed: 0', value_vars=list(pop.columns[1:]), var_name='Company MSA', value_name='Population')
pop1 = pop1.rename(columns = {'Unnamed: 0': 'Year'})
pop1 = pop1[['Company MSA','Year','Population']]
#population (million)
pop1['Population'] = pop1['Population']/1000

df1 = pd.merge(df1, pop1, on=['Company MSA','Year'], how='inner')

df1['Round Number Per Capita'] = df1['Deal Number']/df1['Population']

df1.loc[df1['Year'].isin([1990,1991,1992,1993,1994,1995,1996,1997,1998,1999]), 'Decade'] = '1990-1999'
df1.loc[df1['Year'].isin([2000,2001,2002,2003,2004,2005,2006,2007,2008,2009]), 'Decade'] = '2000-2009'
df1.loc[df1['Year'].isin([2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]), 'Decade'] = '2010-2019'

df2 = df1.groupby(['Company MSA','Decade'])['Round Number Per Capita'].mean().reset_index()

#https://pbpython.com/pandas-crosstab.html
df3 = pd.crosstab(df2['Company MSA'], df2['Decade'], values = df2['Round Number Per Capita'], aggfunc = 'sum')

df4 = df3.sort_values('2010-2019', ascending = False)

df4['D1-D2'] = (df4['2000-2009']-df4['1990-1999'])/df4['1990-1999']*100
df4['D2-D3'] = (df4['2010-2019']-df4['2000-2009'])/df4['2000-2009']*100

df5 = df1.groupby(['Company MSA','Decade'])['Deal Number'].sum().reset_index()
df5 = df5.rename(columns = {0: 'Deal Number'})

df4.to_csv('Fintech_Deal_Number_Average_Per_Capita.csv')
df5.to_csv('Fintech_Deal_Number.csv')
