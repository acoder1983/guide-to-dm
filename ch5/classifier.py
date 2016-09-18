import numpy as np
import pandas as pd
import unittest as ut


def classifyAll(trainData, testData, numCols, checkCol):
    '''
    return correctness
    '''

    # train data
    trainMeds = []
    trainMads = []
    trainModData = pd.DataFrame(columns=numCols)
    for col in numCols:
        med = trainData[col].median()
        mad = trainData[col].mad()
        trainModData[col] = (trainData[col] - med) / mad
        trainMeds.append(med)
        trainMads.append(mad)

    # mod test data
    testModData = pd.DataFrame(columns=numCols)
    for x in xrange(len(numCols)):
        testModData[numCols[x]] = (
            testData[numCols[x]] - trainMeds[x]) / trainMads[x]

    # classify
    corrects = 0.0
    for idx, testObj in testModData.iterrows():
        trainIdx = (trainModData - testObj).abs().T.sum().idxmin()
        if testData[checkCol][idx] == trainData[checkCol][trainIdx]:
            corrects += 1
    return corrects


def bucketData(dataSet, clsCol, bucNum):
    bucketDataSet = []
    for x in xrange(bucNum):
        d = pd.DataFrame(columns=dataSet.columns)
        bucketDataSet.append(d)

    clsValues = dataSet[clsCol].unique()
    clsBucIdxs = clsValues - clsValues
    for i, row in dataSet.iterrows():
        clsIdx = np.where(clsValues == row[clsCol])[0][0]
        bucIdx = clsBucIdxs[clsIdx]
        bucketDataSet[bucIdx] = bucketDataSet[bucIdx].append(row)
        if bucIdx == bucNum - 1:
            bucIdx = 0
        else:
            bucIdx += 1
        clsBucIdxs[clsIdx] = bucIdx
    return bucketDataSet


def mergeData(dataSet, excludeIdx):
    data = None
    for x in xrange(len(dataSet)):
        if data is None:
            data = dataSet[x]
        elif x != excludeIdx:
            data = data.append(dataSet[x])
    return data


class Classifier(ut.TestCase):

    def testMpg(self):
        dataSet = pd.read_table('mpgTrainingSet.txt',
                                sep=' +', engine='python')
        bucketDataSet = bucketData(dataSet, 'class', 10)
        corrects = 0.0
        for x in xrange(len(bucketDataSet)):
            trainData = mergeData(bucketDataSet, x)
            testData = bucketDataSet[x]
            corrects += classifyAll(trainData, testData, [
                'num1', 'num2', 'num3', 'num4', 'num5'], 'class')
        print corrects, len(dataSet), corrects / len(dataSet)
        self.assertTrue(
            corrects / len(dataSet) > 0.53)
