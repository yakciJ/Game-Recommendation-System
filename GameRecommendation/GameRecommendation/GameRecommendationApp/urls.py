from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:AppId>/<int:UID>', views.product, name='product'),
    path('search/<str:query>', views.search, name='search'),
    path('calculate/<int:a>/<int:b>/', views.calculate, name='calculate'),
    path('saveRating/<int:userId>/<int:AppID>/<int:rating>', views.save_rating, name='saveRating'),
]