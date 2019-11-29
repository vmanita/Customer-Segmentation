#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:20:37 2018

@author: Manita
"""
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt

# Compute clustering with MeanShift

to_MS = engage.drop(columns=["Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])


# Scale variables

from sklearn.preprocessing import MinMaxScaler
my_scaler = MinMaxScaler()

to_MS = my_scaler.fit_transform(to_MS)


# The following bandwidth can be automatically detected using
my_bandwidth = estimate_bandwidth(to_MS,
                               quantile=0.15,
                               n_samples=1000)

ms = MeanShift(bandwidth=my_bandwidth,
               #bandwidth=0.15,
               cluster_all = False,
               bin_seeding=True)

ms.fit(to_MS)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)


#Values
print(my_scaler.inverse_transform(X=cluster_centers))

#Count
unique, counts = np.unique(labels, return_counts=True)

print(np.asarray((unique, counts)).T)

# lets check our are they distributed


from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(to_MS)
pca_2d = pca.transform(to_MS)
for i in range(0, pca_2d.shape[0]):
    if labels[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r',marker='+')
    elif labels[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',marker='o')
    elif labels[i] == 2:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',marker='*')
    elif labels[i] == -1:
        c4 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='c',marker='H')

plt.legend([c1, c2, c3,c4], ['Cluster 1', 'Cluster 2','Cluster 3 ','Noise'])
plt.title('Mean Shift found 3 clusters')
plt.show()


#DBSCAN
to_MS = engage.drop(columns=["Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])


# Scale variables

from sklearn.preprocessing import MinMaxScaler
my_scaler = MinMaxScaler()

to_MS = my_scaler.fit_transform(to_MS)


# The following bandwidth can be automatically detected using
my_bandwidth = estimate_bandwidth(to_MS,
                               quantile=0.2,
                               n_samples=1000)

ms = MeanShift(bandwidth=my_bandwidth,
               #bandwidth=0.15,
               cluster_all = False,
               bin_seeding=True)

ms.fit(to_MS)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
test = to_MS


from sklearn.cluster import DBSCAN
from sklearn import metrics

db = DBSCAN(eps=my_bandwidth,
            min_samples=100).fit(test)

labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

unique_clusters, counts_clusters = np.unique(db.labels_, return_counts = True)
print(np.asarray((unique_clusters, counts_clusters)))

from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(test)
pca_2d = pca.transform(test)
for i in range(0, pca_2d.shape[0]):
    if db.labels_[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r',marker='+')
    elif db.labels_[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',marker='o')
    elif db.labels_[i] == 2:
        c4 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='k',marker='v')
    elif db.labels_[i] == 3:
        c5 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='y',marker='s')
    elif db.labels_[i] == 4:
        c6 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='m',marker='p')
    elif db.labels_[i] == 5:
        c7 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='c',marker='H')
    #elif db.labels_[i] == -1:
    #    c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',marker='*')

plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2','Noise'])
plt.title('DBSCAN finds 2 clusters and noise')
plt.show()

















