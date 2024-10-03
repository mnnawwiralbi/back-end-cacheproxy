from rest_framework import serializers
from RestfulApi.models import UserData

class UserDataSerializer(serializers.ModelField) :
    class Meta : 
        model = UserData
        fields = '__all__'