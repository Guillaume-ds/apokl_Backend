from django.urls import path
from .views import GetPostsView,GetRoomView,ClaimRoomAccessView,GetCommentsView

app_name = 'rooms'

urlpatterns = [
    path('get-posts',GetPostsView.as_view(),name='getcollectionposts'),
    path('get-rooms',GetRoomView.as_view(),name='getrooms'),
    path('get-comments',GetCommentsView.as_view(),name='getcomments'),
    path('claim-access',ClaimRoomAccessView.as_view(),name='claimroomaccess'),
]