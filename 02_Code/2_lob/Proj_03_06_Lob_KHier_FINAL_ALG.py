#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:52:39 2018

@author: Manita
"""

lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

#******************************************************************************
# normalize
#******************************************************************************

my_scaler = preprocessing.StandardScaler() #StandardScaler
lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)

Z = linkage(lob_to_clust,
            method = 'ward')#method='single, complete

dendo(lob_to_clust, line = 80, p =35)


#******************************************************************************
# Hierarchical
#******************************************************************************

lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

# normalize lob 

lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)

k=3

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity='euclidean',
                                      linkage='ward')

# Get clusters
my_HC = Hclustering.fit(lob_to_clust)

my_labels = pd.DataFrame(my_HC.labels_)
my_labels.columns =  ['cluster']

# lob clustered
lob_clustered = lob.copy()
lob_clustered = pd.concat([lob_clustered,my_labels],axis=1)

# lob clusters mean

lob_clusters = np.round(lob_clustered.groupby(['cluster']).mean(),decimals=2)
print(lob_clusters)

lob_clusters.mean()


# frequency 

cluster_freq(lob_clustered,"cluster")

# centroids

init_centroids=lob_clusters.copy().drop(columns=['c_id','R_Household']).values


#******************************************************************************
# K means
#******************************************************************************

# normalize lob 
lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)



table = lob_to_clust


kmeans = KMeans(n_clusters=k, 
            random_state=0,
            n_init = 1,
            init=init_centroids,
            max_iter = 300).fit(table)
table["cluster"] = kmeans.labels_


print("")
print("Inertia:",np.round(kmeans.inertia_,decimals=2))

##

lob_clusters = pd.DataFrame(pd.DataFrame(lob_to_clust.groupby('cluster').mean()))
print (lob_clusters)

# Cluster frequency

cluster_freq(lob_to_clust,"cluster")


# Lob_clustered -> Lob + clusters

lob_clustered = lob.copy()

lob_clustered = pd.concat([lob_clustered,lob_to_clust.cluster],axis=1)

print(np.round(lob_clustered.groupby(['cluster']).mean(),decimals=2))

lob_clustered.mean()


#################################################################################################################################################
# DONUT
plt.style.use('seaborn-white')

names = ['Motor','Household','Health','Life','Work']
pop_avg = lob_clustered[['R_Motor','R_Household','R_Health','R_Life','R_Work_compensate']].describe()[1:2].values[0]
donut = lob_clustered.groupby(['cluster'])['R_Motor','R_Household','R_Health','R_Life','R_Work_compensate'].mean().values

# 0 -> Health
# 1 -> Motor
# 2 -> Generic

donut_plt(names =names ,pop = pop_avg,table = donut,nrow = 1)

#################################################################################################################################################
# pie

labels = list(lob_to_clust["cluster"].value_counts().reset_index()['index'])
sizes = list(lob_to_clust["cluster"].value_counts().reset_index()['cluster'])

pieplt = pd.DataFrame({'labels':labels,'sizes':sizes})

pieplt.plot(kind='pie',y = 'sizes', subplots=False, figsize=(16,8), autopct='%1.0f%%')

'''
fig1, ax1 = plt.subplots(figsize=(6,6))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal') 

plt.show()
'''

# 2 d


table = lob_clustered
x = "R_Motor"
y = "R_Life"
hue = "cluster"

plot2d(table,x,y,hue)


#K-Means 3D

x = lob_clustered['R_Motor']
y = lob_clustered['R_Health']
z = lob_clustered['R_Life']

c = lob_clustered['cluster']


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















