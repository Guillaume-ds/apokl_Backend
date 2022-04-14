from django.urls import path
from .views import CreateCreatorView,CreatorsView, GetCreatorView,CreateCollectionView,CollectionsView,GetCollectionView,SearchCollection,SearchCreator

app_name = 'creators'

urlpatterns = [
    path('',CreatorsView.as_view(),name='creators'),    
    path('activate', CreateCreatorView.as_view(),name='createcreators'),
    path('create-collection',CreateCollectionView.as_view(),name='createcollection'),
    path('search-collection',SearchCollection.as_view(),name='searchcollection'),
    path('search-creator',SearchCreator.as_view(),name='searchcreator'),
    path('<name>',GetCreatorView.as_view(),name='getcreator'),  
    path('<name>/collections',CollectionsView.as_view(),name='getcollections'),
    path('<name>/collections/<slug>',GetCollectionView.as_view(),name='getcollection')
]