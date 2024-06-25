from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import Data





def home(request):
    template = loader.get_template('product.html')
    context = {
        }
    return HttpResponse(template.render(context, request))