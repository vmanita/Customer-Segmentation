#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 17:18:55 2018

@author: Manita
"""


# Dendogram

engage_to_clust = engage.drop(columns=["c_id","Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])


#******************************************************************************
# normalize
#******************************************************************************


my_scaler = preprocessing.StandardScaler() #StandardScaler MinMaxScaler
engage_to_clust = my_scaler.fit_transform(engage_to_clust)

# dendogram

dendo(engage_to_clust, line = 80, p =35)


#******************************************************************************
# Hierarchical
#******************************************************************************

engage_to_clust = engage.drop(columns=["c_id","Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])
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


'''boxplot compare distributions'''
variable = 'Total_Premium'

sns.boxplot (y = variable, x = "cluster", data =engage_clustered ,showmeans=True)

sns.boxplot (y = "C_value", data =engage_clustered ,showmeans=True, orient = 'v' )


# Cluster frequency

cluster_freq(engage_clustered,"cluster")

# centroids

engage_clusters
init_centroids=engage_clusters.copy().values


#******************************************************************************
# K means
#******************************************************************************


# elbow graph

engage_to_clust = engage[['Salary','C_value','Total_Premium']].copy()
my_scaler = preprocessing.StandardScaler()
engage_to_clust = my_scaler.fit_transform(engage_to_clust)
engage_to_clust = pd.DataFrame(engage_to_clust, columns = ['Salary','C_value','Total_Premium'])

table = engage_to_clust
k = 3

sse = {}
kmeans = KMeans(n_clusters=k, 
            random_state=0,
            n_init = 1,
            init=init_centroids,
            max_iter = 500).fit(table)
table["cluster"] = kmeans.labels_


print("Inertia:",np.round(kmeans.inertia_,decimals=2))



engage_clustered = my_scaler.inverse_transform(X=engage_to_clust.drop(columns="cluster"))
engage_clustered = pd.DataFrame(engage_clustered, columns = ['Salary','C_value','Total_Premium'])
engage_clustered["cluster"] = engage_to_clust["cluster"]

# add claims rate

engage_clustered['Claims_rate'] = engage.Claims_rate

cluster_freq(engage_clustered,"cluster")
engage_clusters = pd.DataFrame(pd.DataFrame(engage_clustered.groupby('cluster').mean()))
print (np.round(engage_clusters,decimals=2))

engage_clusters.mean()

'''
# see best cluster method: hier or k means with hier
zero = engage_clustered.loc[engage_clustered.cluster == 0]
zero = zero [['Salary','C_value','Total_Premium']]


centro = engage_clusters[['Salary','C_value','Total_Premium']].values[0]
valores = zero.values

dist = 0
for value in valores:
  dist = dist + distance.euclidean(centro,value)

dist = np.round(dist,decimals=2)
print(dist)

'''

variable = 'Salary'

sns.boxplot (y = variable, x = "cluster", data =engage_clustered ,showmeans=True)



# Cluster frequency

cluster_freq(engage_clustered,"cluster")


# visualize 

table = engage_clustered
x = "Salary"
y = "Total_Premium"
hue = "cluster"

plot2d(table,x,y,hue)


engage_clustered.boxplot(column=['C_value'])



#K-Means 3D

table = engage_clustered
z = "Total_Premium"
y = "C_value"
x = "Salary"

x = table[x]
y = table[y]
z = table[z]
c = "cluster"

c = table[c]


trace1 = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=12,
        color=c,
        colorscale = 'Viridis',
        opacity=0.8
        
    )
)

data = [trace1]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig)
















