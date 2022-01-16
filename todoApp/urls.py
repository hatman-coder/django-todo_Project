from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

import todoApp.views
from todoApp.views import *


router = routers.DefaultRouter()

router.register(r'users', todoApp.views.UserViewSet )
router.register(r'users-me', todoApp.views.RequestedUserViewSet)
router.register(r'todos', todoApp.views.TodoAppViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
]