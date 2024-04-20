from django.urls import path
from .views import listApiView, signUp, attendance, check_user, \
    view_all_messages, admin_create_message_view
from rest_framework_simplejwt.views import (
TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path("register/", listApiView),
    path('signUp/', signUp),
    path('attendance/', attendance),
    path('jwt/create', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify', TokenVerifyView.as_view(), name='jwt_verify'),
    path('mark/register', check_user, name="mark_register"),
    path('messages/', view_all_messages, name='messages'),
    path('create/message', admin_create_message_view, name="create_message")
]