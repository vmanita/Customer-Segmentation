#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:40:50 2018

@author: Manita
"""

to_EM = engage.copy()[['Salary','C_value','Total_Premium']]

#test = StandardScaler().fit_transform(test)
#To reverse
my_scaler = StandardScaler()

to_EM_norm = my_scaler.fit_transform(to_EM)

from sklearn import mixture
gmm = mixture.GaussianMixture(n_components=3,
                              covariance_type='full',
                              init_params='kmeans',
                              max_iter=1000,
                              n_init=10)

gmm.fit(to_EM_norm)
EM_labels_ = gmm.predict(to_EM_norm)
#Elbow
EM_score_ = gmm.score(to_EM_norm)
#Individual
EM_score_samp = gmm.score_samples(to_EM_norm)
#Individual
EM_pred_prob = gmm.predict_proba(to_EM_norm)

import numpy as np
unique_clusters, counts_clusters = np.unique(EM_labels_, return_counts = True)
print(np.asarray((unique_clusters, counts_clusters)).T)
#Check the distribution
gmm.weights_
gmm.means_

# Engage clustered

engage_clustered = to_EM.copy()
labels = pd.DataFrame({'cluster':EM_labels_})

engage_clustered = pd.concat([engage_clustered,labels],axis=1)

cluster_freq(engage_clustered,"cluster")


engage_clusters = pd.DataFrame(pd.DataFrame(engage_clustered.groupby('cluster').mean()))
print (engage_clusters)

engage_clusters.mean()



table = engage_clustered
x = "Total_Premium"
y = "C_value"
hue = "cluster"

plot2d(table,x,y,hue)









