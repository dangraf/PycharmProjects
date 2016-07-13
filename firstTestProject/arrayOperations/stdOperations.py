import numpy as np


# converts an array to % where first value in array represents 100%
def arrayToPercent( inputArray ):
    startValue = inputArray[0]
    temp = inputArray-startValue
    temp = temp/startValue*100
    return temp

# calculates euclidian distance between two arrays of equal size
def getDist( inputData,matchData ):
    ret = inputData - matchData
    ret = np.multiply(ret,ret)
    ret = np.sum(ret,axis=1)
    ret = np.exp(-ret)
    return ret;
# Normalizes an array where min value represents of 0 and max value of 1
def normalize(inputArray):
    myMin = np.amin(inputArray)
    myMax = np.amax(inputArray)
    temp = inputArray-myMin
    diff = myMax-myMin
    temp = np.divide(temp,diff)
    return temp


def  findMinDistance(inputData,matchData):
    # calculates the number of
     len = matchData.shape[1]
     numSteps = inputData.shape[1] - len+1
     matchData = normalize(matchData)
     error = []
     for i in range(numSteps):
         endIndex = i + len
         indata = inputData[:,i:endIndex]
         indata = normalize( indata )
         tempError = getDist( indata,matchData )
         if i == 0:
            error = tempError
         else:
             error = np.append(error,tempError,axis = 1)

         print i

     return np.max(error,axis=1)
