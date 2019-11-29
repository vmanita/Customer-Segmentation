# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 20:12:35 2018

@author: vitor
"""

# cluster frequency plot

def cluster_freq(table, column):
    print("\n")
    df = pd.DataFrame({"Absolute freq":table[column].value_counts(),
                       "Relative freq": np.round(table[column].value_counts()/len(table)*100,decimals=2)})
    print(df)
    plt.subplots(figsize=(7, 3))
    sns.countplot(x=table[column], data=table, palette="Oranges")
    sns.despine(left='False') 
    plt.show()
    
# 2 D clustering plot

def plot2d(table,x,y,hue=None):
    plt.figure(figsize=(15,7))
    plt.title ("Clusters", loc = "left",fontweight = "bold")
    sns.scatterplot(x=x, y=y, hue=hue,data=table, palette='Paired')
    plt.tick_params(labelsize=12)
    plt.xlabel(x,fontsize=12)
    plt.ylabel(y,fontsize=12)    
    plt.show()
    
    
# correlations
    
def corr(table):
    table = table.corr()
    mask = np.zeros_like(table)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        plt.figure(figsize = (10,5))
        sns.heatmap(table, 
                xticklabels=table.columns.values,
                yticklabels=table.columns.values,
                linewidths=0.1, annot= True,mask=mask,square=False)
    plt.show()
    
# k means elbow
 
def kmeans_elb(table, k):
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
    clusters_df = pd.DataFrame({"num_clusters":cluster_range,
                            "cluster_errors":cluster_errors})
    print (clusters_df)
    print("")
    print("Inertia:",np.round(kmeans.inertia_,decimals=2))
    
    
# dendogram
 
def dendo(table, method = 'ward', p = 40, line = 0):
    Z = linkage(table,
                method = 'ward')#method='single, complete
    plt.subplots(figsize=(8, 8))   
    dendrogram(Z,
               #truncate_mode='none',
               truncate_mode='lastp',
               p=p,
               orientation = 'top',
               leaf_rotation=45.,
               leaf_font_size=10.,
               show_contracted=True,
               show_leaf_counts=True)
        
    plt.title ("Truncated Hierarchical Clustering Dendrogram", loc = "left",fontweight = "bold")
    plt.axhline(y=line, color = "salmon", linestyle = "--")
    plt.xlabel('')
    plt.ylabel('Distance',fontsize=12)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.tick_params(labelsize=12)
    plt.show()
    
    
# DONUT

def donut_plt(names,pop,table,nrow):
    group_names=names
    group_size=pop
    subgroup_names=names
    subgroup_size=table[nrow]
    # colors
    a, b, c,d,e=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Oranges, plt.cm.Greys] 
    # outside
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.3,textprops={'fontsize': 14},colors=[a(0.6), b(0.6), c(0.6),d(0.6),e(0.6)], wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' } )
    plt.setp( mypie, width=0.3, edgecolor='white')
    
    # labels=group_names
    # Inside
    mypie2, _ = ax.pie(subgroup_size, radius=1.3-0.2, labeldistance=0.8, colors=[a(0.6), b(0.6), c(0.6),d(0.6),e(0.6)], wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' })
    plt.setp( mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    plt.show()

        

