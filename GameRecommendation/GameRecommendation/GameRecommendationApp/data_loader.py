import pickle
import requests


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

        print("Loading recommendation data...")

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

        self.loaded = True

        print("Recommendation data loaded.")


recommendation_data = RecommendationData()

