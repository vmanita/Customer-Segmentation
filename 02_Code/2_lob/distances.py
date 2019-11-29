# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 19:07:14 2018

@author: vitor
"""

lob_clustered.sort_values(by = 'cluster', inplace=True)


for value in lob_clustered.cluster.unique():
    lob_clusters.values[0]


count = 0

for index,centroid in lob_clustered[['R_Motor','R_Household','R_Health','R_Life','R_Work_compensate','cluster']].iterrows(): 
    if centroid.cluster==0:
        count +=1
    
print(count)   


zero = lob_clustered.loc[lob_clustered.cluster == 0]
zero = zero [['R_Motor','R_Health','R_Life','R_Work_compensate']]


##################


centro = lob_clusters[['R_Motor','R_Health','R_Life','R_Work_compensate']].values[0]
valores = zero.values

dist = 0
for value in valores:
  dist = dist + distance.euclidean(centro,value)

dist = np.round(dist,decimals=2)
print(dist)