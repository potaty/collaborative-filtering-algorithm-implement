import numpy as np
import pandas as pd
from sklearn import model_selection as ms
from sklearn.metrics.pairwise import cosine_similarity
import cosine
from scipy import sparse
import math
import scipy.io

header = ['user_id', 'movie_id', 'movie_rating']

f = pd.read_csv('CIAO/movie-ratings.txt', sep = ' ', names = header)
t = pd.read_csv('CIAO/trusts.txt', sep = ' ', names = ['u', 'v', 'trust'])

print f
n_users = f.user_id.max()
n_items = f.movie_id.max()

print n_users

user_dict = {}
movie_dict = {}
user_similarity = np.zeros((n_users, n_users))
fm1 = {}
fm2 = {}
fz = {}
predict_user = {}
predict_movie = {}
count_user = {}
count_movie = {}

for i in xrange(n_users):
	user_dict[i] = {}
	fm1[i] = {}
	fm2[i] = {}
	fz[i] = {}
	predict_user[i] = 0.0
	count_user[i] = 0

for i in xrange(n_items):
	movie_dict[i] = {}
	predict_movie[i] = 0.0
	count_movie[i] = 0

print n_users, n_items

# split train and test data
train_data, test_data = ms.train_test_split(f, test_size = 0.20)


count = 0

# initialize data
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
	train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
	user_dict[line[1] - 1][line[2] - 1] = 1
	movie_dict[line[2] - 1][line[1] - 1] = 1
	predict_user[line[1] - 1] += line[3]
	count_user[line[1] - 1] += 1
	predict_movie[line[2] - 1] += line[3]
	count_movie[line[2] - 1] += 1

for user in xrange(n_users):
	count += 1
	print count
	predict_user[user] = 1.0 * predict_user[user] / count_user[user] #sum(train_data_matrix[user]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[user]))

for movie in xrange(n_items):
	if count_movie[movie] != 0:
		predict_movie[movie] = 1.0 * predict_movie[movie] / count_movie[movie] #sum(train_data_matrix[:, movie]) / sum(map(lambda(x): 1 if x != 0 else 0, train_data_matrix[:, movie]))
	else:
		predict_movie[movie] = 4
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
	user_similarity[i][i] = 0.0
	for j in xrange(i + 1, n_users):
		if (fm1[i].get(j) == None or fm1[i].get(j) < 1e-10 or fm2[i].get(j) == None or fm2[i].get(j) < 1e-10):
			user_similarity[i][j] = 0.0
			user_similarity[j][i] = 0.0
		else:
			user_similarity[i][j] = (fz[i][j] / math.sqrt(fm1[i][j]) / math.sqrt(fm2[i][j]) + 1.0) / 2
			if (user_similarity[i][j] < 0):
				user_similarity[i][j] = 0.0
			user_similarity[j][i] = user_similarity[i][j]

for line in t.itertuples():
	u = line[1] - 1
	v = line[2] - 1
	user_similarity[u][v] = 1

# calculate RMSD
result = 0.0

count = 0
for line in test_data.itertuples():
	user, movie, rating = line[1] - 1, line[2] - 1, line[3]
	similarity = user_similarity[user].copy()
	median = 0.1
	arr = np.partition(similarity, n_users - 20)[n_users - 20:]
	predict = 0.0
	valid_ratings_count = sum(map(lambda(idx, x): x if train_data_matrix[idx][movie] > 0 and x > median else 0, enumerate(similarity)))
	if valid_ratings_count != 0:
		predict = sum(map(lambda(idx, x): x * train_data_matrix[idx][movie] if x > median else 0, enumerate(similarity))) / (valid_ratings_count)
	if predict < 1.0 or predict != predict:
		predict = predict_movie[movie]
	if predict < 1.0 or predict != predict:
		predict = predict_user[user]
	if predict != predict:
		predict = 4
		count += 1
	result += (predict - rating) ** 2
result /= len(test_data)
result = math.sqrt(result)
print result
