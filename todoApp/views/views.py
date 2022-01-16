from django.contrib.auth.models import User
from rest_framework import viewsets, authentication
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from todoApp.api.serializers import *
from todoApp.models import *
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequestedUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)


class TodoAppViewSet(viewsets.ModelViewSet):
    serializer_class = TodoAppSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = todoModel.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            todos = todoModel.objects.filter(user=request.user)
        except ObjectDoesNotExist as e:
            todos = todoModel.objects.all()
        todos_serialized = [TodoAppSerializer(r).data for r in todos]
        return Response(todos_serialized)
