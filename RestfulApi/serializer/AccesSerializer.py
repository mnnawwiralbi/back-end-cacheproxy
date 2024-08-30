from rest_framework import serializers
from RestfulApi.models import AccessLog

class AccesLogSerializer(serializers.ModelSerializer) :
    class Meta :
        model = AccessLog
        fields = '__all__'