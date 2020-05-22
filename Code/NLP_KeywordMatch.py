#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 16:37:57 2019

@author: kundan
"""


#Import packages
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


#Load keywords
keywords = pd.read_csv('key_words_new.csv')
key_words = list(keywords['Keywords'])
individual_words = key_words[0:14]
stop_words = set(stopwords.words("english"))


#Load demo data
demo = pd.read_csv('newCompanyData_CPI.csv')
demo = demo[['Company Name','Company Business Description, Long', 'SIC']]
#demo = demo.sample(frac=1)
#demo = demo.head(1000)
demo.columns = ['Name', 'Description', 'SIC']


#Clean demo data
def Cleaning(x):
    try:
        x['Description_Cleaned'] = re.sub('[^a-zA-Z]', ' ', x['Description'])
        x['Description_Cleaned'] = x['Description_Cleaned'].lower()
        x['Description_Cleaned'] = x['Description_Cleaned'].split()
        x['Description_Cleaned'] = [WordNetLemmatizer().lemmatize(word) for word in x['Description_Cleaned']]
        x['Description_Cleaned'] = [word for word in x['Description_Cleaned'] if word not in stop_words]
        x['Description_Cleaned'] = ' '.join(x['Description_Cleaned'])
        return x
    except TypeError:
        return x


demo = demo.apply(lambda x: Cleaning(x), axis=1)
demo['Description_Cleaned'] = demo['Description_Cleaned'].astype(str)

demo = demo[['Name', 'Description', 'Description_Cleaned', 'SIC']]


#First filter
def first_filter(x):
    valueList = []
    for i in range(len(individual_words)):
        if x['Description_Cleaned'].find(individual_words[i]) != -1:
            valueList.append(individual_words[i])
    return valueList


demo['First'] = demo.apply(lambda x: first_filter(x), axis = 1)


#Detect common words
def common_words(x):
    valueList = []
    for i in range(len(key_words)):
        if x['Description_Cleaned'].find(key_words[i]) != -1:
            valueList.append(key_words[i])
    return valueList


demo['Common'] = demo.apply(lambda x: common_words(x), axis = 1)


#Check if Fintech or not
def Fintech(x):
    if len(x['First']) >= 1 and len(x['Common']) >= 3 and \
    'medicine' not in x['Description_Cleaned'] and \
    'medical' not in x['Description_Cleaned'] and \
    'healthcare' not in x['Description_Cleaned'] and \
    x['SIC'] in [59, 60, 61, 62, 63, 64, 65, 67, 73, 87, 89]:
        x['Fintech'] = 'True'
    else:
        x['Fintech'] = 'False'
    return x


demo_fintech = demo.apply(lambda x: Fintech(x), axis=1)


#Value counts
total_value_counts = demo_fintech['Fintech'].value_counts()


#Add SIC constraints
#demo_fintech_SIC = demo_fintech[demo_fintech['SIC'].isin(['59','60','61','62','63','64','65','67','73','87','89'])]


#Export data
demo_fintech.to_csv('fintech_output_new.csv')
#demo_fintech_SIC.to_csv('fintech_output_SIC.csv')


#Convert a list to dataframe
#key_words = pd.DataFrame(key_words)
#key_words.to_csv('key_words_new.csv')


#Check several rows
#test = demo_fintech[demo_fintech['Name'] == 'CHD Meridian Healthcare']


#Check SIC code
#fintech_only = demo_fintech[demo_fintech['Fintech']=='True']
#SIC = fintech_only['SIC'].value_counts()
#SIC.to_csv('SIC.csv')


#Drop duplicates
#demo_fintech_no_dup = demo_fintech.drop_duplicates(['Name', 'Description'], keep = 'first').reset_index()
#total_value_counts = demo_fintech_no_dup['Fintech'].value_counts()
#fintech_only_no_dup = demo_fintech_no_dup[demo_fintech_no_dup['Fintech']=='True']
#SIC_no_dup = fintech_only_no_dup['SIC'].value_counts()
#SIC_no_dup.to_csv('SIC_no_dup.csv')

