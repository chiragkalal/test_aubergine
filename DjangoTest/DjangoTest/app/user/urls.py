from .views import UserCreateAPIView, LoginAPIView, UserRetrieveAPIView
from django.urls import path

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user_detail/', UserRetrieveAPIView.as_view()),
]