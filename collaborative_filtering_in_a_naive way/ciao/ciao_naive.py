import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import cosine_similarity
import cosine_distance
from scipy import sparse
import math 
import scipy.io

header = ['user_id', 'movie_id', 'genre_id', 'review_id', 'movie_rating', 'date']

f = pd.read_csv('CIAO/movie-ratings.txt', sep = ',', names = header)
print f

n_users = f.user_id.unique().shape[0]
n_items = f.movie_id.unique().shape[0]

user_dict = {}
movie_dict = {}

for i in xrange(n_users):
	user_dict[i] = {}

for i in xrange(n_items):
	movie_dict[i] = {}

print n_users, n_items

# split train and test data
train_data, test_data = ms.train_test_split(f, test_size = 0.20)

# initialize data
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[5]
	user_dict[line[1] - 1][line[2] - 1] = 1
	movie_dict[line[2] - 1][line[1] - 1] = 1


# calculate similarity
user_similarity = np.zeros((n_users, n_users))

for i in xrange(n_users):
	for j in xrange(n_users):
		user_similarity[i, j] = cosine.exactly_cosine(train_data_matrix[i], train_data_matrix[j])

print user_similarity

# calculate RMSD
result = 0.0

count = 0
for line in test_data.itertuples():
	# print count
	user, movie, rating = line[1] - 1, line[2] - 1, line[5]
	similarity = user_similarity[user].copy()
	median = np.median(similarity)
	predict = 0.0
	valid_ratings_count = sum(map(lambda(idx, x): x if train_data_matrix[idx][movie] > 0 and x > median else 0, enumerate(similarity)))
	if valid_ratings_count != 0:
		predict = sum(map(lambda(idx, x): x * train_data_matrix[idx][movie] if x > median else 0, enumerate(similarity))) / (valid_ratings_count)
	if predict < 1.0 or predict != predict:
		predict = sum(train_data_matrix[user]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[user]))
	if predict < 1.0 or predict != predict:
		predict = sum(train_data_matrix[:, movie]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[:, movie]))
	if predict != predict:
		predict = 2.5
	result += (predict - rating) ** 2
result /= len(test_data)
result = math.sqrt(result)
print result
