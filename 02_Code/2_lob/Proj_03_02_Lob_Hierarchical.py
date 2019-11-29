# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:58:25 2018

@author: vitor
"""

#******************************************************************************
#Hierarchical
#******************************************************************************


#lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

# normalize

lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

# normalize lob 

my_scaler = preprocessing.StandardScaler() #StandardScaler #MinMaxScaler
lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)



# Dendogram

dendo(lob_to_clust, line = 80, p =35)

# Hierarchical clustering

lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

# normalize lob 

my_scaler = preprocessing.StandardScaler() #StandardScaler #MinMaxScaler
lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)


k=3

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity='euclidean',
                                      linkage='ward')

# Get clusters
my_HC = Hclustering.fit(lob_to_clust)

my_labels = pd.DataFrame(my_HC.labels_)
my_labels.columns =  ['lob_cluster']

# lob clustered
lob_clustered = lob.copy()
lob_clustered.reset_index(drop=True,inplace=True)


lob_clustered["cluster"] = my_labels


# lob clusters mean

lob_clusters = lob_clustered.groupby(['cluster']).mean()
print(lob_clusters)

lob_clusters.mean()