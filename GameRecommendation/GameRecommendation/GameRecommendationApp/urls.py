from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:AppId>/<int:UID>', views.product, name='product'),
]