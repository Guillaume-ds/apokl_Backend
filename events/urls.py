from django.urls import path
from .views import GetEventView,ClaimEventAccessView

app_name = 'events'

urlpatterns = [
    path('get-events',GetEventView.as_view(),name='getevent'),
    path('claim-access',ClaimEventAccessView.as_view(),name='claimeventaccess'),
]