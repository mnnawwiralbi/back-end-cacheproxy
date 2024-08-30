from rest_framework import serializers
from RestfulApi.models import SquidLog

class SquidLogSerializer (serializers.ModelSerializer) :
    class Meta :
        model = SquidLog
        fields = '__all__'