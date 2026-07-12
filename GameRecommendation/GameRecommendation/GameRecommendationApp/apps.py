from django.apps import AppConfig


class GamerecommendationappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GameRecommendationApp'

    def ready(self):

        from .data_loader import recommendation_data

        recommendation_data.load()
