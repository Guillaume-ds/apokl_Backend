from django.urls import path
from .views import GetPostsView, CreatePostView, CreateRoomView,GetRoomView,ClaimRoomAccessView

app_name = 'rooms'

urlpatterns = [
    path('collection/posts/<slug>',GetPostsView.as_view(),name='getcollectionposts'),
    path('collection/create-post',CreatePostView.as_view(),name='createposts'),
    path('collection/create-room',CreateRoomView.as_view(),name='createroom'),
    path('get-room/<slug>',GetRoomView.as_view(),name='getrooms'),
    path('claim-access',ClaimRoomAccessView.as_view(),name='claimroomaccess'),
]