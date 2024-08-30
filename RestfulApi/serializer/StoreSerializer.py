from rest_framework import serializers
from RestfulApi.models import StoreLog

class StoreLogSerializer ( serializers.ModelSerializer) :
    class Meta :
        model = StoreLog
        fields = '__all__'