import unittest as ut
from ib_filter import *
import numpy as np
import pandas as pd


class Test(ut.TestCase):

    def testSimple(self):
        columns = ['Taylor Swift', 'PSY', 'Whitney Houston']
        index = ['Amy', 'Ben', 'Clara', 'Daisy']
        ratings = pd.DataFrame(columns=columns, index=index)
        ratings['Taylor Swift'] = [4, 5, np.nan, 5]
        ratings['PSY'] = [3, 2, 3.5, np.nan]
        ratings['Whitney Houston'] = [4, np.nan, 4, 3]

        r = Recommender(ratings)
        self.assertIsNotNone(r.ratings)
        self.assertEqual(0, r.getDev('PSY', 'PSY'))
        self.assertEqual(2, r.getDev('Taylor Swift', 'PSY'))
        self.assertEqual(-1, r.getDev('Whitney Houston', 'Taylor Swift'))
        self.assertEqual(2, r.getCnt('Whitney Houston', 'Taylor Swift'))

        expect = [('Whitney Houston', 3.375)]
        self.assertEqual(expect, r.recommend('Ben'))

    def testComplex(self):
        t = pd.read_table('ml-100k/u.data')
        columns = t['item'].unique()
        # columns.sort()
        index = t['user'].unique()
        # index.sort()
        ratings = pd.DataFrame(columns=columns, index=index)
        data = []
        for x in xrange(columns.size * index.size):
            data.append(np.nan)
        ratings.data = np.array(data).reshape(index.size, columns.size)
        for x in xrange(t.size / t.columns.size):
            ratings[t.iloc[x]['item']][t.iloc[x]['user']] = t.iloc[x]['rate']
        self.assertEqual(1, ratings[377][22])
        self.assertTrue(np.isnan(ratings[1641][22]))

        expect = [('Aiqing wansui (1994)', 5.674418604651163),
                  ('Boys, Les (1997)', 5.523076923076923), ('Star Kid (1997)', 5.25)]
        r = Recommender(ratings)
        self.assertEqual(expect, r.Recommender(ratings['user'][25]))
