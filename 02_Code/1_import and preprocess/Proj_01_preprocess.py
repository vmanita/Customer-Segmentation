#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#******************************************************************************
# Cleaning Data
#******************************************************************************
# Don't remove more than 3% of the data
#******************************************************************************
 
# MISSING DATA

# Join tables in a single df -> data

data = engage.merge(lob,on='c_id')

engage.describe()
data.describe()

# Visualize missing values
#plt.style.use('dark_background')
#plt.style.use('seaborn-notebook')
msno.matrix(data,figsize=(10, 5),fontsize=12)
plt.show()

# Birthday
# 1997 rows where birthday is after the first year policy

len(data.loc[data['Birthday'] > data['First_Policy_Year']])

# remove birthday
data.drop(columns=['Birthday'],inplace=True)

# There is one client year equal to 53784.0
# remove it

data.loc[data['First_Policy_Year']>2000.0]
data.drop(index=9294,inplace=True)

# Fill Life and work compensate with mean

fill_life = np.mean(data.Life)
fill_work_comp = np.mean(data.Work_compensate)

data.loc[data.Life.isnull(),"Life"] = fill_life
data.loc[data.Work_compensate.isnull(),"Work_compensate"] = fill_work_comp

# number of deleteds
# add 1 for the first policy year error deleted

n_del = np.sum(data.isnull().sum())+1
n_tot = len(data)

print(data.isnull().sum())

print("\nTotal data deleted:",
      n_del,
      "\n\nPercentage of data deleted:",
      np.round((len(data)-len(data.dropna()))/n_tot*100,decimals=2),"%")

data.dropna(inplace=True)

#Split data df into lob and engage

lob = data.drop(columns=["First_Policy_Year",
              "Educ","Salary",
              "Living_Area",
              "Child",
              "C_value",
              "Claims_rate"])

engage = data.drop(columns=['Motor',
                           'Household',
                           'Health',
                           'Life',
                           'Work_compensate'])

#******************************************************************************
# Describe
#******************************************************************************

lob.info()

engage.info()

# Engage****************

# Educ
# Child
# Living_Area
'''
variable="Educ"
print(np.round(engage[variable].value_counts()/len(engage)*100,decimals=2))
f, ax = plt.subplots(figsize=(7, 3))
sns.countplot(x=variable, data=engage, color="c")
plt.tick_params(labelsize=12)
plt.ylabel("Nro. Clients",fontsize = 13)
plt.xlabel("")
plt.title (variable, loc = "left",fontweight = "bold")
plt.show()
'''

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.countplot(x='Child', data=engage, color="c")
plt.ylabel("Nro. Clients",fontsize = 13)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Child', loc = "left",fontweight = "bold")
#
plt.subplot(1, 3, 2)
sns.countplot(x='Educ', data=engage, color="c")
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.ylabel("")
plt.title ('Educ', loc = "left",fontweight = "bold")

#
plt.subplot(1, 3, 3)
sns.countplot(x='Living_Area', data=engage, color="c")
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.ylabel("")
plt.title ('Living_Area', loc = "left",fontweight = "bold")
plt.tight_layout()
plt.show()




# Change Education
engage.loc[engage['Educ'] == '1 - Basic', 'Educ'] = 1.
engage.loc[engage['Educ'] == '2 - High School', 'Educ'] = 2.
engage.loc[engage['Educ'] == '3 - BSc/MSc', 'Educ'] = 3.
engage.loc[engage['Educ'] == '4 - PhD', 'Educ'] = 4.


# Visualize Customers by year
policy_year=engage['First_Policy_Year'].value_counts()
policy_year.sort_index(inplace=True)

years = []
n_customers=[]
for item in policy_year.index.values:
    years.append(int(item)-1900)
for item in policy_year.values:
    n_customers.append(item)

cust_by_year = {'years': years, 'n_customers': n_customers}
cust_by_year = pd.DataFrame(data=cust_by_year)
cust_by_year.set_index("years",inplace=True)

