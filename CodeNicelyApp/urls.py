from django.urls import path
from CodeNicelyApp import views
urlpatterns = [

    path('index', views.Home, name="homepage"),
    path('register', views.RegisterPageView, name='register'),
    path('login', views.LoginPageView, name='login'),
    path('logout', views.LogoutPage, name='logout'),
    path('find-friends', views.FindFriendsView, name='find-friends'),
    path('results', views.ResultsView, name='search'),
    path('post',views.PostDataView, name='post'),
    path('all-post',views.AllPostView,name='all-post'),
    path('add-friend/<id>', views.AddFriendView, name='add-friend'),
    path('profile',views.ProfileView,name='profile'),
    path('profile-edit',views.profileEditView,name='profile-edit'),
    path('friend-list',views.FriendListView,name='friend-list'),
    path('', views.autocomplete, name='autocomplete'),




]