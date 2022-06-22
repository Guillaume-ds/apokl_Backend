from django.urls import path
from .views import GetPostsView,GetCommentsView

app_name = 'postsAndComments'

urlpatterns = [
    path('get-posts',GetPostsView.as_view(),name='getcollectionposts'),
    path('get-comments',GetCommentsView.as_view(),name='getcomments'),
]