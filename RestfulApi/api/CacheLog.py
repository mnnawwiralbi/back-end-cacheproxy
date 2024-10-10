from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from RestfulApi.models import CacheLog
from RestfulApi.serializer.CacheSerializer import CacheGetSerializer, CacheGetUpdateDelete
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
import paramiko
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class getCache (generics.ListCreateAPIView):
    queryset = CacheLog.objects.all()
    serializer_class = CacheGetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'cache_status', 'request_url']
    search_fields = ['id', 'cache_status', 'request_url']

    def create(self, request, *args, **kwargs):
        try:
            if isinstance(request.data, list):
                serializer = self.get_serializer(data=request.data, many=True)
            else:
                serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Cache Add",
                "data": serializer.data
            }
            return Response(response)
        except:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Article Created",
                "data": serializer.data
            }
            return Response(response)


class CacheUpdateDelete (generics.RetrieveUpdateDestroyAPIView):
    queryset = CacheLog.objects.all()
    serializer_class = CacheGetUpdateDelete
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Cache Update",
                "data": serializer.data
            }
            return Response(response)
        except:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Article Created",
                "data": serializer.data
            }
            return Response(response)
        
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class UpdateAutoCacheLog (APIView) :
    permission_classes = [AllowAny]
    authentication_classes =[TokenAuthentication]
    
    def cachedatabase(self):
        # mengambil orm object cache
        cadata = CacheLog.objects.all()
        jumlah = cadata.count()
        return jumlah

    def itemparse(self, items):
        # membuat list array
        json_logs = []

        for item in items:
            # Lakukan parsing baris log dan sesuaikan dengan format log Squid
            # Misalnya, jika formatnya adalah "timestamp IP_ADDRESS URL"
            parts = item            

            # Menambahkan entitas log ke dalam list json_logs
            json_logs.append(parts)

            jumlah = len(json_logs)

        return json_logs, jumlah


    def get(self, request):
        try:
            # mendapatkan ip server
            server =  CacheLog.objects.get(id=1)
            
            hostname = server.ip_address
            username = 'root'
            password = 'aldi2102'
            port = 22

            # lokasi squid
            squid_log_path = '/var/log/squid/cache.log'
            # menggunakan paramiko
            parami = paramiko.SSHClient()
            parami.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # koneksi ssh
            # Menghubungkan ke server
            parami.connect(hostname, port, username, password)

            # melakukan perintah ssl
            stdin, stdata, stderror = parami.exec_command(f"cat {squid_log_path}")
            data = stdata.read().decode()
            error = stderror.read().decode()

            if error:
                return Response({"status": "error", "message": error})

            # parse datacase
            datacache = data.split('\n')

            # mengambil idcache
            jumlahbase = self.cachedatabase()

            cachelog, jumlahcase = self.itemparse(datacache)
        
            # membuat memory sementara database

            database = [0] * jumlahcase

            # memasukan kedalam database

            if (jumlahbase != jumlahcase):
                for i in range(jumlahbase, jumlahcase):
                    database[i] = CacheLog (
                        message = cachelog[i],
                        server = server        
                    )
                    database[i].save()

            return Response({
                                'message': 'Data valid',
                                'data' : cachelog[jumlahcase-1]
                            }, status=status.HTTP_200_OK)
            
        except:

            return Response({'message': 'Data in valid'}, status=status.HTTP_400_BAD_REQUEST)

# custom        
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Default jumlah item per halaman
    max_limit = 100  # Batas maksimum item per halaman

class getCacheFilterApiView (APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['message']  # Tambahkan field yang ingin difilter
    search_fields = ['message']  # Tambahkan field untuk fitur search
    pagination_class = CustomLimitOffsetPagination

    def post(self, request):
        # Mendapatkan server terkait
        server_id = request.data.get('server_id')
        
        # Akses log yang telah terfilterisasi
        filtered_log = CacheLog.objects.filter(server=server_id)

        # Pagination
        paginator = CustomLimitOffsetPagination()
        result_page = paginator.paginate_queryset(filtered_log, request)
        
        # Membuat array log
        filter_array = [
            {
                'message': item_log.message,
            }
            for item_log in result_page
        ]

        # Jumlah access log
        count = filtered_log.count()

        return paginator.get_paginated_response({
            'count': count,
            'data': filter_array,
        })
    
    


         
    
    
