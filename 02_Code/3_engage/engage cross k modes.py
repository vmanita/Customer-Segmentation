# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 19:59:36 2018

@author: vitor
"""

df = pd.DataFrame(columns=["c_id"])
df.c_id = engage.c_id
#df.set_index("c_id",drop=True,inplace=True)

#kmode_label = pd.read_csv('/Users/Manita/OneDrive - NOVAIMS/DM/project/3_engage/kmodes.csv',sep=',')
kmode_label = pd.read_csv('C:\\Users\\vitor\\OneDrive - NOVAIMS\\DM\\project\\3_engage\\kmodes.csv',sep=',')
df['kmode_cluster']=kmode_label.kmode_cluster

df = pd.concat([df,engage_clustered.cluster],axis=1)
df.columns = ["c_id","kmode_cluster","engage_cluster"]

#teste = engage[['Child','High_Educ','Living_Area']]

#teste['kmode'] = df.kmode_cluster

#teste.groupby(['kmode']).apply(pd.DataFrame.mode).reset_index(drop=True)


# give names to clusters

# engage
df['engage_cluster'].replace(to_replace=0, value='Wealthier', inplace=True)
df['engage_cluster'].replace(to_replace=1, value='Most_valuable', inplace=True)
df['engage_cluster'].replace(to_replace=2, value='Less_valuable', inplace=True)

# kmodes
df['kmode_cluster'].replace(to_replace=0, value='high_educ_la1', inplace=True)
df['kmode_cluster'].replace(to_replace=1, value='high_child', inplace=True)
df['kmode_cluster'].replace(to_replace=2, value='low_educ_child', inplace=True)



print(df.groupby(['engage_cluster']).size())
print(df.groupby(['engage_cluster','kmode_cluster']).size())


c1 = pd.DataFrame({'count' : df.groupby( [ "engage_cluster"] ).size()}).reset_index()
c2 = pd.DataFrame({'count' : df.groupby( [ "engage_cluster", "kmode_cluster"] ).size()}).reset_index()

c1_count = c1['count'].values

    
to_divide = pd.DataFrame({'to_divide':np.column_stack((c1_count, c1_count,c1_count)).flatten()})


c2 = pd.concat([c2,to_divide],axis=1)


# table with percentage of each k mode cluster in engage clusters
c2['kmode_freq'] = np.round(np.divide(c2['count'].values,c2.to_divide)*100,decimals = 1)

print(c2)



crosstable =pd.crosstab(df['engage_cluster'], df['kmode_cluster']).apply(lambda r: r/r.sum(), axis=1)

crosstable.plot.bar(figsize=(10, 7),colormap="Oranges",edgecolor = "black",linewidth = 1,rot=0)
#plt.legend() -> array com nomes dos clusters
plt.legend(title = "Kmode cluster",loc = 0)
plt.title ("Describing Engage", loc = "left",fontweight = "bold")
plt.ylabel("Nro. Clients", fontsize = 12)
plt.tick_params(labelsize=12)
plt.show()


















