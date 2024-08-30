from rest_framework import serializers
from RestfulApi.models import ProxyServerInfo

class ServerSerializer (serializers.ModelSerializer):
    class Meta:
        model = ProxyServerInfo
        fields = '__all__'
