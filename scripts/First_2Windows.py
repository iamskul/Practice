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
PERIOD_OF_TIME 			= 1200 # Seconds 
outfileW1 			= open("RunningMeanDataW1.csv", "w" )
outfileW2 			= open("RunningMeanDataW2.csv", "w" )
outfileLiveData 		= open("RunningLiveRate.csv", "w" )

###################################
# 1. Geting Window Size - Begin
###################################

if len(sys.argv) != 5 :
    print("Please input a valid window size !")
    print("<script> -window_size <val>")
    sys.exit()
elif len(sys.argv) == 5 :
    print("Window1 and Window2 sizes passed are - ", sys.argv[2], "and ", sys.argv[4]) 
    window1 			= int(sys.argv[2])
    window2 			= int(sys.argv[4])

###################################
# 1. Geting Window Size - End
###################################

###################################
# 2. Geting Info from COINBASE - Begin
###################################
def get_info():
    public_client 		= gdax.PublicClient()
    ticker	 		= public_client.get_product_ticker(product_id='LTC-USD')
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
    #running_meanPriceW1= []
    #running_meanPriceW2= []
    #runningDataValue	= []
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
        i += 1
        time.sleep(0.1)
    #runningDataValue.append(float(productPrice))
    outfileLiveData.write(str(productPrice))
    outfileLiveData.write("\n")
    #running_meanPriceW1.append( sum(data_streamPriceW1)/window1 )
    outfileW1.write(str(sum(data_streamPriceW1)/window1))
    outfileW1.write("\n")
    #running_meanPriceW2.append( sum(data_streamPriceW2)/window2 )
    outfileW2.write(str(sum(data_streamPriceW2)/window2))
    outfileW2.write("\n")
    return(data_streamPriceW1, data_streamPriceW2)
    #return(running_meanPriceW1, data_streamPriceW1, running_meanPriceW2, data_streamPriceW2, runningDataValue)

###################################
# 3. Calculating Initial running mean over window - End
###################################

###################################
# 4. Adding elements from stream and getting running mean - Begin
###################################

#running_meanPriceW1, data_streamPriceW1, running_meanPriceW2, data_streamPriceW2, runningDataValue = initialRunningMean()
data_streamPriceW1, data_streamPriceW2 = initialRunningMean()
#print(" Getting initial data for both window sizes ")
#print( data_streamPriceW1, data_streamPriceW2 )
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
    data_streamPriceW1.append(float(productPrice))
    data_streamPriceW2.append(float(productPrice))
    outfileW1.write(str(sum(data_streamPriceW1)/window1))
    outfileW1.write("\n")
    outfileW2.write(str(sum(data_streamPriceW2)/window2))
    outfileW2.write("\n")
    #outfileLiveData.write(str(productPrice))
    outfileLiveData.write(productPrice)
    outfileLiveData.write("\n")
    #running_meanPriceW1.append(sum(data_streamPriceW1)/window1)
    #running_meanPriceW2.append(sum(data_streamPriceW2)/window2)
    #runningDataValue.append(str(productPrice))
    #print( data_streamPriceW1, running_meanPriceW1, data_streamPriceW2, running_meanPriceW2, runningDataValue )
    #print( data_streamPriceW1, data_streamPriceW2 )
    if time.time() > startTime + PERIOD_OF_TIME : 
        print("BREAKING DUE TO USER SPECIFIED TIME-OUT !")
        break

###################################
# 4. Adding elements from stream and getting running mean - End
###################################

outfileW1.close()
outfileW2.close()
outfileLiveData.close()

########################### Graph Plotting Experiment ########################


FILENAMES = ["RunningLiveRate.csv", "RunningMeanDataW1.csv", "RunningMeanDataW2.csv"]
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
    else :
        plt.plot(x,y, c='g', label='Running Mean W2')
        #plt.scatter(x,y, c='g', label='Running Mean W2')
plt.show()
