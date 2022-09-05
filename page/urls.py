from django.urls import path
from . import views
from.views import CreatePost

urlpatterns = [
    path('explore/', views.Listexplore.as_view(), name='page-explore'),
    path('user/<str:username>/', views.UserList.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.DetailPost.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post-delete'),
    path('post/create/', CreatePost.as_view(), name='post-create'),
    path('about/',views.about,name='page-about'),
    path('home/',views.Listhome.as_view(),name='page-home'),
    path('tests/',views.test,name="page-test"),
    path('user/<str:username>/follower/', views.Follow.as_view(), name='user-follow'),
    path('user/<str:username>/following/', views.Following.as_view(), name='user-following'),
    path('explore/search_results/', views.search, name='search-results'),
    path('post/<str:hsh>/', CreatePost.as_view(), name='hashtag'),
    path('tags/<str:tags>/', views.tags, name='tags'),
    path('songs/',views.music_player,name='music_player'),
    path('music_player/search_results/', views.search_music, name='search-results-music'),





]