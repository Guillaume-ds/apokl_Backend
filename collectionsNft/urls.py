from django.urls import path
from .views import *

app_name = 'collectionsNft'

urlpatterns = [  
    path('search-collections',SearchCollection.as_view(),name='searchcollection'),
    path('update-collection',UpdateCollectionView.as_view(),name='updatecollection'), 
    path('details-collections',GetCollectionDetailsView.as_view(),name='getcollection')
]