import numpy as np
import pandas as pd

header = ['user_id', 'item_id', 'rating']
f = pd.read_csv('epinions_ratings_data.txt', sep = ' ', names = header)

n_users = 49290
n_items = 139738


