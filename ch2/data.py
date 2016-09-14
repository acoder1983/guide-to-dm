import numpy as np
import pandas as pd

bands = ['Blues Traveler', 'Broken Bells', 'Deadmau5', 'Norah Jones',
         'Phoenix', 'Slightly Stoopid', 'The Strokes', 'Vampire Weekend']

users = ['Angelica', 'Bill', 'Chan', 'Dan',
         'Hailey', 'Jordyn', 'Sam', 'Veronica']

ratings = pd.DataFrame(columns=users, index=bands)
ratings['Angelica'] = [3.5, 2, np.nan, 4.5, 5, 1.5, 2.5, 2]
ratings['Bill'] = [2, 3.5, 4, np.nan, 2, 3.5, np.nan, 3]
ratings['Chan'] = [5, 1, 1, 3, 5, 1, np.nan, np.nan]
ratings['Dan'] = [3, 4, 4.5, np.nan, 3, 4.5, 4, 2]
ratings['Hailey'] = [np.nan, 4, 1, 4, np.nan, np.nan, 4, 1]
ratings['Jordyn'] = [np.nan, 4.5, 4, 5, 5, 4.5, 4, 4]
ratings['Sam'] = [5, 2, np.nan, 3, 5, 4, 5, np.nan]
ratings['Veronica'] = [3, np.nan, np.nan, 5, 4, 2.5, 3, np.nan]
