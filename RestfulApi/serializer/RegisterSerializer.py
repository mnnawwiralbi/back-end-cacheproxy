from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer) :
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def create(self, validated_data):    
        query = User.objects.all()
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        return super().create(validated_data)
    
class AccountSerializerRegisterSuperUser(serializers.ModelSerializer):
    class Meta:
        model = User
        # Tambahkan field lain yang diperlukan
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user
    
class AccountSerializerRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        # Tambahkan field lain yang diperlukan
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    