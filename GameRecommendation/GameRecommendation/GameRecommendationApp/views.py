from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from . import Data
from .Data import *
import json


def get_header_img_urls(ids):
    urls = []
    for i in ids:
        urls.append(games[games['AppID'] == i]['Header image'].values[0])
    return urls

def get_names(ids):
    names = []
    for i in ids:
        names.append(games[games['AppID'] == i]['Name'].values[0])
    return names

def get_ids(names):
    ids = []
    for i in names:
        ids.append(games[games['Name'] == i]['AppID'].values[0])
    return ids

def get_tags(ids):
    tags = []
    for i in ids:
        tags.append(raw_features[raw_features['AppID'] == i]['Tags'].fillna('').values[0])
    return tags

def get_personal_rcm_list(userId=UID):
    rcm_list_data = PersonalRCM.objects.filter(userId=userId).values()
    if len(rcm_list_data) > 0:
        rcm_list_data = rcm_list_data[0]['rcmlist']
        rcm_list = json.loads(rcm_list_data)
    else:
        rcm_list = get_personal_recommendation(userId)
    return rcm_list

def get_rating(userId, AppID):
    rating_data = Rating.objects.filter(userId=userId, AppID=AppID).values()
    if len(rating_data) > 0:
        return rating_data[0]['rating']
    else:
        return 0
    
def set_rating(userId, AppID, rating):
    defaults = {'rating': rating}
    obj, created = Rating.objects.update_or_create(userId=userId, AppID=AppID, defaults=defaults)


def home(request):
    template = loader.get_template('home.html')

    most_played_ids = get_most_played()
    most_played_header_img = get_header_img_urls(most_played_ids)
    most_played_names = get_names(most_played_ids)

    context = {
            'UID': UID,
            'most_played_ids_header_img' : zip(most_played_ids, most_played_header_img),
            'most_played_ids_names_header_img': zip(most_played_ids, most_played_names, most_played_header_img)
        }
    return HttpResponse(template.render(context, request))

def product(request, AppId, UID):
    #game info
    name = games[games['AppID'] == AppId]['Name'].values[0]
    header_img = games[games['AppID'] == AppId]['Header image'].values[0]
    about = games[games['AppID'] == AppId]['About the game'].values[0]
    release = games[games['AppID'] == AppId]['Release date'].values[0]
    developer = games[games['AppID'] == AppId]['Developers'].values[0]
    publisher = games[games['AppID'] == AppId]['Publishers'].values[0]
    categories = raw_features[raw_features['AppID'] == AppId]['Categories'].values[0]
    genres = raw_features[raw_features['AppID'] == AppId]['Genres'].values[0]
    tags = raw_features[raw_features['AppID'] == AppId]['Tags'].values[0]
    video = games[games['AppID'] == AppId]['Movies'].values[0]
    screenshots_str = games[games['AppID'] == AppId]['Screenshots'].values[0]
    screenshots = screenshots_str.split(',')
    screenshots = screenshots[:4]
    rating = get_rating(UID, AppId)

    #recommend
    similar_game_ids = get_similar_games(AppId)
    similar_game_imgs = get_header_img_urls(similar_game_ids)
    similar_game_names = get_names(similar_game_ids)

    same_publisher_game_ids = get_same_publishers(AppId)
    same_publisher_game_imgs = get_header_img_urls(same_publisher_game_ids)
    same_publisher_game_names = get_names(same_publisher_game_ids)

    same_feature_games_1_ids, best_feature_1 = get_same_feature_games(AppId, feature_rank=1)
    same_feature_games_1_imgs = get_header_img_urls(same_feature_games_1_ids)
    same_feature_games_1_names = get_names(same_feature_games_1_ids)

    same_feature_games_2_ids, best_feature_2 = get_same_feature_games(AppId, feature_rank=2)
    same_feature_games_2_imgs = get_header_img_urls(same_feature_games_2_ids)
    same_feature_games_2_names = get_names(same_feature_games_2_ids)

    best_feature_1 = feature_words_dict[best_feature_1]
    best_feature_2 = feature_words_dict[best_feature_2]

    template = loader.get_template('product.html')
    context = {
        'AppID': AppId,
        'UID': UID,
        'name': name,
        'header_img': header_img,
        'about' : about,
        'release': release,
        'developer': developer,
        'publisher': publisher,
        'categories': categories,
        'genres' : genres,
        'tags': tags,
        'video': video,
        'screenshots': screenshots,
        'rating': rating,
        'rating_loop': [5, 4, 3, 2, 1],
        'similar_games': zip(similar_game_ids, similar_game_imgs, similar_game_names),
        'same_publisher_games': zip(same_publisher_game_ids, same_publisher_game_imgs, same_publisher_game_names),
        'same_feature_games_1': zip(same_feature_games_1_ids, same_feature_games_1_imgs, same_feature_games_1_names),
        'same_feature_games_2': zip(same_feature_games_2_ids, same_feature_games_2_imgs, same_feature_games_2_names),
        'best_feature_1': best_feature_1,
        'best_feature_2': best_feature_2,
    }
    return HttpResponse(template.render(context, request))

def search(request, query):
    template = loader.get_template('search.html')
    names = get_search_list(query)
    ids = get_ids(names)
    imgs = get_header_img_urls(ids)
    tags = get_tags(ids)
    context = {
            'UID': UID,
            'query': query,
            'games': zip(ids, imgs, names ,tags),
        }
    return HttpResponse(template.render(context, request))

def save_rating(request, userId, AppID, rating):
    context = {"result": "succeed"}
    set_rating(userId, AppID, rating)
    return JsonResponse(context)

def calculate(request, a, b):
    result = a + b
    # ratings = Rating.objects.filter(userId=1).values()
    # print(len(ratings))
    print(get_rating(1, 2))
    return JsonResponse({"result": result})