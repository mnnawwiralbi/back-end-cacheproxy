
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from rest_framework.response import Response
import paramiko
from RestfulApi.api.updatecache import itemparse, cachedatabase
from RestfulApi.models import AccessLog

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
        
class UpdateDataChace(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.periodical = asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self, code):
        self.periodical.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Lakukan operasi pada database menggunakan data yang diterima
        # Misalnya:
        await sync_to_async(self.update_database)(data)

        # Kirim pesan balik ke WebSocket
        await self.send(text_data=json.dumps({
            'message': 'Data updated successfully'
        }))

    def update_database(self, data):
        # Operasi sinkron untuk memperbarui database
        # Misalnya:
        # my_model_instance = MyModel.objects.get(id=data['id'])
        # my_model_instance.field = data['new_value']
        # my_model_instance.save()
        pass

    async def send_periodic_updates(self):
        try:
            while True:
                # Lakukan operasi yang diperlukan untuk memperbarui database atau aktivitas lainnya
                # Misalnya:
                await sync_to_async(self.update_periodic_data)()

                # Kirim pesan ke WebSocket (opsional)
                await self.send(text_data=json.dumps({
                    'message': 'Periodic update completed'
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
        # deklarasi konfigurasi akun server
        hostname = '192.168.120.41'
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
        stdin, stdout, stderr = parami.exec_command(f"cat {squid_log_path}")

        data = stdout.read().decode()
        error = stderr.read().decode()

        parami.close()

        if error:
            raise Exception(f"Error reading squid log: {error}")

        # parse datacache
        datacache = data.split('\n')

        # mengambil idcache
        idlog, jumlahbase = cachedatabase()

        acceslog, jumlahcase = itemparse(datacache)

        # membuat memory sementara database
        database = [0] * jumlahcase

        # memasukan kedalam database
        if jumlahbase != jumlahcase:
            for i in range(jumlahbase, jumlahcase):
                database[i] = AccessLog(idlog=i, timestamp=acceslog[i]['timestamp'],
                                    ip=acceslog[i]['ip_address'], url=acceslog[i]['url'])
                database[i].save()