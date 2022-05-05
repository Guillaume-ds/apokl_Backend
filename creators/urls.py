from django.urls import path
from .views import *

app_name = 'creators'

urlpatterns = [  
    path('search-creators',SearchCreator.as_view(),name='searchcreator'),
    path('details-creator',GetCreatorDetailsView.as_view(),name='getcreator'), 
    path('context-creator',GetCreatorContextView.as_view(),name='getcreator'), 
    path('update-creator',UpdateCreatorView.as_view(),name='updatecreator'),
    path('search-collections',SearchCollection.as_view(),name='searchcollection'),
    path('update-collection',UpdateCollectionView.as_view(),name='updatecollection'), 
    path('details-collections',GetCollectionDetailsView.as_view(),name='getcollection')
]