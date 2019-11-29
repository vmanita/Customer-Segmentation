#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 17:52:22 2018

@author: Manita
"""

# loop para ver a distancia para cada cluster e juntar ao mais próximo


from scipy.spatial import distance

# outliers are in array -> outliers

lob_outliers

engage_outliers

# lob clusters
#print(distance.euclidean(Most_valuable, Less_valuable)) # this one

lob_clusters

outliers
        
# total table
        
centroids = total.groupby(['lob_cluster','engage_cluster']).mean().drop(columns='c_id')

centroids[1:2]


tuple_df = pd.DataFrame()
for i in outliers:
    tuplo = [0,0]
    d=10000000000
    counter = 0
    j = 0
    for index,centroid in centroids.iterrows():
         
        dist = np.round(distance.euclidean(i,list(centroid)),decimals=4)
        #print('id:',i,'distance:',dist)
        
        if dist<d:
            tuplo=centroids.index.values[counter]
            client_id = i
            d = dist
        counter +=1
    #print('id:',i,'nearest cluster is\t',tuplo)
    new_row = [i,tuplo]
    #print(new_row)
    tuple_df=tuple_df.append([new_row])

tuple_df.reset_index(drop=True,inplace=True)
tuple_df.columns=['c_id','cgroup']


# 1 index -> lob
# 2 index -> engage

for index,row in tuple_df.iterrows():
    tuple_df.loc[index,'lob_cluster'] =tuple_df.cgroup[index][0]
    tuple_df.loc[index,'engage_cluster'] =tuple_df.cgroup[index][1]


total
# c_id /engage/engage cluster/lob/lob cluster

engage_outliers_clustered = pd.concat([engage_outliers,tuple_df.engage_cluster],axis=1)
lob_outliers_clustered = pd.concat([lob_outliers,tuple_df.lob_cluster],axis=1)

outliers_clustered = pd.merge(engage_outliers_clustered, lob_outliers_clustered, on='c_id')


total = total.append(outliers_clustered, ignore_index=True)


# crosstable
df = total.copy()
df['lob_cluster'].replace(to_replace=0, value='Motor', inplace=True)
df['lob_cluster'].replace(to_replace=1, value='Average', inplace=True)
df['lob_cluster'].replace(to_replace=2, value='House_life_work', inplace=True)

# engage
df['engage_cluster'].replace(to_replace=0, value='Wealthier', inplace=True)
df['engage_cluster'].replace(to_replace=1, value='Most_valuable', inplace=True)
df['engage_cluster'].replace(to_replace=2, value='Less_valuable', inplace=True)


crosstable =pd.crosstab(df['lob_cluster'], df['engage_cluster'])
print(df.groupby(['lob_cluster','engage_cluster']).size())

# join 29 elements from to less valuable
df.loc[(df.lob_cluster == 'Average') & (df.engage_cluster == 'Most_valuable'),'engage_cluster'] = 'Less_valuable'

crosstable =pd.crosstab(df['lob_cluster'], df['engage_cluster'])
print(df.groupby(['lob_cluster','engage_cluster']).size())


crosstable.plot.bar(figsize=(10, 7),colormap="Oranges",edgecolor = "black",linewidth = 1,rot=0)
#plt.legend() -> array com nomes dos clusters
plt.legend(title = "Product cluster",loc = 0)
plt.title ("Clients per group", loc = "left",fontweight = "bold")
plt.xlabel("Value Cluster")
plt.ylabel("Number of Clients")
plt.show()



f, axes = plt.subplots(2, 2, figsize=(15,15), sharex=True)
sns.distplot( df["Salary"] , color="skyblue", ax=axes[0, 0])
sns.distplot( df["Total_Premium"] , color="olive", ax=axes[0, 1])
sns.distplot( df["C_value"] , color="gold", ax=axes[1, 1])
plt.show()


plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.distplot( df["Salary"] , color="skyblue")
plt.ylabel("Nro. Clients",fontsize = 13)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Salary', loc = "left",fontweight = "bold")
#
plt.subplot(1, 3, 2)
sns.distplot( df["Total_Premium"] , color="olive")
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.ylabel("")
plt.title ('Total_Premium', loc = "left",fontweight = "bold")

#
plt.subplot(1, 3, 3)
sns.distplot( df["C_value"] , color="gold")
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.ylabel("")
plt.title ('C_value', loc = "left",fontweight = "bold")
plt.tight_layout()
plt.show()

















