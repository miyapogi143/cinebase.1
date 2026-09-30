from django.urls import path
from . import views
urlpatterns=[path('',views.movie_list,name='catalog'),path('movies/<slug:slug>/',views.movie_detail,name='movie_detail'),path('watchlist/',views.watchlist,name='watchlist'),path('watchlist/toggle/<int:movie_id>/',views.toggle_watchlist,name='toggle_watchlist'),path('watchlist/remove/<int:item_id>/',views.remove_watchlist,name='remove_watchlist'),path('reviews/<slug:slug>/',views.add_review,name='add_review'),path('manage/movies/new/',views.movie_create,name='movie_create')]
