from django.urls import path
from UserApp.api import views as api_views


urlpatterns = [
    path('userAuth/<str:token>/', api_views.UserAccTokenAutAPIView.as_view(), name="userAuth"),
    path('plists/<str:listname>/', api_views.UserUyeListAPIView.as_view(), name="plists"),
    path('userplists/', api_views.UserProductListView.as_view(), name="userplists"),
    path('usersepet/', api_views.UserSepetListAddDeleteAPIView.as_view(), name="usersepet")
]