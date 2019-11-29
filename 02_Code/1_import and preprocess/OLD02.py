#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#******************************************************************************
# Normalize Data
#******************************************************************************

# 1-hot encoding
'''
engage = pd.get_dummies(data = engage,
                        columns=['Living_Area'],
                        drop_first = True)

   
engage.rename(index = str, columns = {'Living_Area_2.0':'LA_2',
                                      'Living_Area_3.0':'LA_3',
                                      'Living_Area_4.0':'LA_4'},inplace = True )


engage[["LA_2","LA_3","LA_4"]] = engage[["LA_2","LA_3","LA_4"]]/3    
'''
# Normalize engage
    
my_scaler = preprocessing.StandardScaler()
scaled_data_engage = my_scaler.fit_transform(engage)    
 
scaled_engage = pd.DataFrame(scaled_data_engage,
                          index=engage.index,
                          columns=engage.columns)
  
