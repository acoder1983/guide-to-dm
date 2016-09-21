from __future__ import division
import numpy as np
import pandas as pd
import unittest as ut


class NaiveBayesClassifier:

    def train(self, dataSet, attrCols, clsCol):
        self.attrCols = pd.Series(attrCols)
        self.clsValues = dataSet[clsCol].unique()

        self.pCls = []
        for x in xrange(self.clsValues.size):
            self.pCls.append(
                len(dataSet[dataSet[clsCol] == self.clsValues[x]]) / len(dataSet))

        self.pAttrs = []
        for attrCol in self.attrCols:
            attrs = dataSet[attrCol].unique()
            attrP = pd.DataFrame(columns=self.clsValues, index=attrs)
            for cls in self.clsValues:
                clsData = dataSet[dataSet[clsCol] == cls]
                for attr in attrs:
                    attrP[cls][attr] = len(
                        clsData[clsData[attrCol] == attr]) / len(clsData)
            self.pAttrs.append(attrP)

    def classify(self, params):
        # P(retCol|params)=P(params|retCol)*P(retCol)
        # maxArg(retCol)
        maxP = 0.0
        maxI = 0
        for i in xrange(self.clsValues.size):
            cls = self.clsValues[i]
            p = 1.0
            for j in xrange(self.attrCols.size):
                p *= self.pAttrs[j][cls][params[j]]
            p *= self.pCls[i]
            print cls, p
            if p > maxP:
                maxP = p
                maxI = i
        return self.clsValues[maxI]


class TestNaiveBayesClassifier(ut.TestCase):

    def testiHealth(self):
        dataSet = pd.read_table('iHealth/i-01',
                                header=None, engine='python')
        c = NaiveBayesClassifier()
        c.train(dataSet, [0, 1, 2, 3], 4)
        self.assertEqual(0.4, c.pCls[0])
        self.assertEqual(0.167, round(c.pAttrs[0]['i100']['health'], 3))
        self.assertEqual(0.333, round(c.pAttrs[0]['i100']['appearance'], 3))
        self.assertEqual(0.667, round(c.pAttrs[3]['i500']['yes'], 3))

        actual = c.classify(['health', 'moderate', 'moderate', 'yes'])
        self.assertEqual('i500', actual)
