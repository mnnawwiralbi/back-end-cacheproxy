# Note : cara pemrograman yang baik adala dengan menggunakan algoritmik validasi dan implementasi

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from RestfulApi.api.AccesLog import UpdateAutoAccesLog
from RestfulApi.api.StoreLog import UpdateAutoStoreLog
from RestfulApi.models import AccessLog, ProxyServerInfo, UserAgentLog, StoreLog
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
import paramiko

# membuat example web socket 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

# membuat update data access log        
class UpdateDataAccesLog(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.periodical = asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self, code):
        self.periodical.cancel()

    async def send_periodic_updates(self):
        try:
            while True:
                
                # Lakukan operasi yang diperlukan untuk memperbarui database atau aktivitas lainnya
                # Misalnya:
                
                await sync_to_async(self.update_periodic_data)()

                # Kirim pesan ke WebSocket (opsional)
                await self.send(text_data=json.dumps({
                    'message': 'Periodic update acces completed'
                }))

                # Tunggu selama 10 menit sebelum mengulang
                await asyncio.sleep(3)
                
        except asyncio.CancelledError:
            # Handle cancellation separately if needed
            pass
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f'Periodic update failed: {str(e)}'
            }))

    def update_periodic_data(self):
            server =  ProxyServerInfo.objects.get(id=2)
            
            hostname = server.ip_address
            username = 'root'
            password = '1234'
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
            jumlahbase = UpdateAutoAccesLog.cachedatabase()

            acceslog, jumlahcase = UpdateAutoAccesLog.itemparse(datacache)
        

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
            
# membuat update data store log        
class UpdateDataStoreLog(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.periodical = asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self, code):
        self.periodical.cancel()

    async def send_periodic_updates(self):
        try:
            while True:
                
                # Lakukan operasi yang diperlukan untuk memperbarui database atau aktivitas lainnya
                # Misalnya:
                
                await sync_to_async(self.update_periodic_data)()

                # Kirim pesan ke WebSocket (opsional)
                await self.send(text_data=json.dumps({
                    'message': 'Periodic update store completed'
                }))

                # Tunggu selama 10 menit sebelum mengulang
                await asyncio.sleep(3)
                
        except asyncio.CancelledError:
            # Handle cancellation separately if needed
            pass
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f'Periodic update failed: {str(e)}'
            }))

    def update_periodic_data(self):
            # deklarasi configurasi akun server
            
            # mendapatkan ip server
            server =  ProxyServerInfo.objects.get(id=2)
            
            hostname = server.ip_address
            username = 'root'
            password = '1234'
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
            jumlahbase = UpdateAutoStoreLog.cachedatabase()

            acceslog, jumlahcase = UpdateAutoStoreLog.itemparse(datacache)
        

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
                        server = acceslog[i]['server']        
                    )
                    database[i].save()

            return Response({
                                'message': 'Data valid',
                                'data' : acceslog[jumlahcase-1]
                            }, status=status.HTTP_200_OK)