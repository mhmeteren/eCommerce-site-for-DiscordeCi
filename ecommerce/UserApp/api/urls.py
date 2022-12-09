from django.urls import path
from UserApp.api import views as api_views


urlpatterns = [
    path('userAuth/<str:token>/', api_views.UserAccTokenAutAPIView.as_view(), name="userAuth"),
]