# Note : berarti sebelumnya salah dimaana jika kita hanya merubah salah satu maka semuanya tidak akan berubah
# Note : berarti UpdateGrubDataUserSuper harus memerulkan yang namanya username untuk validasi

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UpdateDataUser(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
class UpdateGrubDataUser(serializers.Serializer):
    
    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def update(self, instance, validated_data):
        # mmendapatkan group
        queryset = self.get_queryset()
        
        # verrivikasi grub
        
        for item in queryset :
            if (instance.username == item.username ) :
                 instance.last_name = validated_data.get('last_name', instance.last_name)
                 instance.firs_name = validated_data.get('firs_name', instance.firs_name)
                 instance.save()
                 return instance
             
        raise serializers.ValidationError(
                    "Gagal Update")

class UpdateGrubDataUserSuper(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'
    
    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def update(self, instance, validated_data):
        # mmendapatkan group
        queryset = self.get_queryset()
        
        # verrivikasi grub
        
        for item in queryset :
            if (instance.username == item.username ) :
                return super().update(instance, validated_data)
             
        raise serializers.ValidationError(
                    "Gagal Update")
        
class UpdateGrubDataUserById(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'
    
    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def update(self, instance, validated_data):
        # mmendapatkan group
        queryset = self.get_queryset()
        
        # verrivikasi grub
        
        for item in queryset :
            if (instance.id == item.id ) :
                return super().update(instance, validated_data)
             
        raise serializers.ValidationError(
                    "Gagal Update")

class UpdateGrubDataSuperUserById(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'
    
    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def update(self, instance, validated_data):
        # mmendapatkan group
        queryset = self.get_queryset()
        
        # verrivikasi grub
        
        for item in queryset :
            if (instance.id == item.id ) :
                return super().update(instance, validated_data)
             
        raise serializers.ValidationError(
                    "Gagal Update")
        
   
    
    
    