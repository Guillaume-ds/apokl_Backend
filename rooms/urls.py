from django.urls import path
from .views import GetPostsView

app_name = 'rooms'

urlpatterns = [
    path('collection/posts/<slug>',GetPostsView.as_view(),name='getcollectionposts')
]