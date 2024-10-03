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
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from RestfulApi.models import UserData

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

@api_view(['PUT', 'DELETE'])
@permission_classes((AllowAny,))
def UpdateDataUserAPI(request, id):
    try:
        # Mendapatkan lookup id
        id_user = id
        
        if request.method == 'PUT':
            data = request.data
            if not data:
                return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': 'No data provided'})

            # Mendapatkan user
            try:
                user = User.objects.get(id=id_user)
            except User.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'message': 'User not found'})
            
            # Update user fields
            user.username = data.get('username', user.username)  # Tidak mengubah jika tidak disediakan
            password = data.get('password', None)
            if password:
                user.password = make_password(password)
            user.email = data.get('email', user.email)
            user.save()

            # Update atau buat UserData
            user_data = UserData.objects.filter(data_owner=id_user).first()  # Menghindari dua kali query
            if user_data:
                # Update existing user data
                user_data.nama_lengkap = data.get('nama_lengkap', user_data.nama_lengkap)
                user_data.kelamin = data.get('kelamin', user_data.kelamin)
                user_data.no_ktp = data.get('no_ktp', user_data.no_ktp)
                user_data.alamat_domisili = data.get('alamat_domisili', user_data.alamat_domisili)
                user_data.alamat_ktp = data.get('alamat_ktp', user_data.alamat_ktp)
                user_data.npwp = data.get('npwp', user_data.npwp)
                user_data.no_telp = data.get('no_telp', user_data.no_telp)
                user_data.agama = data.get('agama', user_data.agama)
                user_data.tanggal_lahir = data.get('tanggal_lahir', user_data.tanggal_lahir)
                user_data.tempat_lahir = data.get('tempat_lahir', user_data.tempat_lahir)
            else:
                # Create new user data
                user_data = UserData.objects.create(
                    nama_lengkap=data.get('nama_lengkap', ''),
                    kelamin=data.get('kelamin', ''),
                    no_ktp=data.get('no_ktp', ''),
                    alamat_domisili=data.get('alamat_domisili', ''),
                    alamat_ktp=data.get('alamat_ktp', ''),
                    npwp=data.get('npwp', ''),
                    no_telp=data.get('no_telp', ''),
                    agama=data.get('agama', ''),
                    tanggal_lahir=data.get('tanggal_lahir', None),
                    tempat_lahir=data.get('tempat_lahir', ''),
                    data_owner=user
                )
            user_data.save()

            return Response({'code': status.HTTP_200_OK, 'message': 'Data successfully updated!'})

        elif request.method == 'DELETE':
            try:
                # Menghapus UserData dan User
                user_data = UserData.objects.get(data_owner=id_user)
                user_data.delete()

                user = User.objects.get(id=id_user)
                user.delete()

                return Response({'code': status.HTTP_200_OK, 'message': 'Data successfully deleted!'})
            except UserData.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'message': 'User data not found'})
            except User.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'message': 'User not found'})

    except Exception as e:
        return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': f'Error: {str(e)}'})
 
    