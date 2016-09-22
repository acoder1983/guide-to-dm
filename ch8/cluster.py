from __future__ import division
import numpy as np
import pandas as pd
import unittest as ut
from Queue import PriorityQueue


class ClusterBot:

    def train(self, dataSet, elemCol, attrCols):
        # norm the dataset
        dataSet.index = dataSet[elemCol]
        self.normDataSet = pd.DataFrame(
            columns=attrCols, index=dataSet.index)
        print attrCols
        for col in attrCols:
            self.normDataSet[col] = (
                dataSet[col] - dataSet[col].median()) / dataSet[col].mad()

        # gen dist priority queue
        self.queue = PriorityQueue()
        maxDist = 0.0
        for i in xrange(len(self.normDataSet)):
            for j in xrange(i + 1, len(self.normDataSet)):
                dist = 0.0
                for col in attrCols:
                    dist += (self.normDataSet.iloc[i][col] -
                             self.normDataSet.iloc[j][col])**2
                self.queue.put(
                    (np.sqrt(dist), (self.normDataSet.index[i], self.normDataSet.index[j])))

        # gen leaf cluster for every elem
        self.clusters = []
        for elem in self.normDataSet.index:
            c = Cluster(elem=elem)
            self.clusters.append(c)

        # process every dist pair in queue
        # find the clusters owns elems
        # the cluster should not be merged
        # merge the clusters into new bigger clusters
        # until the dist queue empty
        while self.queue.qsize() > 0:
            distPair = self.queue.get()
            elems = distPair[1]

            newCluster = Cluster()
            maxLevel = 0
            for e in elems:
                for c in self.clusters:
                    if not c.merged and c.hasElem(e):
                        newCluster.subClusters.append(c)
                        if c.level > maxLevel:
                            maxLevel = c.level
                        break
            if len(newCluster.subClusters) == len(elems) and newCluster.subClusters[0] != newCluster.subClusters[1]:
                newCluster.level = maxLevel + 1
                print elems, newCluster.level
                newCluster.resetSubLevels()
                self.clusters.append(newCluster)
                for c in newCluster.subClusters:
                    c.merged = True
                    c.parent = newCluster

    def getNormValue(self, elem, col):
        return self.normDataSet[col][elem]

    def getShortestDist(self):
        head = self.queue.get()
        self.queue.put(head)
        print self.queue
        return head[0]

    def getClustersByLevel(self, level):
        # get level in cluster tree
        maxLevel = self.clusters[len(self.clusters) - 1].level
        level = maxLevel - level
        n = 0
        clusters = {}
        for c in self.clusters:
            if c.level >= level:
                clusters[c] = c
        print len(clusters)

        # remove parents
        remClusters = {}
        for c in clusters:
            while not c.parent is None:
                remClusters[c.parent] = c.parent
                c = c.parent
        for c in remClusters:
            del clusters[c]
        return len(clusters)

    def getAllClusterNum(self):
        return len(self.clusters)


class Cluster:

    def __init__(self, elem=None, subClusters=None, level=0, merged=False, parent=None):
        self.elem = elem
        self.level = level
        self.merged = merged
        self.parent = parent
        if subClusters is None:
            self.subClusters = []

    def hasElem(self, elem):
        found = self.elem == elem
        for c in self.subClusters:
            found |= c.hasElem(elem)
        return found

    def resetSubLevels(self):
        for c in self.subClusters:
            c.level = self.level - 1
            c.resetSubLevels()

    def __str__(self):
        return '%s, %d, %d, %d' % (self.elem, len(self.subClusters), self.level, self.merged)


class TestClusterBot(ut.TestCase):

    def testDogs(self):
        dataSet = pd.read_csv('dogs.csv', engine='python')
        c = ClusterBot()
        c.train(dataSet, 'breed', ['height (inches)', 'weight (pounds)'])
        self.assertEqual(21, c.getAllClusterNum())

        # self.assertEqual(2, c.getClustersByLevel(1))
        # self.assertEqual(4, c.getClustersByLevel(2))
        self.assertEqual(5, c.getClustersByLevel(3))

if __name__ == '__main__':
    ut.main()
