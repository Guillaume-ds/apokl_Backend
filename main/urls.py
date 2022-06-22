from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin

import accounts.views
import nfts.views
import profiles.views
import events.views
import collectionsNft.views
import postsAndComments.views

router = routers.DefaultRouter()
router.register(r'users', accounts.views.UserViewSet)
router.register(r'nfts', nfts.views.NFTViewSet)
router.register(r'profiles', profiles.views.ProfileViewSet)
router.register(r'collections', collectionsNft.views.CollectionViewSet)
router.register(r'posts', postsAndComments.views.PostViewSet)
router.register(r'events', events.views.EventViewSet)
router.register(r'comments', postsAndComments.views.CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', accounts.views.UserAPIView.as_view(), name='login'),
    path('api/register/', accounts.views.RegisterUserAPIView.as_view(), name='register'),
    path('api/change-password/', accounts.views.ChangePasswordView.as_view(), name='change-password'),
    path('api/reset-password/', accounts.views.ResetPasswordView.as_view(), name='change-password'),
    path('api/profiles/', include('profiles.urls', namespace='profiles')),
    path('api/postsAndComments/', include('postsAndComments.urls', namespace='postsAndComments')),
    path('api/collections/', include('collectionsNft.urls', namespace='collections')),
    path('api/events/', include('events.urls', namespace='events')),
    path('api/nfts/',include('nfts.urls', namespace='nfts')),
]
