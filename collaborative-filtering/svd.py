from google.colab import drive
import pandas as pd
import numpy as np
from surprise.model_selection import cross_validate
from surprise.prediction_algorithms import SVD
from surprise.prediction_algorithms import KNNWithMeans, KNNBasic, KNNBaseline
from surprise.model_selection import GridSearchCV
from surprise import Reader, Dataset

base_url = '.'
output_path = 'output.txt'

ratings = pd.read_csv(base_url + "/MovieRating.txt", sep=" ")
genres = pd.read_csv(base_url + "/Genre.txt", sep=" ")

genre_movie_dict = dict()
for movie, row in genres.iterrows():
  genre = genres.loc[movie]['Genre']
  arr = genre_movie_dict.get(genre, [])
  arr.append(movie)
  genre_movie_dict[genre] = arr

user_list = []
rating_list = []
movie_list = []

# rating data frame
for user, row in ratings.iterrows():
  for movie in range(1, 61):
    if ratings.loc[user]['Movie' + str(movie)] != -1:
      user_list.append(int(user.split("User")[1]))
      rating_list.append(float(ratings.loc[user]['Movie' + str(movie)]))
      movie_list.append(movie)
rating_df = pd.DataFrame(data = {
    "userId": user_list,
    "movieId": movie_list,
    "rating": rating_list
})

reader = Reader()
data = Dataset.load_from_df(rating_df,reader)
dataset = data.build_full_trainset()

# grid search to find the best args
params = {'n_factors' :[5,10,20,50,100], # 10 classes in movie genre dataset
         'reg_all':[0.02,0.05,0.1]}
svd = GridSearchCV(SVD,param_grid=params,n_jobs=-1)
svd.fit(data)

print(svd.best_score)
print(svd.best_params)

# found the best arg, 100 and 0.02
svd = SVD(n_factors=100, reg_all=0.02)
svd.fit(dataset)

new_ratings = ratings.copy(deep=True)
for user, row in ratings.iterrows():
  for movie in range(1, 61):
    movie_name = 'Movie' + str(movie)
    if ratings.loc[user][movie_name] == -1:
      # use predict by SVD
      new_ratings.loc[user][movie_name] = float(svd.predict(int(user.split("User")[1]), movie, verbose=False).est)

      # if this user had rated the same genre then average it with the SVD predict value
      genre = genres.loc[movie_name]['Genre']
      rating_count = 0.0
      count = 0
      # iterate all movies with the same genre
      for similar_movie in genre_movie_dict[genre]:
        if ratings.loc[user][movie_name] != -1:
          count += 1
          rating_count += ratings.loc[user][movie_name]
      if count != 0:
        same_genre_rating = rating_count / count
        new_ratings.loc[user][movie_name] = (new_ratings.loc[user][movie_name] + same_genre_rating) / 2
with open(output_path, 'w') as f:
    f.write(
        new_ratings.to_string(header = False, index = False)
    )
