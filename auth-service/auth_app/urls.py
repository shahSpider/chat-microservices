from django.contrib import admin
from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', CreateUserView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chat/conversations/', ConversationListCreateView.as_view(), name='conversation_list'),
    path('chat/conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message_list_create'),
    path('chat/conversations/<int:conversation_id>/messages/<int:pk>/', MessageRetrieveDestroyView.as_view(), name='message_retrieve_destroy'),
]