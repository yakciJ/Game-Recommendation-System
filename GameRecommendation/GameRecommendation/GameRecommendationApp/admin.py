from django.contrib import admin
from .models import *
# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    list_display = ('userId', 'AppID', 'rating')
class PersonalRCMAdmin(admin.ModelAdmin):
    list_display = ('userId', 'rcmlist')

admin.site.register(Rating, RatingAdmin)
admin.site.register(PersonalRCM, PersonalRCMAdmin)
