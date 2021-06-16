import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import math 

header = ['user_id', 'item_id', 'rating', 'timestamp']
f = pd.read_table('movielens1m.txt', sep = '::',names = header)
print f

n_users = 6040
n_items = 3952

# split train and test data
train_data, test_data = ms.train_test_split(f, test_size = 0.20)

# initialize data
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[3]


# calculate similarity
user_similarity = cosine_similarity(train_data_matrix)

# calculate RMSD
result = 0.0

for line in test_data.itertuples():
	user, movie, rating = line[1] - 1, line[2] - 1, line[3]
	similarity = user_similarity[user].copy()
	predict = sum(map(lambda(idx, x): x * train_data_matrix[idx][movie] if x > 0.1 else 0, enumerate(similarity))) / sum(map(lambda(idx, x): x if train_data_matrix[idx][movie] > 0 and x > 0.1 else 0, enumerate(similarity)))
	if (predict != predict):
		predict = sum(train_data_matrix[user]) / sum(map(lambda(x): 1 if x != 0 else 0, enumerate(train_data_matrix[user])))
	result += (predict - rating) ** 2
result /= len(test_data)
result = math.sqrt(result)
print result
