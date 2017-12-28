#!/usr/bin/python3

import gdax
import time
import timeit
import threading
import numpy
import sys, getopt
import numpy as np
import matplotlib.pyplot as plt

startTime 			= time.time()
PERIOD_OF_TIME 			= 3600 # Seconds 
outfileW1 			= open("RunningMeanDataW1.csv", "w" )
outfileW2 			= open("RunningMeanDataW2.csv", "w" )
outfileW3 			= open("RunningMeanDataW3.csv", "w" )
outfileLiveData 		= open("RunningLiveRate.csv", "w" )
DECISION 			= open("Decision.csv", "w" )

crossoverVal			= 0
crossoverCount			= 0
buyOrderVal			= 0
sellOrderVal			= 0
sellMaxVal			= 0
BuyOrderLog			= []
SellOrderLog			= []

###################################
# 1. Geting Window Size - Begin
###################################

if len(sys.argv) != 7 :
    print("Please input a valid window1, window2 and window3 size !")
    print("<script> -window_size <val>")
    sys.exit()
elif len(sys.argv) == 7 :
    print("Window1 Window2 and Window3 sizes passed are - ", sys.argv[2], "and ", sys.argv[4], "and ", sys.argv[6]) 
    window1 			= int(sys.argv[2])
    window2 			= int(sys.argv[4])
    window3 			= int(sys.argv[6])

###################################
# 1. Geting Window Size - End
###################################

###################################
# 2. Geting Info from COINBASE - Begin
###################################
def get_info():
    public_client 		= gdax.PublicClient()
    ticker	 		= public_client.get_product_ticker(product_id='BTC-USD')
    productPrice 		= ticker.get('price')
    return(productPrice)
    
###################################
# 2. Geting Info from COINBASE - End
###################################

###################################
# 3. Calculating Initial running mean over window - Begin
###################################

def initialRunningMean():
    data_streamPriceW1	= []
    data_streamPriceW2	= []
    data_streamPriceW3	= []
    i = 0
    while i < window1 :
        productPrice = get_info()
        while True :
            if productPrice == None :
                print("Getting new data, since productPrice is - None ")
                productPrice = get_info()
            else :
                break
        data_streamPriceW1.append(float(productPrice))
        if i >= (window1 - window2):
            data_streamPriceW2.append(float(productPrice)) 
        if i >= (window1 - window3):
            data_streamPriceW3.append(float(productPrice)) 
        i += 1
        time.sleep(3)
    outfileLiveData.write(str(productPrice))
    outfileLiveData.write("\n")
    outfileW1.write(str(sum(data_streamPriceW1)/window1))
    outfileW1.write("\n")
    outfileW2.write(str(sum(data_streamPriceW2)/window2))
    outfileW2.write("\n")
    outfileW3.write(str(sum(data_streamPriceW3)/window3))
    outfileW3.write("\n")
    return(data_streamPriceW1, data_streamPriceW2, data_streamPriceW3)
    #return(running_meanPriceW1, data_streamPriceW1, running_meanPriceW2, data_streamPriceW2, runningDataValue)

###################################
# 3. Calculating Initial running mean over window - End
###################################

###################################
# 4. Adding elements from stream and getting running mean - Begin
###################################

#running_meanPriceW1, data_streamPriceW1, running_meanPriceW2, data_streamPriceW2, runningDataValue = initialRunningMean()
data_streamPriceW1, data_streamPriceW2, data_streamPriceW3 = initialRunningMean()
#print(" Getting initial data for both window sizes ")
print( data_streamPriceW1, data_streamPriceW2, data_streamPriceW3 )
#print( data_streamPriceW1, running_meanPriceW1, data_streamPriceW2, running_meanPriceW2, runningDataValue )

