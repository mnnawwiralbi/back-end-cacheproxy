# note : untuk meng copy sebuah dict pada python tidak lah simple sperti ini a=b melainkan harus seperti ini a=b.copy()
# note : ternya list juga berpengarug pada generics.retrieveupdate

from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAdminUser
from RestfulApi.serializer.UpdateDataUserSerializer import UpdateDataUser, UpdateGrubDataUserSuper, UpdateGrubDataUserById, UpdateGrubDataSuperUserById
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

class UserUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateDataUser
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Updated",
            "data": serializer.data
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Deleted",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    
class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateGrubDataUserSuper
    permission_classes = [AllowAny]
    lookup_field = 'username'

    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def list(self, request, *args, **kwargs):
        
        # mmendapatkan group
        queryset = self.get_queryset()
        data = queryset.count()
        nama = [item.username for item in queryset]
        
        print(queryset[0])
        # serializer = self.get_serializer(queryset, many=True)
        return Response({
                            "data" : data,
                            "nama" : nama
                        })
        
    def update(self, request, *args, **kwargs):
        # mendapatkan instance saat ini
        instance = self.get_object()
        
        # setpassword
        get_data = request.data.copy() # membuat copy dari request.data
        get_data["password"] = make_password(get_data["password"]) # melakukan hash data
        
        serializer = UpdateGrubDataUserSuper(instance, data=get_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Updated",
            "data": serializer.data
        }
        return Response(response)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Deleted",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
class UserUpdateById(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateGrubDataUserById
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=False)
    
    def list(self, request, *args, **kwargs):
        
        # mmendapatkan group
        queryset = self.get_queryset()
        data = queryset.count()
        nama = [item.username for item in queryset]
        
        print(queryset[0])
        # serializer = self.get_serializer(queryset, many=True)
        return Response({
                            "data" : data,
                            "nama" : nama
                        })
        
    def update(self, request, *args, **kwargs):
        # mendapatkan instance saat ini
        instance = self.get_object()
        
        # setpassword
        get_data = request.data.copy() # membuat copy dari request.data
        get_data["password"] = make_password(get_data["password"]) # melakukan hash data
        
        serializer = UpdateGrubDataUserById(instance, data=get_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Updated",
            "data": serializer.data
        }
        return Response(response)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Deleted",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    

class SuperUserUpdateById(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateGrubDataSuperUserById
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        # Filter data pengguna yang bukan staff
        return User.objects.filter(is_staff=True)
    
    def list(self, request, *args, **kwargs):
        
        # mmendapatkan group
        queryset = self.get_queryset()
        data = queryset.count()
        nama = [item.username for item in queryset]
        
        print(queryset[0])
        # serializer = self.get_serializer(queryset, many=True)
        return Response({
                            "data" : data,
                            "nama" : nama
                        })
        
    def update(self, request, *args, **kwargs):
        # mendapatkan instance saat ini
        instance = self.get_object()
        
        # setpassword
        get_data = request.data.copy() # membuat copy dari request.data
        get_data["password"] = make_password(get_data["password"]) # melakukan hash data
        
        serializer = self.get_serializer(instance, data=get_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Updated",
            "data": serializer.data
        }
        return Response(response)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "User Deleted",
        }
        
        return Response(response, status=status.HTTP_200_OK)