#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:40:55 2018

@author: Manita
"""

x = engage[['Salary','C_value','Claims_rate','Total_Premium']].copy()

my_scaler = preprocessing.StandardScaler()
scaled_x = my_scaler.fit_transform(x)    
 
scaled_x = pd.DataFrame(scaled_x,
                          index=x.index,
                          columns=x.columns)
  

n_components = 2

pca = PCA(n_components= n_components)

principalComponents = pca.fit_transform(scaled_x)

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
plt.title ("Engage PCA elbow graph", loc = "left",fontweight = "bold")
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


engage_pca = pd.DataFrame(principalComponents,
                     columns = pca_index)




'''
we can retain 2 principal components
PC1 -- + C_value - Claims rate
PC2 -- - Salary + Total_Premium
'''


# k means on PCA

engage_to_clust=engage_pca.copy()

# elobw graph

sse = {}
for k in range(1, 5):
    kmeans = KMeans(n_clusters=k, 
                random_state=0,
                n_init = 15,
                max_iter = 300).fit(engage_to_clust)
    engage_to_clust["clusters"] = kmeans.labels_
    #print(data["clusters"])
    sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
plt.figure(figsize=(8,5))
plt.plot(list(sse.keys()), list(sse.values()),
         linewidth=1.5,
         linestyle="--",
         marker = "X",
         markeredgecolor="r",
         color = "black")
plt.title("Elbow Graph: Engage")
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()

######################## 4 clusters

engage_clusters = pd.DataFrame(kmeans.cluster_centers_,columns=engage_to_clust.columns)

engage_clustered = engage_pca.copy()

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

table = engage_to_clust
x = "PC1"
y = "PC2"
hue = "clusters"

plot2d(table,x,y,hue)



























