from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

import pickle
import pandas as pd
import os
import numpy as np

current_dir = os.path.dirname(__file__)
UID = 0

with open(current_dir+'/Data/games.pkl', 'rb') as f:
    games = pickle.load(f)

with open(current_dir+'/Data/users.pkl', 'rb') as f:
    users = pickle.load(f)

with open(current_dir+'/Data/games_sort_most_played.pkl', 'rb') as f:
    games_sort_most_played = pickle.load(f)

with open(current_dir+'/Data/tfidf_unique_tags.pkl', 'rb') as f:
    tfidf_unique_tags = pickle.load(f)

with open(current_dir+'/Data/tfidf_duplicate_tags.pkl', 'rb') as f:
    tfidf_duplicate_tags = pickle.load(f)

with open(current_dir+'/Data/id_idx.pkl', 'rb') as f:
    id_idx = pickle.load(f)

with open(current_dir+'/Data/idx_id.pkl', 'rb') as f:
    idx_id = pickle.load(f)

with open(current_dir+'/Data/tfidf_feature_names.pkl', 'rb') as f:
    tfidf_feature_names = pickle.load(f)

with open(current_dir+'/Data/raw_features.pkl', 'rb') as f:
    raw_features = pickle.load(f)



def create_matrix(users):
  U = len(users['userId'].unique())
  A = len(users['AppID'].unique())

  uid_idx = pd.Series(data=range(U), index=users['userId'].unique())
  aid_idx = pd.Series(data=range(A), index=users['AppID'].unique())

  idx_uid = pd.Series(index=range(U), data=users['userId'].unique())
  idx_aid = pd.Series(index=range(A), data=users['AppID'].unique())

  user_index = [uid_idx[i] for i in users['userId']]
  app_index = [aid_idx[i] for i in users['AppID']]

  user_game_matrix = csr_matrix((users['rating'], (user_index, app_index)), shape=(U, A))
  game_user_matrix = user_game_matrix.transpose()

  return user_game_matrix, game_user_matrix, uid_idx, aid_idx, idx_uid, idx_aid

user_game_matrix, game_user_matrix, uid_idx, aid_idx, idx_uid, idx_aid = create_matrix(users)

def get_cosine_score(id, id_idx, matrix):
  if id not in id_idx.index:
    return None
  idx = id_idx[id]
  cosine_score = cosine_similarity(matrix[idx], matrix)
  return list(enumerate(cosine_score.flatten()))

def get_most_similar(id, id_idx, idx_id, matrix, n=10):
  cos_scores = get_cosine_score(id, id_idx, matrix)
  if cos_scores is None:
    return None
  cos_scores = sorted(cos_scores, key=lambda x: x[1], reverse=True)
  top_n_indices = [i[0] for i in cos_scores[1:n+1]]
  top_n_ids = [idx_id[i] for i in top_n_indices]
  return top_n_ids

def get_collaborative_recommendation(userId, uid_idx, idx_aid, matrix, n=10):
  if userId not in uid_idx.index:
    return None
  uidx = uid_idx[userId]
  user_scores = cosine_similarity(matrix[uidx], matrix)
  user_scores = np.delete(user_scores, uidx)
  predicted_rating_list = []
  for i in range(matrix.shape[1]):
    if matrix[uidx, i] == 0:
      user_ratings = matrix[:, i]
      user_ratings = user_ratings.toarray().flatten()
      user_ratings = np.delete(user_ratings, uidx)
      weight_sum = np.dot(user_scores, user_ratings)
      sum_of_scores = np.sum(user_scores)
      predicted_rating = 0
      if sum_of_scores != 0:
        predicted_rating = weight_sum / sum_of_scores
      predicted_rating_list.append((i, predicted_rating))

  predicted_rating_list = sorted(predicted_rating_list, key=lambda x: x[1], reverse=True)
  top_n_indices = [i[0] for i in predicted_rating_list[1:n+1]]
  top_n_ids = [idx_aid[i] for i in top_n_indices]
  return top_n_ids

def get_content_based_recommendation(appId_list, id_idx, idx_id, matrix, n=10):
  if len(appId_list) == 0:
    return None
  weighted_cosine_scores = [0 for i in range(matrix.shape[0])]
  for i in appId_list:
    cosine_score = cosine_similarity(matrix[id_idx[i[0]]], matrix).flatten()
    for j in range(matrix.shape[0]):
      weighted_cosine_scores[j] += cosine_score[j] * i[1]
  weighted_cosine_scores = [(idx_id[i], weighted_cosine_scores[i]) for i in range(len(weighted_cosine_scores))]
  appIds = [i[0] for i in appId_list]
  weighted_cosine_scores = [i for i in weighted_cosine_scores if i[0] not in appIds]
  weighted_cosine_scores = sorted(weighted_cosine_scores, key=lambda x: x[1], reverse=True)
  top_n_ids = [i[0] for i in weighted_cosine_scores[0:n]]
  return top_n_ids

#1
def get_most_played(n=10):
  id_list = games_sort_most_played['AppID'].values[:n]
  id_list = [i for i in id_list]
  return id_list

