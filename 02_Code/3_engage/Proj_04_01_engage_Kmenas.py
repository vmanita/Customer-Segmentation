# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 15:05:40 2018

@author: vitor
"""

#******************************************************************************
#K-means
#******************************************************************************

corr(engage)

# Claims_rate is negatively correlated with customer value p = -0.92, remove it

engage_to_clust = engage.drop(columns=["c_id","Child","Claims_rate","Living_Area","High_Educ","years_as_cust"])
my_scaler = preprocessing.StandardScaler() #StandardScaler
engage_to_clust = my_scaler.fit_transform(engage_to_clust)


engage_to_clust=pd.DataFrame(engage_to_clust, columns = ['Salary','C_value','Salary'])
# elobw graph

table = engage_to_clust
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


engage_clusters = pd.DataFrame(kmeans.cluster_centers_,columns=engage_to_clust.columns)

engage_clustered = engage[['Salary','C_value','Total_Premium']].copy()

engage_clustered.loc[engage_clustered.index==engage_to_clust.index,"engage_cluster"] = engage_to_clust["clusters"]

print(engage_clustered.groupby(['engage_cluster']).mean())


# compare with mean

print("\Absolute frequency of each cluster:\n")
print(engage_to_clust["clusters"].value_counts())
print("\nRelative frequency of each cluster:\n")
print(np.round(engage_to_clust["clusters"].value_counts()/
               len(engage_to_clust)*100,
               decimals=2))
plt.subplots(figsize=(7, 3))
sns.countplot(x=engage_to_clust["clusters"], data=engage_to_clust, palette="Oranges")
sns.despine(left='False') 
plt.show()