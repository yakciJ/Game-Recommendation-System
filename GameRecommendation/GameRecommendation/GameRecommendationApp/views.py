from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import Data
from .Data import *


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
    name = games[games['AppID'] == AppId]['Name'].values[0]
    template = loader.get_template('product.html')
    context = {
        'name': name
    }
    return HttpResponse(template.render(context, request))