from rest_framework import serializers
from RestfulApi.models import CacheLog

class CacheGetSerializer (serializers.ModelSerializer):
    class Meta:
        model = CacheLog
        fields = '__all__'


class CacheGetUpdateDelete (serializers.Serializer):
    userid = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    image = serializers.ImageField()
    activate = serializers.BooleanField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.userid = validated_data.get('userid', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
