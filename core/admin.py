from django.contrib import admin
from .models import *
admin.site.register([Genre,Movie,CastMember,Review,WatchlistItem])
