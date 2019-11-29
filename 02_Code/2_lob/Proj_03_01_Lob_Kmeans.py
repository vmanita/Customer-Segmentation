# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:30:15 2018

@author: vitor
"""

#******************************************************************************
#K-means
#******************************************************************************

# Correlations
corr(lob)

# Remove R_Household -> correlation with R_Motor= -0.8

lob_to_clust = lob.copy().drop(columns=['c_id','R_Household'])

# normalize lob 

my_scaler = preprocessing.StandardScaler() #StandardScaler
lob_to_clust = my_scaler.fit_transform(lob_to_clust)

lob_to_clust=pd.DataFrame(lob_to_clust, columns =  lob.copy().drop(columns=['c_id','R_Household']).columns)
########

lob_to_clust.boxplot(figsize=(8,8),grid=False)

lob_to_clust.describe()

# elbow graph
table = lob_to_clust
k=10
cluster_range = range(1,k+1)
cluster_errors = []
sse = {}
for k in cluster_range:
    kmeans = KMeans(n_clusters=k, 
                random_state=0,
                n_init = 10,
                max_iter = 300).fit(table)
    table["cluster"] = kmeans.labels_
    #print(data["clusters"])
    sse[k] = kmeans.inertia_
    cluster_errors.append(kmeans.inertia_)
    # Inertia: Sum of distances of samples to their closest cluster center
plt.figure(figsize=(10,7))
plt.plot(list(sse.keys()), list(sse.values()),
         linewidth=1.5,
         markeredgecolor="r",
         color = "black")
plt.title ("Elbow Graph", loc = "left",fontweight = "bold")
plt.xlabel("Nro. cluster", fontsize=12)
plt.ylabel("SSE", fontsize=12)
plt.tick_params(labelsize=12)
plt.show()


print("")
print("Inertia:",np.round(kmeans.inertia_,decimals=2))


# Check the clusters
lob_clustered = lob.copy().drop(columns=['R_Household'])
lob_clustered = pd.concat([lob_clustered,lob_to_clust.cluster],axis=1)

lob_clusters = pd.DataFrame(pd.DataFrame(lob_clustered.drop(columns="c_id").groupby('cluster').mean()))
print (lob_clusters)

# Cluster frequency

cluster_freq(lob_to_clust,"cluster")



# visualize 

table = lob_clustered
x = "R_Motor"
y = "R_Household"
hue = "cluster"

plot2d(table,x,y,hue)



















