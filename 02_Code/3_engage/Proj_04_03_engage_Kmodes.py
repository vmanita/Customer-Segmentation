# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 20:29:23 2018

@author: vitor
"""



variable = 'R_Motor'

sns.boxplot (y = variable, x = "cluster", data =teste ,showmeans=True)


teste = lob.copy()
teste = pd.concat([teste,lob_clustered.cluster],axis=1)

#******************************************************************************
#K-modes
#******************************************************************************

my_modes = engage[["Child","High_Educ","Living_Area"]].astype(str)

k = 3

km = KModes(n_clusters=k,
            init='Huang', 
            n_init=15, 
            verbose=1)


clusters = km.fit_predict(my_modes)

ktest= engage.copy()
ktest["kmode_cluster"]=clusters

# Cluster frequency


cluster_freq(ktest,'kmode_cluster')


# Print the cluster centroids

k_modes = pd.DataFrame(km.cluster_centroids_, columns = ["Child","High_Educ","Living_Area"])
print(k_modes)


df = pd.DataFrame(ktest.kmode_cluster)
df.to_csv("/Users/Manita/OneDrive - NOVAIMS/DM/project/3_engage/kmodes.csv")






