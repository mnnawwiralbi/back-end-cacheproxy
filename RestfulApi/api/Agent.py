from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from RestfulApi.serializer.AgentSerializer import AgentLogSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from RestfulApi.models import UserAgentLog, ProxyServerInfo
import paramiko



class getAgent (generics.ListCreateAPIView):
    queryset = UserAgentLog.objects.all()
    serializer_class = AgentLogSerializer
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


class AgentUpdateDelete (generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAgentLog.objects.all()
    serializer_class = AgentLogSerializer
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


class UpdateAutoAgentLog (APIView) :
    permission_classes = [AllowAny]
    authentication_classes =[TokenAuthentication]
    
    def cachedatabase(self):
        
        # mengambil orm object cache
        cadata = UserAgentLog.objects.all()
        jumlah = cadata.count()
        return jumlah

    def itemparse(self, items):
        # membuat list array
        json_logs = []

        for item in items:
            # Lakukan parsing baris log dan sesuaikan dengan format log Squid
            # Misalnya, jika formatnya adalah "timestamp IP_ADDRESS URL"
            parts = item.split(' ',3)

            if len(parts) >= 3:  # Pastikan ada cukup bagian dalam baris log
                ip = parts[0]
                date = parts[1]+ parts[2]
                device = parts[3]

                # Membuat entitas log dalam format JSON
                log_entry = {
                    'ip': ip,
                    'date' : date,
                    'device': device,
                }

                # Menambahkan entitas log ke dalam list json_logs
                json_logs.append(log_entry)
                
                # mendapatkan jumlah dara cache
                jumlah = len(json_logs)
        
        # mengembalikan nilai
        return json_logs, jumlah


    def get(self, request):
        # try:
            # deklarasi configurasi akun server
            
            # mendapatkan ip server
            server =  ProxyServerInfo.objects.get(id=1)
            
            hostname = server.ip_address
            username = 'root'
            password = 'aldi2102'
            port = 22

            # lokasi squid
            squid_log_path = '/var/log/squid/useragent.log'
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
                    database[i] = UserAgentLog(
                        ip = acceslog[i]['ip'],
                        date = acceslog[i]['date'],
                        device = acceslog[i]['device'],
                        server = server        
                    )
                    
                    database[i].save()

            return Response({
                                'message': 'Data valid',
                                'meta' : 
                                    {
                                       'ip' : acceslog[0]['ip'],
                                       'date' : acceslog[0]['date'],
                                       'device' : acceslog[0]['device']
                                    }
                                ,
                                'data' : 'data user agent log berhasil di update'
                            }, status=status.HTTP_200_OK)

class getAgentApiView (APIView) : 
    permission_classes = [ AllowAny]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request) :
        
        # mendapatkan server terkait 
        server_id = request.data.get('server_id')
        
        # acceslog yang telah ter filterisasi
        filtered_log = UserAgentLog.objects.filter(server=server_id)
        
        # membuat array log
        filter_array = []
        
        for item_log in filtered_log :
            filter_array.append(
                {
                    'ip': item_log.ip,
                    'date' : item_log.date,
                    'device': item_log.device,
                }
            )
        
        #jumlah acces log 
        count = filtered_log.count()
        
        return Response({
            'count' : count,
            'data'  : filter_array
        })