#2
def get_personal_recommendation(userId, uid_idx=uid_idx, idx_aid=idx_aid, id_idx=id_idx, idx_id=idx_id, user_game_matrix=user_game_matrix, feature_matrix=tfidf_unique_tags, n=10):
  if userId not in uid_idx.index:
    return None
  uidx = uid_idx[userId]
  ratings = user_game_matrix[uidx].toarray().flatten()
  ratings_list = [(idx_aid[i], ratings[i]) for i in range(len(ratings))]
  ratings_list = [i for i in ratings_list if i[1] != 0]
  if len(ratings_list) >= 5:
    #print(1)
    return get_collaborative_recommendation(userId, uid_idx, idx_aid, user_game_matrix, n=n)
  elif len(ratings_list) != 0:
    #print(2)
    appId_list = [i for i in ratings_list if i[1] >= 3]
    if (len(appId_list) == 0):
      highest_rating = max([i[1] for i in ratings_list])
      appId_list = [i for i in ratings_list if i[1] == highest_rating]
    return get_content_based_recommendation(appId_list, id_idx, idx_id, feature_matrix, n=n)
  else:
    #print(3)
    return get_most_played(n=n)
  
#3
def get_similar_games(AppID, id_idx, idx_id, aid_idx, idx_aid, feature_matrix, game_user_matrix, n=10, weight=0.5):
  feature_cosine_score = cosine_similarity(feature_matrix[id_idx[AppID]], feature_matrix).flatten()
  feature_cosine_score_list = [(idx_id[i], feature_cosine_score[i]) for i in range(len(feature_cosine_score))]
  for i in feature_cosine_score_list:
    if i[0] == AppID:
      feature_cosine_score_list.remove(i)

  item_cosine_score = cosine_similarity(game_user_matrix[aid_idx[AppID]], game_user_matrix).flatten()
  item_cosine_score_list = [(idx_aid[i], item_cosine_score[i]) for i in range(len(item_cosine_score))]


  for i in item_cosine_score_list:
    if i[0] == AppID:
      item_cosine_score_list.remove(i)


  combined_cosine_score_list = {}
  for k, v in feature_cosine_score_list:
    combined_cosine_score_list[k] = v *(1 - weight)
  for k, v in item_cosine_score_list:
    if k in combined_cosine_score_list:
      combined_cosine_score_list[k] += v * weight
    else:
      combined_cosine_score_list[k] = v * weight
  combined_cosine_score_list = list(combined_cosine_score_list.items())
  combined_cosine_score_list = sorted(combined_cosine_score_list, key=lambda x: x[1], reverse=True)
  top_n_ids = [i[0] for i in combined_cosine_score_list[0:n]]
  return top_n_ids

#4
def get_same_publishers(AppID, n=10):
  publisher = games_sort_most_played[games_sort_most_played['AppID'] == AppID]['Publishers'].values[0]
  id_list = games_sort_most_played[games_sort_most_played['Publishers'] == publisher]['AppID'].values
  id_list = [i for i in id_list if i != AppID]
  return id_list[:n]

def get_best_feature(id, id_idx, feature_rank=1 , excludes='', matrix=tfidf_duplicate_tags):
  idx = id_idx[id]
  feature_scores = matrix[idx].toarray().flatten()
  feature_names = tfidf_feature_names
  feature_scores = list(zip(feature_names, feature_scores))
  feature_scores = [i for i in feature_scores if i[0] not in excludes]
  feature_scores = sorted(feature_scores, key=lambda x: x[1], reverse=True)
  best_feature = feature_scores[feature_rank-1][0]
  return best_feature

def get_same_feature_games(AppID, aid_idx, idx_aid, feature_rank=1, game_user_matrix=game_user_matrix, n=10):
  categories = games_sort_most_played[games_sort_most_played['AppID'] == AppID]['Categories'].values[0]
  best_feature = get_best_feature(AppID, id_idx, feature_rank=feature_rank, excludes=categories, matrix=tfidf_duplicate_tags)

  print(best_feature)
  same_feature_games = games_sort_most_played[games_sort_most_played['combined unique tags'].str.contains(best_feature)]['AppID'].values
  same_feature_games = [i for i in same_feature_games if i != AppID]
  if AppID in aid_idx.index:
    cosine_score = cosine_similarity(game_user_matrix[aid_idx[AppID]], game_user_matrix).flatten()
    cosine_score_list = [(idx_aid[i], cosine_score[i]) for i in range(len(cosine_score))]
    cosine_score_dict = dict(cosine_score_list)

    sorted_same_feature_games = []
    for i in same_feature_games:
      if i in cosine_score_dict.keys():
        sorted_same_feature_games.append((i, cosine_score_dict[i]))
      else:
        sorted_same_feature_games.append((i, 0))
    sorted_same_feature_games = sorted(sorted_same_feature_games, key=lambda x: x[1], reverse=True)
    same_feature_games = [i[0] for i in sorted_same_feature_games]

  return same_feature_games[:n]



