from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
import rooms.views
import accounts.views
import nfts.views
import creators.views

router = routers.DefaultRouter()
router.register(r'users', accounts.views.UserViewSet)
router.register(r'groups', rooms.views.GroupViewSet)
router.register(r'rooms', rooms.views.RoomViewSet)
router.register(r'nfts', nfts.views.NFTViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('nfts/<slug>',nfts.views.NFTView.as_view(),name='NFTdetails'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', accounts.views.UserAPIView.as_view(), name='login'),
    path('api/register/', accounts.views.RegisterUserAPIView.as_view(), name='register')   ,
    path('api/change-password/', accounts.views.ChangePasswordView.as_view(), name='change-password'),
    path('api/reset-password/', accounts.views.ResetPasswordView.as_view(), name='change-password'),
    path('api/creators/', include('creators.urls', namespace='creators')),
]
