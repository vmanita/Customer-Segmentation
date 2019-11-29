# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 15:24:00 2018

@author: vitor
"""
#******************************************************************************
#Hierarchical
#******************************************************************************

import scipy
from scipy.cluster.hierarchy import dendrogram, linkage 
from scipy.cluster import hierarchy
import sklearn
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm

# Dendogram

engage_to_clust = engage.drop(columns=["c_id","Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])
my_scaler = preprocessing.MinMaxScaler() #StandardScaler
engage_to_clust = my_scaler.fit_transform(engage_to_clust)

#https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
Z = linkage(engage_to_clust,
            method = 'ward')#method='single, complete

dendrogram(Z,
           #truncate_mode='none',
           truncate_mode='lastp',
           p=40,
           orientation = 'top',
           leaf_rotation=45.,
           leaf_font_size=10.,
           show_contracted=True,
           show_leaf_counts=True)

plt.title('Truncated Hierarchical Clustering Dendrogram')
plt.xlabel('Cluster Size')
plt.ylabel('Distance')

plt.axhline(y=10)
plt.show()

# Hierarchical clustering

engage_to_clust = engage.drop(columns=["c_id","Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])
my_scaler = preprocessing.MinMaxScaler()
engage_to_clust = my_scaler.fit_transform(engage_to_clust)

k=3

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity='euclidean',
                                      linkage='ward')

# Get clusters
my_HC = Hclustering.fit(engage_to_clust)

my_labels = pd.DataFrame(my_HC.labels_)
my_labels.columns =  ['engage_cluster']

# Engage clustered
engage_clustered = my_scaler.inverse_transform(X=engage_to_clust)
engage_clustered = pd.concat([pd.DataFrame(engage_clustered), my_labels], axis=1)
engage_clustered.columns =  ['Salary','C_value','Total_Premium','cluster']

# Engage clusters mean

engage_clusters = engage_clustered.groupby(['cluster'])['Salary','C_value','Total_Premium'].mean()
print(engage_clusters)

engage_clustered.mean()

# Cluster frequency

cluster_freq(engage_clustered,"cluster")