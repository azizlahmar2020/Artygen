from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView
urlpatterns = [ 
 
    path('', PostListView.as_view(),name="post-home"),
    path('post/<int:pk>/', PostDetailView.as_view(),name="post-detail"),
    path('create/new', PostCreateView.as_view(),name="post-Create"),


]
