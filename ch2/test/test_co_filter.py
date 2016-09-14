import pandas as pd
import numpy as np
import unittest as ut

import sys
sys.path.append('../')
from data import *
from co_filter import *


class TestCoFilter(ut.TestCase):

    def testManhattan(self):
        self.assertEqual(2.0, manhattan(
            ratings['Hailey'], ratings['Veronica']))
        self.assertEqual(7.5, manhattan(
            ratings['Hailey'], ratings['Jordyn']))

    def testRecommend(self):
        expect = [('Blues Traveler', 3.0), ('Phoenix', 4.0),
                  ('Slightly Stoopid', 2.5)]
        self.assertEqual(expect, recommend('Hailey'))

        expect = [('Deadmau5', 1.0)]
        self.assertEqual(expect, recommend('Sam'))

        expect = []
        self.assertEqual(expect, recommend('Angelica'))

    def testPearson(self):
        expect = 1.0
        rating1 = [4.75, 4.5, 5, 4.25, 4]
        rating2 = [4, 3, 5, 2, 1]
        self.assertTrue(abs(expect - pearson(rating1, rating2)) < 1e-5)

        expect = -0.90405349906826993
        self.assertTrue(
            abs(expect - pearson(ratings['Angelica'], ratings['Bill'])) < 1e-5)

        expect = 1.0
        rating1 = np.arange(100)
        rating2 = rating1 + 100
        self.assertTrue(abs(expect - pearson(rating1, rating2)) < 1e-5)

    def testCossim(self):
        expect = 0.935
        rating1 = [4.75, 4.5, 5, 4.25, 4]
        rating2 = [4, 3, 5, 2, 1]
        self.assertTrue(abs(expect - cossim(rating1, rating2)) < 1e-2)

if __name__ == '__main__':
    ut.main()
