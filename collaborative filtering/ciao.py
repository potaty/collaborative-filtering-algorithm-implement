import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import cosine_similarity
import cosine
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
user_similarity = np.zeros((n_users, n_users))
fm1 = {}
fm2 = {}
fz = {}
predict_user = {}
predict_movie = {}

for i in xrange(n_users):
	user_dict[i] = {}
	fm1[i] = {}
	fm2[i] = {}
	fz[i] = {}

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

for user in xrange(n_users):
	predict_user[user] = sum(train_data_matrix[user]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[user]))

for movie in xrange(n_items):
	predict_movie[movie] = sum(train_data_matrix[:, movie]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[:, movie]))

# calculate similarity
# user_similarity = np.zeros((n_users, n_users))
for u1 in xrange(n_users):
	for movie in user_dict[u1].keys():
		for u2 in movie_dict[movie].keys():
			if u1 >= u2:
				continue
			x = 1.0 * train_data_matrix[u1][movie] - predict_user[u1]
			y = 1.0 * train_data_matrix[u2][movie] - predict_user[u2]
			if (fz[u1].get(u2) == None):
				fz[u1][u2] = 0.0
			fz[u1][u2] += x * y
			if (fm1[u1].get(u2) == None):
				fm1[u1][u2] = 0.0
			if (fm2[u1].get(u2) == None):
				fm2[u1][u2] = 0.0
			fm1[u1][u2] += x ** 2
			fm2[u1][u2] += y ** 2

for i in xrange(n_users):
	for j in xrange(i + 1, n_users):
		if (fm1[i].get(j) == None or fm1[i].get(j) < 1e-10 or fm2[i].get(j) == None or fm2[i].get(j) < 1e-10):
			user_similarity[i][j] = 0.0
			user_similarity[j][i] = 0.0
		else:
			user_similarity[i][j] = fz[i][j] / math.sqrt(fm1[i][j]) / math.sqrt(fm2[i][j])
			user_similarity[j][i] = user_similarity[i][j]

# calculate RMSD
result = 0.0

count = 0
for line in test_data.itertuples():
	user, movie, rating = line[1] - 1, line[2] - 1, line[5]
	similarity = user_similarity[user].copy()
	median = 0.2
	predict = 0.0
	valid_ratings_count = sum(map(lambda(idx, x): x if train_data_matrix[idx][movie] > 0 and x > median else 0, enumerate(similarity)))
	if valid_ratings_count != 0:
		predict = sum(map(lambda(idx, x): x * train_data_matrix[idx][movie] if x > median else 0, enumerate(similarity))) / (valid_ratings_count)
	if predict < 1.0 or predict != predict:
		predict = predict_user[user]
	if predict < 1.0 or predict != predict:
		predict = predict_movie[movie]
	if predict != predict:
		predict = 4
		count += 1
	result += (predict - rating) ** 2
	print predict, rating
result /= len(test_data)
print result
result = math.sqrt(result)
print result
print count