plt.subplots(figsize=(10,5))
plt.xlabel("Years",fontsize = 13)
plt.ylabel("N clients", fontsize = 13)
plt.title ("Clients per year", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.plot(cust_by_year,color="c",linewidth=4)
plt.show()

# lob****************

lob.drop(columns="c_id").boxplot(figsize=(10,8),grid=False)
plt.title ("Lob boxplot", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.show()

# Engage****************

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
engage[['Salary']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Salary', loc = "left",fontweight = "bold")
#
plt.subplot(1, 3, 2)
engage[['C_value']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('C_value', loc = "left",fontweight = "bold")

#
plt.subplot(1, 3, 3)
engage[['Claims_rate']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Claims_rate', loc = "left",fontweight = "bold")
plt.tight_layout()
plt.show()



#******************************************************************************
# Outliers
#******************************************************************************

# engage

##########
#visualize
##########

# Total_Premium
# Salary
# C_value
# Claims_rate

variable= "Salary"
# boxplot**

plt.subplots(figsize=(5, 5))
sns.boxplot(engage[variable],orient="v",linewidth=2,palette="Blues")
plt.show()


f, axes = plt.subplots(2, 2, figsize=(15,15), sharex=True)
sns.distplot( engage["Salary"] , color="skyblue", ax=axes[0, 0])
sns.distplot( engage["Claims_rate"] , color="olive", ax=axes[0, 1])
sns.distplot( engage["C_value"] , color="gold", ax=axes[1, 1])
plt.show()

plt.subplots(figsize=(10, 7))
sns.distplot( engage.Salary , color="skyblue")
plt.show()


# distplot**
'''

sns.distplot(engage[variable],kde=False,bins=100)
plt.show()
'''

#Outliers ID

# c_value era -5000
outliers = list(engage.loc[engage["C_value"]<-2000]['c_id'])

outliers=np.append(outliers,
                   list(engage.loc[engage["Salary"]>20000]['c_id']))


outliers=np.append(outliers,
                   list(engage.loc[engage["Claims_rate"]>50]['c_id']))



#lob

##########
#visualize
##########

#Motor
#Household
#Health
#Life
#Work_compensate

#boxplot**
variable= "Work_compensate"

plt.subplots(figsize=(5, 5))
sns.boxplot(lob[variable],orient="v",linewidth=2,palette="Blues")
plt.show()


# Outliers ID

outliers=np.append(outliers,
                   list(lob.loc[lob["Motor"]>2000]['c_id']))

outliers=np.append(outliers,
                   list(lob.loc[lob["Household"]>2000]['c_id']))

outliers=np.append(outliers,
                   list(lob.loc[lob["Health"]>5000]['c_id']))

'''
outliers=np.append(outliers,
                   lob.loc[lob["Life"]>375].index.values)
#rever life
'''
outliers=np.append(outliers,
                   list(lob.loc[lob["Work_compensate"]>750]['c_id']))



# Unique IDs
outliers = set(outliers)

len(outliers)

# set a df apart with outliers

lob_outliers = lob.copy()
engage_outliers = engage.copy()

lob_outliers = lob_outliers.loc[lob_outliers['c_id'].isin(outliers)]
engage_outliers = engage_outliers.loc[engage_outliers['c_id'].isin(outliers)]


# delete outliers

for outlier in outliers:
    engage = engage[engage.c_id != outlier]
    lob = lob[lob.c_id != outlier]
    n_del+= 1
  
print("\nTotal data deleted:",
      n_del,
      "\n\nPercentage of data deleted:",
      np.round(n_del/n_tot*100,decimals=2),"%")
       

# after

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
engage[['Salary']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Salary', loc = "left",fontweight = "bold")
#
plt.subplot(1, 3, 2)
engage[['C_value']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('C_value', loc = "left",fontweight = "bold")

#
plt.subplot(1, 3, 3)
engage[['Claims_rate']].boxplot(figsize=(10,8),grid=False)
plt.tick_params(labelsize=12)
plt.xlabel("")
plt.title ('Claims_rate', loc = "left",fontweight = "bold")
plt.tight_layout()
plt.show()



lob.drop(columns="c_id").boxplot(figsize=(10,8),grid=False)
plt.title ("Lob boxplot", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.show()



#******************************************************************************
# Add New Variables
#******************************************************************************

#------
#Engage
#------

engage['Total_Premium'] = lob[['Motor','Household','Health','Life','Work_compensate']].sum(axis=1)
engage_outliers['Total_Premium'] = lob_outliers[['Motor','Household','Health','Life','Work_compensate']].sum(axis=1)


engage["High_Educ"]=0
engage_outliers["High_Educ"] = 0

engage.loc[(engage.Educ == 3.) | (engage.Educ == 4.), "High_Educ"] = 1.
engage_outliers.loc[(engage_outliers.Educ == 3.) | (engage_outliers.Educ == 4.), "High_Educ"] = 1.
# years as customer (2016 is the reference)

engage["years_as_cust"] = 2016. - engage["First_Policy_Year"]
engage_outliers["years_as_cust"] = 2016. - engage_outliers["First_Policy_Year"]

#data['R_salary_premiums'] = data['Salary']/data['Total_Premium']
#data['R_cvalue_crate'] = data['C_value']/data['Claims_rate']

engage.drop(columns=["Educ","First_Policy_Year"],inplace=True)
engage_outliers.drop(columns=["Educ","First_Policy_Year"],inplace=True)

#------
#lob
#------

lob['R_Motor'] = lob['Motor']/engage['Total_Premium']*100
lob['R_Household'] = lob['Household']/engage['Total_Premium']*100
lob['R_Health'] = lob['Health']/engage['Total_Premium']*100
lob['R_Life'] = lob['Life']/engage['Total_Premium']*100
lob['R_Work_compensate'] = lob['Work_compensate']/engage['Total_Premium']*100

lob_outliers['R_Motor'] = lob_outliers['Motor']/engage_outliers['Total_Premium']*100
lob_outliers['R_Household'] = lob_outliers['Household']/engage_outliers['Total_Premium']*100
lob_outliers['R_Health'] = lob_outliers['Health']/engage_outliers['Total_Premium']*100
lob_outliers['R_Life'] = lob_outliers['Life']/engage_outliers['Total_Premium']*100
lob_outliers['R_Work_compensate'] = lob_outliers['Work_compensate']/engage_outliers['Total_Premium']*100

# use ratios

lob.drop(columns=['Motor','Household','Health','Life','Work_compensate'],
             inplace=True)
lob_outliers.drop(columns=['Motor','Household','Health','Life','Work_compensate'],
             inplace=True)

# check distribution

lob.drop(columns="c_id").boxplot(figsize=(15,8),grid=False)
plt.title ("Lob boxplot", loc = "left",fontweight = "bold")
plt.tick_params(labelsize=12)
plt.show()

# reset indexes

lob.reset_index(drop=True,inplace=True)
engage.reset_index(drop=True,inplace=True)

lob_outliers.reset_index(drop=True,inplace=True)
engage_outliers.reset_index(drop=True,inplace=True)





















