while True :
    productPrice = get_info()
    while True :
        if productPrice == None :
            print("Getting new data, since productPrice is - None ")
            productPrice = get_info()
        else :
            break
    data_streamPriceW1.pop(0)
    data_streamPriceW2.pop(0)
    data_streamPriceW3.pop(0)
    data_streamPriceW1.append(float(productPrice))
    data_streamPriceW2.append(float(productPrice))
    data_streamPriceW3.append(float(productPrice))
    outfileW1.write(str(sum(data_streamPriceW1)/window1))
    outfileW1.write("\n")
    outfileW2.write(str(sum(data_streamPriceW2)/window2))
    outfileW2.write("\n")
    outfileW3.write(str(sum(data_streamPriceW3)/window3))
    outfileW3.write("\n")
    #outfileLiveData.write(str(productPrice))
    outfileLiveData.write(productPrice)
    outfileLiveData.write("\n")
    if int(sum(data_streamPriceW1)/window1) == int(sum(data_streamPriceW3)/window3) and crossoverCount < 10 :
        crossoverCount += 1
    elif int(sum(data_streamPriceW1)/window1) == int(sum(data_streamPriceW3)/window3) and crossoverCount == 10 and BuyOrderLog == [] and int(buyOrderVal) == 0 :
        DECISION.write(" Begining Crossover and Buy Quote at - ")
        DECISION.write(productPrice)
        DECISION.write("\n")
        BuyOrderLog.append(float(productPrice))
        crossoverCount = 0
        buyOrderVal = float(productPrice)
    elif int(sum(data_streamPriceW1)/window1) == int(sum(data_streamPriceW3)/window3) and crossoverCount == 10 and BuyOrderLog != [] and abs(int(buyOrderVal) - int(sum(data_streamPriceW1)/window1)) > 3 and int(buyOrderVal) != 0 :
        DECISION.write(" Crossover Sell of quotes - ")
        SellOrderLog = [i for i in BuyOrderLog if i < int(sum(data_streamPriceW3)/window3)]
        BuyOrderLog = [i for i in BuyOrderLog if i >= int(sum(data_streamPriceW3)/window3)]
        BuyOrderLog.sort()
        for i in SellOrderLog : 
            DECISION.write(str(i)) 
            DECISION.write(" for value of :-") 
            DECISION.write(productPrice) 
            DECISION.write(" ") 
        DECISION.write("\n")
        DECISION.write(" Crossover Buy at - ")
        DECISION.write(productPrice)
        DECISION.write("\n")
        BuyOrderLog.append(float(productPrice))
        BuyOrderLog.sort()
        crossoverCount = 0
        buyOrderVal = float(productPrice)
    else :
        crossoverCount = 0
    if time.time() > startTime + PERIOD_OF_TIME : 
        print("BREAKING DUE TO USER SPECIFIED TIME-OUT !")
        break

###################################
# 4. Adding elements from stream and getting running mean - End
###################################

outfileW1.close()
outfileW2.close()
outfileW3.close()
outfileLiveData.close()
DECISION.close()

########################### Graph Plotting Experiment ########################


FILENAMES = ["RunningLiveRate.csv", "RunningMeanDataW1.csv", "RunningMeanDataW2.csv", "RunningMeanDataW3.csv"]
for filename in FILENAMES :
    print(filename)
    with open(filename) as f:
        data = f.read()
    data = data.split('\n')
    x = list(range(1, len(data)))
    y = [row for row in data]
    y.pop(len(data)-1)
    if filename == FILENAMES[0] :
        plt.plot(x,y, c='r', label='The Data')
        #plt.scatter(x,y, c='r', label='The Data')
    elif filename == FILENAMES[1] :
        plt.plot(x,y, c='b', label='Running Mean W1')
        #plt.scatter(x,y, c='b', label='Running Mean W1')
    elif filename == FILENAMES[2] :
        plt.plot(x,y, c='y', label='Running Mean W2')
        #plt.scatter(x,y, c='b', label='Running Mean W1')
    else :
        plt.plot(x,y, c='g', label='Running Mean W3')
        #plt.scatter(x,y, c='g', label='Running Mean W2')
plt.show()
