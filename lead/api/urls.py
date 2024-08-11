from django.urls import path
from . views import *
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView 
urlpatterns = [
    path('login',loginUser , name='token_obtain_pair'),
    path('token/refresh' ,TokenRefreshView.as_view() ,name='token_refresh'),
    path('add-user',addUser,name="add-user"),
    path('get-user',getUsersList , name='get-user')
]
