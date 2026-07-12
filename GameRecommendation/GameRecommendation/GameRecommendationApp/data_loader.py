from django.conf import settings

import pickle
import requests
import os


class RecommendationData:

    BASE_URL = "https://github.com/yakciJ/Game-Recommendation-System/releases/download/v1.0"

    FILES = {
        "games": "games.pkl",
        "users": "users.pkl",
        "games_sort_most_played": "games_sort_most_played.pkl",
        "tfidf_unique_tags": "tfidf_unique_tags.pkl",
        "tfidf_duplicate_tags": "tfidf_duplicate_tags.pkl",
        "id_idx": "id_idx.pkl",
        "idx_id": "idx_id.pkl",
        "tfidf_feature_names": "tfidf_feature_names.pkl",
        "raw_features": "raw_features.pkl",
        "feature_words_dict": "feature_words_dict.pkl",
    }

    def __init__(self):
        self.loaded = False

        self.games = None
        self.users = None
        self.games_sort_most_played = None

        self.tfidf_unique_tags = None
        self.tfidf_duplicate_tags = None

        self.id_idx = None
        self.idx_id = None

        self.tfidf_feature_names = None
        self.raw_features = None

        self.feature_words_dict = None


    def load_pickle(self, filename):

        url = f"{self.BASE_URL}/{filename}"

        response = requests.get(url)

        response.raise_for_status()

        return pickle.loads(response.content)
    

    def load(self):
        if self.loaded:
            return
        
        print("RCM_DATA_SOURCE =" + settings.RCM_DATA_SOURCE)
        if settings.RCM_DATA_SOURCE == "local":
            self.load_local()
        else:
            self.load_github()

        self.loaded = True
        print("Recommendation data loaded.")

    def load_local(self):
        current_dir = os.path.dirname(__file__)

        print("Loading recommendation data from local...")

        with open(current_dir+'/Data/games.pkl', 'rb') as f:
            self.games = pickle.load(f)

        with open(current_dir+'/Data/users.pkl', 'rb') as f:
            self.users = pickle.load(f)

        with open(current_dir+'/Data/games_sort_most_played.pkl', 'rb') as f:
            self.games_sort_most_played = pickle.load(f)

        with open(current_dir+'/Data/tfidf_unique_tags.pkl', 'rb') as f:
            self.tfidf_unique_tags = pickle.load(f)

        with open(current_dir+'/Data/tfidf_duplicate_tags.pkl', 'rb') as f:
            self.tfidf_duplicate_tags = pickle.load(f)

        with open(current_dir+'/Data/id_idx.pkl', 'rb') as f:
            self.id_idx = pickle.load(f)

        with open(current_dir+'/Data/idx_id.pkl', 'rb') as f:
            self.idx_id = pickle.load(f)

        with open(current_dir+'/Data/tfidf_feature_names.pkl', 'rb') as f:
            self.tfidf_feature_names = pickle.load(f)

        with open(current_dir+'/Data/raw_features.pkl', 'rb') as f:
            self.raw_features = pickle.load(f)

        with open(current_dir+'/Data/feature_words_dict.pkl', 'rb') as f:
            self.feature_words_dict = pickle.load(f)


    def load_github(self):

        print("Loading recommendation data from Github Releases...")

        self.games = self.load_pickle(
            self.FILES["games"]
        )

        self.users = self.load_pickle(
            self.FILES["users"]
        )

        self.games_sort_most_played = self.load_pickle(
            self.FILES["games_sort_most_played"]
        )

        self.tfidf_unique_tags = self.load_pickle(
            self.FILES["tfidf_unique_tags"]
        )

        self.tfidf_duplicate_tags = self.load_pickle(
            self.FILES["tfidf_duplicate_tags"]
        )

        self.id_idx = self.load_pickle(
            self.FILES["id_idx"]
        )

        self.idx_id = self.load_pickle(
            self.FILES["idx_id"]
        )

        self.tfidf_feature_names = self.load_pickle(
            self.FILES["tfidf_feature_names"]
        )

        self.raw_features = self.load_pickle(
            self.FILES["raw_features"]
        )

        self.feature_words_dict = self.load_pickle(
            self.FILES["feature_words_dict"]
        )


recommendation_data = RecommendationData()

