import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import pairwise_distances
from scipy import sparse


header = ['user_id', 'item_id', 'rating', 'time_stamp']
f = pd.read_table('movielens100k.txt', names = header)

print f

n_users = 943
n_items = 1682

train_data, test_data = ms.train_test_split(f, test_size = 0.20)

train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
print train_data_matrix
print 1

test_data_matrix = np.zeros((n_users, n_items))
for line in test_data.itertuples():
	test_data_matrix[line[1] - 1, line[2] - 1] = line[3]
print 2

user_similarity = pairwise_distances(sparse.dia_matrix(train_data_matrix), metric = 'cosine')

print 3
print user_similarity



