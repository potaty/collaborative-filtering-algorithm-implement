import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import math 
import scipy.io

header = ['user_id', 'movie_id', 'genre_id', 'review_id', 'movie_rating', 'date']

f = pd.read_csv('CIAO/movie-ratings.txt', sep = ',', names = header)
print f

n_users = f.user_id.unique().shape[0]
n_items = f.movie_id.unique().shape[0]

print n_users, n_items

# split train and test data
train_data, test_data = ms.train_test_split(f, test_size = 0.20)

# initialize data
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[5]


# calculate similarity
user_similarity = cosine_similarity(train_data_matrix)

# calculate RMSD
result = 0.0

count = 0
for line in test_data.itertuples():
	count += 1
	print count
	user, movie, rating = line[1] - 1, line[2] - 1, line[5]
	similarity = user_similarity[user].copy()
	median = np.median(similarity)
	valid_ratings_count = sum(map(lambda(idx, x): x if train_data_matrix[idx][movie] > 0 and x > median else 0, enumerate(similarity)))
	predict = sum(map(lambda(idx, x): x * train_data_matrix[idx][movie] if x > median else 0, enumerate(similarity))) / valid_ratings_count if valid_ratings_count != 0 else \
			  sum(train_data_matrix[user]) / sum(map(lambda(x): 1 if x != 0 else 0, enumerate(train_data_matrix[user])))
	result += (predict - rating) ** 2
result /= len(test_data)
result = math.sqrt(result)
print result
