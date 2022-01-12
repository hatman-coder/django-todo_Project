from django.urls import path, include
from rest_framework import routers

import todoApp.views
from todoApp.views import *


router = routers.DefaultRouter()

router.register(r'users', todoApp.views.UserViewSet )
router.register(r'todos', todoApp.views.TodoAppViewSet)

urlpatterns = [
    path('', include(router.urls)),
]