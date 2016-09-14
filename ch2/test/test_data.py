import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import unittest as ut

from data import *


class TestData(ut.TestCase):

    def test(self):
        columns = list('ABCD')
        rows = 6
        dates = pd.date_range('20130101', periods=rows)
        df = pd.DataFrame(np.arange(len(columns) * rows).reshape(
            rows, len(columns)), index=dates, columns=columns)

        self.assertEqual(df['B']['20130101'], 1)

        self.assertEqual(60, df['A'].sum())
        self.assertEqual(6, df.loc['20130101'].sum())

    def testRatings(self):
        self.assertEqual(5, ratings['Angelica']['Phoenix'])
        self.assertTrue(np.isnan(ratings['Bill']['Norah Jones']))
        self.assertEqual(1, ratings['Chan']['Deadmau5'])
        self.assertEqual(4.5, ratings['Dan']['Slightly Stoopid'])
        self.assertTrue(np.isnan(ratings['Hailey']['Phoenix']))
        self.assertEqual(4, ratings['Jordyn']['Vampire Weekend'])
        self.assertEqual(2, ratings['Sam']['Broken Bells'])
        self.assertEqual(3, ratings['Veronica']['Blues Traveler'])
