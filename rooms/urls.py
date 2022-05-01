from django.urls import path
from .views import GetPostsView,GetRoomView,ClaimRoomAccessView

app_name = 'rooms'

urlpatterns = [
    path('get-posts',GetPostsView.as_view(),name='getcollectionposts'),
    path('get-rooms',GetRoomView.as_view(),name='getrooms'),
    path('claim-access',ClaimRoomAccessView.as_view(),name='claimroomaccess'),
]