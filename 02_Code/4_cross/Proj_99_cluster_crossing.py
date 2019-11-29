#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 17:22:27 2018

@author: Manita
"""

#kmode_label = pd.read_csv('/Users/Manita/OneDrive - NOVAIMS/DM/project/3_engage/kmodes.csv',sep=',')
#kmode_label = pd.read_csv('C:\\Users\\vitor\\OneDrive - NOVAIMS\\DM\\project\\3_engage\\kmodes.csv',sep=',')
#df['kmode_cluster']=kmode_label.kmode_cluster

#queremos uma tabela grouped by valor e por produto e numero de clientes
df = pd.DataFrame(columns=["c_id"])
df.c_id = lob.c_id
#df.set_index("c_id",drop=True,inplace=True)

df = pd.concat([df,lob_clustered.cluster],axis=1)
df.reset_index(drop=True,inplace=True)
df = pd.concat([df,engage_clustered.cluster],axis=1)
df.columns = ["c_id","lob_cluster","engage_cluster"]

lob_clusters
engage_clusters

# give names to clusters
# lob
df['lob_cluster'].replace(to_replace=1, value='Motor', inplace=True)
df['lob_cluster'].replace(to_replace=0, value='Average', inplace=True)
df['lob_cluster'].replace(to_replace=2, value='House_life_work', inplace=True)

# engage
df['engage_cluster'].replace(to_replace=0, value='Wealthier', inplace=True)
df['engage_cluster'].replace(to_replace=1, value='Most_valuable', inplace=True)
df['engage_cluster'].replace(to_replace=2, value='Less_valuable', inplace=True)
'''
# kmodes
df['kmode_cluster'].replace(to_replace=0, value='high_educ_la1', inplace=True)
df['kmode_cluster'].replace(to_replace=1, value='high_child', inplace=True)
df['kmode_cluster'].replace(to_replace=2, value='low_educ_child', inplace=True)
'''


#group by
#print(df.groupby(['lob_cluster','engage_cluster', 'kmode_cluster']).size())

#df[['value_cluster', 'product_cluster',"Number_of_Clients"]].groupby(['value_cluster', 'product_cluster']).agg(['count'])

#visualize

'''
crosstable = pd.crosstab(df['lob_cluster'], [df['engage_cluster'],df['kmode_cluster']])

crosstable.to_csv("/Users/Manita/OneDrive - NOVAIMS/DM/project/crosstable.csv")
'''
pd.crosstab(df['lob_cluster'], df['engage_cluster']).apply(lambda r: r/r.sum()*100, axis=1)

print(df.groupby(['lob_cluster','engage_cluster']).size())

#################################################################################################
# complete data
#################################################################################################

# juntar por grupo de cliente ou por engage?

engage_copy = engage.copy()
engage_copy = pd.concat([engage_copy,engage_clustered.cluster],axis=1)

total = engage_copy.copy()
total=total.rename(columns = {'cluster':'engage_cluster'})

lob_copy = lob.copy()
lob_copy = pd.concat([lob_copy,lob_clustered.cluster],axis=1).drop(columns="c_id")

total = pd.concat([total,lob_copy],axis=1)
total=total.rename(columns = {'cluster':'lob_cluster'})


# set clusters with less than 100 customers to nearest cluster

total_copy = total.drop(columns=["engage_cluster","lob_cluster","c_id"])
total_scaled = my_scaler.fit_transform(total_copy)
total_scaled = pd.DataFrame(total_scaled, columns = total_copy.columns)
total_scaled = pd.concat([total_scaled,total[["engage_cluster","lob_cluster","c_id"]]],axis=1)

to_relocate = total_scaled.loc[(total_scaled.lob_cluster == 1) & (total_scaled.engage_cluster == 1)].drop(columns=["c_id","lob_cluster","engage_cluster"])
to_relocate_id =  total_scaled.loc[(total_scaled.lob_cluster == 1) & (total_scaled.engage_cluster == 1)]["c_id"].values

total_scaled = total_scaled.loc[~total_scaled["c_id"].isin(to_relocate_id)]


centroids = total_scaled.groupby(['lob_cluster','engage_cluster']).mean().drop(columns='c_id')


tuple_df = pd.DataFrame()
for i in to_relocate_id:
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

tuple_df.lob_cluster = tuple_df.lob_cluster.astype(int)
tuple_df.engage_cluster = tuple_df.engage_cluster.astype(int)
tuple_df['lob_cluster'].replace(to_replace=1, value='Motor', inplace=True)
tuple_df['lob_cluster'].replace(to_replace=0, value='Average', inplace=True)
tuple_df['lob_cluster'].replace(to_replace=2, value='House_life_work', inplace=True)
tuple_df['engage_cluster'].replace(to_replace=0, value='Wealthier', inplace=True)
tuple_df['engage_cluster'].replace(to_replace=1, value='Most_valuable', inplace=True)
tuple_df['engage_cluster'].replace(to_replace=2, value='Less_valuable', inplace=True)


df.loc[df.c_id.isin(to_relocate_id), 'lob_cluster'] = tuple_df.lob_cluster.values
df.loc[df.c_id.isin(to_relocate_id), 'engage_cluster'] = tuple_df.engage_cluster.values

print(df.groupby(['lob_cluster','engage_cluster']).size())

'''
distances = engage_to_clust.groupby(['cluster']).mean()


Wealthier = distances[:1]
Most_valuable = distances[1:2]
Less_valuable = distances[2:3]


# see what is the closest cluster to join most valuable

print(distance.euclidean(Most_valuable, Less_valuable)) # this one
print(distance.euclidean(Most_valuable, Wealthier))


df.loc[(df.lob_cluster == 'Motor') & (df.engage_cluster == 'Most_valuable'),'engage_cluster'] = 'Less_valuable'
'''

df['lob_cluster'].replace(to_replace='Average', value='Generic+Health', inplace=True)
df['lob_cluster'].replace(to_replace='House_life_work', value='Personal', inplace=True)


crosstable =pd.crosstab(df['lob_cluster'], df['engage_cluster'])
crosstable.plot.bar(figsize=(10, 7),colormap="Oranges",edgecolor = "black",linewidth = 1,rot=0)
#plt.legend() -> array com nomes dos clusters
plt.legend(title = "Product cluster",loc = 0)
plt.title ("Clients per group (Absolute frq)", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.ylabel("Nro. Clients",fontsize=12)
plt.xlabel("")
plt.show()

crosstable2 =pd.crosstab(df['lob_cluster'], df['engage_cluster']).apply(lambda r: r/r.sum()*100, axis=1)
crosstable2.plot.bar(figsize=(10, 7),colormap="Oranges",edgecolor = "black",linewidth = 1,rot=0)
#plt.legend() -> array com nomes dos clusters
plt.legend(title = "Product cluster",loc = 0)
plt.title ("Clients per group (Percentage)", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.ylabel("Percentage of Clients",fontsize=12)
plt.xlabel("")
plt.show()

######### engage description


engage_copy = engage.copy()
engage_copy = pd.concat([engage_copy,engage_clustered.cluster],axis=1)

engage_copy.groupby(['cluster']).mean()


#Child
#years_as_cust
#High_Educ
#Living_Area

engage_clusters

x = 'Child' 
sns.countplot(x=x, hue="cluster", data=engage_copy)



## all data

total = engage_copy.copy()
total=total.rename(columns = {'cluster':'engage_cluster'})

lob_copy = lob.copy()
lob_copy = pd.concat([lob_copy,lob_clustered.cluster],axis=1).drop(columns="c_id")

total = pd.concat([total,lob_copy],axis=1)
total=total.rename(columns = {'cluster':'lob_cluster'})


# export to csv


total.to_csv("/Users/Manita/OneDrive - NOVAIMS/DM/project/total.csv")







print(df.groupby(['lob_cluster','engage_cluster']).size())
























