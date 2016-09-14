import numpy as np
import pandas as pd


class Recommender:

    def __init__(self, ratings):
        self.ratings = ratings
        self.items = ratings.columns
        self.users = ratings.index
        # compute dev
        self.devs = pd.DataFrame(
            columns=self.items, index=self.items, data=np.nan)
        self.cnts = pd.DataFrame(columns=self.items, index=self.items)
        for i in xrange(self.items.size):
            for j in xrange(i, self.items.size):
                userRateCnt = 0
                dev = 0.0
                itemI = self.items[i]
                itemJ = self.items[j]
                for k in xrange(self.users.size):
                    if not(np.isnan(self.ratings[itemI][k])) and not(np.isnan(self.ratings[itemJ][k])):
                        dev += self.ratings[itemI][k] - self.ratings[itemJ][k]
                        userRateCnt += 1
                if userRateCnt > 0:
                    self.devs[itemI][j] = dev / userRateCnt
                    self.devs[itemJ][i] = -dev / userRateCnt
                else:
                    self.devs[itemJ][j] = np.nan
                    self.devs[itemI][i] = np.nan
                self.cnts[itemI][itemJ] = self.cnts[itemJ][itemI] = userRateCnt

        print self.devs
        print self.cnts

    def getDev(self, item1, item2):
        return self.devs[item1][item2]

    def getCnt(self, item1, item2):
        return self.cnts[item1][item2]

    def recommend(self, user):
        # find not rated item in user
        # predict the non-rating
        results = []
        for itm in self.items:
            if np.isnan(self.ratings[itm][user]):
                rating = 0.
                cnt = 0
                for itmI in self.items:
                    c = self.cnts[itm][itmI]
                    if itm != itmI and c > 0:
                        rating += (self.ratings[itmI][user] +
                                   self.devs[itm][itmI]) * c
                        cnt += c
                if cnt > 0:
                    results.append((itm, rating / cnt))
        return results
