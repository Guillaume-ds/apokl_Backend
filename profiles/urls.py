from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [  
    path('search-creators',SearchProfile.as_view(),name='searchcreator'),
    path('get-specific-creator/<creatorName>',GetSpecificProfileView.as_view(),name='searchcreator'),
    path('details-creator',GetProfileDetailsView.as_view(),name='getcreator'), 
    path('context-creator',GetProfileContextView.as_view(),name='getcreator'), 
    path('update-creator',UpdateProfileView.as_view(),name='updatecreator')
]