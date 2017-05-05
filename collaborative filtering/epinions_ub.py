import numpy as np
import pandas as pd
from sklearn import cross_validation as cv



header = ['user_id', 'item_id', 'rating']
f = pd.read_csv('epinions_ratings_data.txt', sep = ' ', names = header)

n_users = 49290
n_items = 139738

train_data, test_data = cv.train_test_split(f, test_size = 0.20)

train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
print train_data_matrix

test_data_matrix = np.zeros((n_users, n_items))
for line in test_data_matrix.itertuples():
	test_data_matrix[line[1] - 1, line[2] - 1] = line[3]

user_similarity = pairwise_distances(train_data_matrix, metric = 'cosine')

print user_similarity



