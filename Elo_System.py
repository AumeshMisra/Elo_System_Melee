import pandas as pd
import numpy as np

data = pd.read_csv("Elo_System_Matrix.csv")
data = data.drop("Unnamed: 0", axis = 1)

#Create a correlation matrix of winning/losing 
#Probabilities between players
for i in range(len(data)):
    for j in range(len(data.ix[i])):
        if (pd.isnull(data.iloc[i,j])):
            data.ix[i,j] = 1 - data.ix[j,i] 

#print (len(data.columns))