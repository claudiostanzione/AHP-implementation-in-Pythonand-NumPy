# -*- coding: utf-8 -*-


import numpy as np
import os
from numpy import genfromtxt
import sys
import csv

def checkmatrixreciproc(matrix):# control if the matrix is ok
    for i in range(matrix.shape[0]):
        matrix[i][i]=1 # if not, set diagonal with 1
        for j in range(matrix.shape[1]):
            if np.isnan(matrix[i][j])==True: #check if the value is nan, if yes
                matrix[i][j]=1/matrix[j][i]#set the reciprocal value
            if matrix[i][j]==0:#same control of the nan with the 0
                matrix[i][j]= 1/matrix[j][i]
    np.asarray(matrix) # transform the matrix in array
    return matrix

def consistencymatrix(matri,pv): # check the consistency of the matrix
    rc=open("rcivalues.csv")# open the rci table
    rci= genfromtxt(rc,delimiter=",")
    rci[0]=0 #set the first value of the table if there are problems in the reading
    consist= matri*pv #Multiply each value in the first column of the comparison matrix 
    weightedsum= np.sum(consist, axis=1) #Add the values in each row to obtain a set of values called weighted sum
    lambdamax= (np.sum(weightedsum/pv))/len(pv) #calculate lambdamax
    ci=(lambdamax-len(pv))/(len(pv)-1)
    cr= ci/rci[len(pv)-1]  
    if not cr >= 0.10: 
        print("Consistency ratio = ", cr, "\n")
        print("Consistency OK")
    else:
        print("Revise the comparison matrix")
        ask= int(input("If you prefer to continue digit 1, else digit 0 \n")) #the user is able to exit if he wants to repair the comparison matrix
        if ask==0: 
            sys.exit("Good revision")

def readnames(name): # read the csv file for the tables with the names
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for riga in csv_reader:
            print(riga)
    return riga 
           
start= input("provide the file name of criteria \n")
startname= input("provide the file name of criteria names \n")
print("\n")
data11= genfromtxt(start, delimiter=',') 
data1=checkmatrixreciproc(data11)
criterianormalized= data1/np.sum(data1, axis=0) # calculate the values of criteria normalized
print ("Matrix normalized: \n",criterianormalized, "\n")
criteriapv = np.mean(criterianormalized, axis=1) # calculate the priority vector
print("The priority vector of criteria is the following: \n")
readnames(startname)
print(criteriapv, "\n")
consistencymatrix(data1, criteriapv)
i=0
pvmed= np.array([])
cartel= input("provide the folder name of alternative comparison \n")# read the name of the cartel with set of file with comparison among alternatives
altname= input("provide the file name of alternatives name \n")
for name in os.listdir(cartel):#scroll in the cartel with file of alternative comparison
    i=i+1
    data2 = np.array([])
    data2= genfromtxt(os.getcwd()+"\\"+cartel+"\\"+name, delimiter=",")#read the file in the cartel
    data2=checkmatrixreciproc(data2)
    weicrialt= np.mean((np.divide(data2,np.sum(data2,axis=0))),axis=1)#obtain the priority of each alternative for each criteria
    weicrialt= np.asarray(weicrialt) 
    pvmed=np.append(pvmed,weicrialt)
x=int((len(pvmed))/i)#calculate the index for the reshape
pvfinal= np.reshape(pvmed,(i,x))#reshape the array in rows and columns that need
for i in range (len(criteriapv)):
    pvfinal[i]=np.dot(pvfinal[i],criteriapv[i])# preparation for weighting of priorities
pvfinal=np.transpose(pvfinal)# transposing the array for the final calculation of overall
overall=np.sum(pvfinal,axis=1)
b=readnames(altname)
print("")
print("Overall: \n",overall, "\n")
a=np.argmax(overall)#search the index of best value
print("The best alternative is: ",b[a]," with a final score of ",overall[a]*100, " out of 100.")

