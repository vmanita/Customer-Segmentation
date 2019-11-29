# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:55:46 2018

@author: vitor
"""
import sqlite3
import pandas as pd
import numpy as np
import sklearn
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
import missingno as msno
from sklearn.cluster import KMeans
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from plotly.offline import init_notebook_mode
import scipy
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm
from sklearn.decomposition import PCA
from kmodes.kmodes import KModes
from sklearn.preprocessing import StandardScaler


pd.set_option('display.expand_frame_repr', False)

#******************************************************************************
#Import data
#******************************************************************************
# mac
my_path = '/Users/Manita/Documents/DM/project/1_import and preprocess/insurance.db'

# windows
#my_path = 'C:\\Users\\vitor\\OneDrive - NOVAIMS\\DM\\project\\1_import and preprocess\\insurance.db'
#******************************************************************************
#SQL
#******************************************************************************

conn = sqlite3.connect(my_path)
cursor = conn.cursor()

cursor.execute("select name from sqlite_master where type= 'table';")
print(cursor.fetchall())

lob_query= """select * from LOB"""
engage_query = """select * from Engage"""

#Tables
lob= pd.read_sql_query(lob_query, conn)
engage= pd.read_sql_query(engage_query, conn)

#******************************************************************************
#Rename columns
#******************************************************************************
#Lob
lob.rename(index = str, columns = {'Customer Identity':'c_id',
                                    'Premiums in LOB: Motor':'Motor',
                                    'Premiums in LOB: Household' : 'Household',
                                    'Premiums in LOB: Health':'Health',
                                    'Premiums in LOB:  Life':'Life',
                                    'Premiums in LOB: Work Compensations':'Work_compensate'},inplace = True )

#Engage
engage.rename(index = str, columns = {'Customer Identity':'c_id',
                                      'First Policy´s Year':'First_Policy_Year',
                                      'Brithday Year':'Birthday',
                                      'Educational Degree':'Educ',
                                      'Gross Monthly Salary':'Salary',
                                      'Geographic Living Area':'Living_Area',
                                      'Has Children (Y=1)':'Child',
                                      'Customer Monetary Value':'C_value',
                                      'Claims Rate':'Claims_rate'},inplace = True )

#******************************************************************************
#Set indexes
#******************************************************************************
'''
lob.c_id = lob.c_id-1
engage.c_id = engage.c_id-1
'''
#lob
#lob.set_index(keys='c_id',drop=True,inplace=True)
lob.drop(columns=['index'],inplace=True)
#engage
#engage.set_index(keys='c_id',drop=True,inplace=True)
engage.drop(columns=['index'],inplace=True)















