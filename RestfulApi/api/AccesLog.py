from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination , PageNumberPagination 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from RestfulApi.models import AccessLog
from RestfulApi.serializer.AccesSerializer import AccesLogSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from RestfulApi.models import ProxyServerInfo
import paramiko
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class getAcces (generics.ListCreateAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccesLogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'http_status', 'request_url']
    search_fields = ['id', 'http_status', 'request_url']

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
                "message": "Store Add",
                "data": serializer.data
            }
            return Response(response)
        except:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Store Add Failed",
                "data": serializer.data
            }
            return Response(response)


class AccesUpdateDelete (generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccesLogSerializer
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
                "message": "Store Update",
                "data": serializer.data
            }
            return Response(response)
        except:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Store Update",
                "data": serializer.data
            }
            return Response(response)

class UpdateAutoAccesLog (APIView) :
    permission_classes = [AllowAny]
    authentication_classes =[TokenAuthentication]
    
    def cachedatabase(self):
        # mengambil orm object cache
        cadata = AccessLog.objects.all()
        jumlah = cadata.count()
        return jumlah

    def itemparse(self, items):
        # membuat list array
        json_logs = []

        for item in items:
            # Lakukan parsing baris log dan sesuaikan dengan format log Squid
            # Misalnya, jika formatnya adalah "timestamp IP_ADDRESS URL"
            parts = item.split()

            if len(parts) >= 7:  # Pastikan ada cukup bagian dalam baris log
                timestamp = parts[0]
                time_taken = parts[1]
                ip_address = parts[2]
                Http_status = parts[3]
                bytes = parts[4]
                method = parts[5]
                url = parts[6]
                host= parts[8]
                

                # Membuat entitas log dalam format JSON
                log_entry = {
                    'timestamp': timestamp,
                    'timetaken' : time_taken,
                    'ip_address': ip_address,
                    'http_status' : Http_status,
                    'bytes' : bytes,
                    'methode' : method,
                    'url': url,
                    'host' : host,
                }

                # Menambahkan entitas log ke dalam list json_logs
                json_logs.append(log_entry)

                jumlah = len(json_logs)

        return json_logs, jumlah



    def get(self, request):
        try:
            #     deklarasi configurasi akun server   
            #     mendapatkan ip server
            
            server =  ProxyServerInfo.objects.get(id=1)
            
            hostname = server.ip_address
            username = 'root'
            password = 'aldi2102'
            port = 22

            # lokasi squid
            squid_log_path = '/var/log/squid/access.log'
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

            acceslog, jumlahcase = self.itemparse(datacache)
        

            # membuat memory sementara database

            database = [0] * jumlahcase

            # memasukan kedalam database

            if (jumlahbase != jumlahcase):
                for i in range(jumlahbase, jumlahcase):
                    database[i] = AccessLog(
                        timestamp = acceslog[i]['timestamp'],
                        elapsed_time = acceslog[i]['timetaken'],
                        client_address = acceslog[i]['ip_address'],
                        http_status = acceslog[i]['http_status'],
                        bytes = acceslog[i]['bytes'],
                        request_method = acceslog[i]['methode'],
                        request_url = acceslog[i]['url'],
                        host = acceslog[i]['host'],
                        server = server,        
                    )
                    database[i].save()

            return Response({
                                'message': 'Data valid',
                                'data' : acceslog[jumlahcase-1]
                            }, status=status.HTTP_200_OK)

        except:

            return Response({'message': 'Data in valid'}, status=status.HTTP_400_BAD_REQUEST)
        
class getAccesApiView (APIView) : 
    permission_classes = [ AllowAny]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request) :
        
        # mendapatkan server terkait 
        server_id = request.data.get('server_id')
        
        # acceslog yang telah ter filterisasi
        filtered_log = AccessLog.objects.filter(server=server_id)
        
        # membuat array log
        filter_array = []
        
        for item_log in filtered_log :
            filter_array.append(
                {
                    'timestamp': item_log.timestamp,
                    'timetaken' : item_log.elapsed_time,
                    'ip_address': item_log.client_address,
                    'http_status' : item_log.http_status,
                    'bytes' : item_log.bytes,
                    'methode' : item_log.request_method,
                    'url': item_log.request_url,
                    'host' : item_log.host,
                }
            )
        
        #jumlah acces log 
        count = filtered_log.count()
        
        return Response({
            'count' : count,
            'data'  : filter_array
        }) 
 
# Menggunakan LimitOffsetPagination
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Default jumlah item per halaman
    max_limit = 100  # Batas maksimum item per halaman

class getAccessApiView (APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client_address', 'http_status']  # Tambahkan field yang ingin difilter
    search_fields = ['request_url', 'host', 'client_address', 'timestamp', 'http_status', 'bytes']  # Tambahkan field untuk fitur search
    pagination_class = CustomLimitOffsetPagination

    def post(self, request):
        # Mendapatkan server terkait
        server_id = request.data.get('server_id')
        
        # Akses log yang telah terfilterisasi
        filtered_log = AccessLog.objects.filter(server=server_id)

        # Pagination
        paginator = CustomLimitOffsetPagination()
        result_page = paginator.paginate_queryset(filtered_log, request)
        
        # Membuat array log
        filter_array = [
            {
                'timestamp': item_log.timestamp,
                'timetaken': item_log.elapsed_time,
                'ip_address': item_log.client_address,
                'http_status': item_log.http_status,
                'bytes': item_log.bytes,
                'methode': item_log.request_method,
                'url': item_log.request_url,
                'host': item_log.host,
            }
            for item_log in result_page
        ]

        # Jumlah access log
        count = filtered_log.count()

        return paginator.get_paginated_response({
            'count': count,
            'data': filter_array,
        })
            
        
        
        
        