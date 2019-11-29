# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 19:29:54 2018

@author: vitor
"""
x = lob.drop(columns="c_id").copy()



my_scaler = preprocessing.StandardScaler()
scaled_x = my_scaler.fit_transform(x)    
 
scaled_x = pd.DataFrame(scaled_x,
                          index=x.index,
                          columns=x.columns)


table = scaled_x
n_components = 2

pca = PCA(n_components= n_components)

principalComponents = pca.fit_transform(table)

# Explained variance by each component

pca_board = pd.DataFrame({"Explained_Var":np.round(pca.explained_variance_ratio_*100,decimals=1),
                          "Cumulative_Var":np.round(np.cumsum(pca.explained_variance_ratio_*100),decimals= 2)})
pca_board.index.name = 'PC'
pca_board.index += 1 

print (pca_board)


# elbow graph

plt.figure(figsize=(10,7))
plt.plot(pca_board.Explained_Var, color = "black", label = "explained variance",linewidth=2)
plt.xlabel('Nro. components', fontsize = 13)
plt.ylabel('Explained Var')
plt.title ("Lob PCA elbow graph", loc = "left",fontweight = "bold")
plt.xticks(np.arange(1, n_components+1, 1))
#plt.axvline(x = 3, alpha = 0.8, color = "salmon", linestyle = "--", label = "cumulative explained var > 80%")
plt.legend()
plt.tick_params(labelsize=12)
plt.show()

# Revert PCA effect
# pca.inverse_transform(principalComponents)

pca_index= []

for i in range(1,n_components+1):
    pca_index.append('PC'+str(i))
    
print (pd.DataFrame(np.round(pca.components_,decimals=2),
                    columns=x.columns,
                    index = pca_index))

lob_pca = pd.DataFrame(principalComponents,
                     columns = pca_index)





'''
PC1 -- -Motor 
PC2 -- +Health -Household
PC3 -- + Life + Work compensate
'''



lob_to_clust=lob_pca.copy()

# elobw graph

kmeans_elb(lob_to_clust, 3)

k = 3
table = lob_to_clust
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
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()

######################## 4 clusters

lob_clusters = pd.DataFrame(kmeans.cluster_centers_,columns=lob_to_clust.columns)

lob_clustered = lob_pca.copy()

lob_clustered.loc[lob_clustered.index==lob_clustered.index,"lob_cluster"] = lob_to_clust["cluster"]

print(lob_clustered.groupby(['lob_cluster']).mean())


# compare with mean

print("\Absolute frequency of each cluster:\n")
print(lob_to_clust["cluster"].value_counts())
print("\nRelative frequency of each cluster:\n")
print(np.round(lob_to_clust["cluster"].value_counts()/
               len(lob_to_clust)*100,
               decimals=2))
plt.subplots(figsize=(7, 3))
sns.countplot(x=lob_to_clust["cluster"], data=lob_to_clust, palette="Oranges")
sns.despine(left='False') 
plt.show()

# define function for cluster frequency

def cluster_freq(table, column):
    print("\n")
    df = pd.DataFrame({"Absolute freq":table[column].value_counts(),
                       "Relative freq": np.round(table[column].value_counts()/len(table)*100,decimals=2)})
    print(df)
    plt.subplots(figsize=(7, 3))
    sns.countplot(x=table[column], data=table, palette="Oranges")
    sns.despine(left='False') 
    plt.show()
    
cluster_freq(engage_to_clust,"clusters")


# Visualize

table = lob_clustered
x = "PC1"
y = "PC2"
hue = "lob_cluster"

plot2d(table,x,y,hue)












