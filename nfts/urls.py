from django.urls import path
from .views import SearchNFT

app_name = 'nfts'

urlpatterns = [  
    path('search-nfts',SearchNFT.as_view(),name='SearchNFT')
]