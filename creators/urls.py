from django.urls import path
from .views import GetCreatorView,UpdateCollectionView,CollectionsView,GetCollectionView,SearchCollection,SearchCreator,UpdateCreatorView

app_name = 'creators'

urlpatterns = [  
    path('update-creator',UpdateCreatorView.as_view(),name='updatecreator'),
    path('update-collection',UpdateCollectionView.as_view(),name='updatecollection'),
    path('search-collection',SearchCollection.as_view(),name='searchcollection'),
    path('search-creator',SearchCreator.as_view(),name='searchcreator'),
    path('details',GetCreatorView.as_view(),name='getcreator'),  
    path('<name>/collections',CollectionsView.as_view(),name='getcollections'),
    path('<name>/collections/<slug>',GetCollectionView.as_view(),name='getcollection')
]