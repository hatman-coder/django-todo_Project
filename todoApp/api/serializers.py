from django.contrib.auth.models import User
from rest_framework import serializers
from todoApp.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class DefaultSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DefaultSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT']:
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1


class TodoAppSerializer(DefaultSerializer):
    class Meta:
        model = todoModel
        fields = '__all__'
        depth = 1