from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from RestfulApi.models import StoreLog
from RestfulApi.serializer.StoreSerializer import StoreLogSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from RestfulApi.models import StoreLog, ProxyServerInfo
import paramiko

class getStore (generics.ListCreateAPIView):
    queryset = StoreLog.objects.all()
    serializer_class = StoreLogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'methode', 'url']
    search_fields = ['id', 'methode', 'url']

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


class StoreUpdateDelete (generics.RetrieveUpdateDestroyAPIView):
    queryset = StoreLog.objects.all()
    serializer_class = StoreLogSerializer
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
        
class UpdateAutoStoreLog (APIView) :
    permission_classes = [AllowAny]
    authentication_classes =[TokenAuthentication]
    
    def cachedatabase(self):
        # mengambil orm object cache
        cadata = StoreLog.objects.all()
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
                realese = parts[1]
                flag = parts[2]
                object_number = parts[3]
                hash = parts[4]
                http = parts[5]
                timestamp_expire = parts[7]
                last_modified= parts[8]
                mime_type = parts[9]
                size = parts[10]
                methode = parts[11]
                url = parts[12]
                

                # Membuat entitas log dalam format JSON
                log_entry = {
                    'timestamp': timestamp,
                    'realese' : realese,
                    'flag': flag,
                    'object_number' : object_number,
                    'hash' : hash,
                    'http' : http,
                    'timestamp_expire': timestamp_expire,
                    'last_modified' : last_modified,
                    'mime_type' : mime_type,
                    'size' : size,
                    'methode' : methode,
                    'url' : url
                }

                # Menambahkan entitas log ke dalam list json_logs
                json_logs.append(log_entry)

                jumlah = len(json_logs)

        return json_logs, jumlah


    def get(self, request):
        try:
        #     # deklarasi configurasi akun server
            
            # mendapatkan ip server
            server =  ProxyServerInfo.objects.get(id=1)
            
            hostname = server.ip_address
            username = 'root'
            password = 'aldi2102'
            port = 22

            # lokasi squid
            squid_log_path = '/var/log/squid/store.log'
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
                    database[i] = StoreLog(
                        timestamp = acceslog[i]['timestamp'],
                        realese = acceslog[i]['realese'],
                        flag = acceslog[i]['flag'],
                        object_number = acceslog[i]['object_number'], 
                        hash = acceslog[i]['hash'],
                        size = acceslog[i]['size'],
                        timestamp_expire = acceslog[i]['timestamp_expire'],
                        url = acceslog[i]['url'],
                        last_modified = acceslog[i]['last_modified'],
                        http = acceslog[i]['http'],
                        mime_type = acceslog[i]['mime_type'],
                        methode = acceslog[i]['methode'],
                        server = server        
                    )
                    database[i].save()

            return Response({
                                'message': 'Data valid',
                                'data' : acceslog[jumlahcase-1]
                            }, status=status.HTTP_200_OK)
            
        except:

            return Response({'message': 'Data in valid'}, status=status.HTTP_400_BAD_REQUEST)
        
class getStoreApiView (APIView) : 
    permission_classes = [ AllowAny]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request) :
        
        # mendapatkan server terkait 
        server_id = request.data.get('server_id')
        
        # acceslog yang telah ter filterisasi
        filtered_log = StoreLog.objects.filter(server=server_id)
        
        # membuat array log
        filter_array = []
        
        for item_log in filtered_log :
            filter_array.append(
                {
                    'timestamp': item_log.timestamp,
                    'release' : item_log.realese,
                    'flag': item_log.flag,
                    'object_number' : item_log.object_number,
                    'hash' : item_log.hash,
                    'http' : item_log.http,
                    'timestamp_expire': item_log.timestamp_expire,
                    'last_modified' : item_log.last_modified,
                    'mime_type' : item_log.mime_type,
                    'size' : item_log.size,
                    'methode' : item_log.methode,
                    'url' : item_log.url
                }
            )
        
        #jumlah acces log 
        count = filtered_log.count()
        
        return Response({
            'count' : count,
            'data'  : filter_array
        })