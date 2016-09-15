import numpy as np
import pandas as pd
import unittest as ut


def normVector(vec):
    med = vec.median()
    mad = vec.mad()
    return ((vec - med) / mad, med, mad)


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def classifyAll(trainData, testData, numCols, checkCol):
    '''
    return correctness
    '''

    # train data
    trainMeds = []
    trainMads = []
    trainModData = pd.DataFrame(columns=numCols)
    for col in numCols:
        ret = normVector(trainData[col])
        trainModData[col] = ret[0]
        trainMeds.append(ret[1])
        trainMads.append(ret[2])

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
    print corrects, testData[checkCol].size
    return corrects / testData[checkCol].size


class Classifier(ut.TestCase):

    def testSport(self):
        '''
        test with data to get classify accuracy
        '''
        # train data to get standard value and median and ab sd
        trainData = pd.read_csv('sport-train.csv')
        testData = pd.read_csv('sport-test.csv')
        correctness = classifyAll(trainData, testData, [
                                  'Height', 'Weight'], 'Sport')
        self.assertTrue(
            abs(correctness - 0.8) < 1e-3)

    def testIris(self):
        trainData = pd.read_csv('irisTrainingSet.data')
        testData = pd.read_csv('irisTestSet.data')
        correctness = classifyAll(trainData, testData, [
                                  'num1', 'num2', 'num3', 'num4', ], 'class')
        self.assertTrue(
            abs(correctness - 0.933) < 1e-3)
