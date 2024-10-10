from typing import Any, Dict, Tuple
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

from django.db import models

from django.db import models

class ProxyServerInfo(models.Model):
    """
    Tabel ini berisi informasi tentang server proxy.
    """
    server_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255)
    admin_contact = models.EmailField()
    system_operation = models.CharField(max_length=255, default='FreeBsd')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.server_name

class UserAgentLog(models.Model):
    """
    Tabel ini berisi informasi log User-Agent dari permintaan HTTP.
    """
    ip = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ip} - {self.device}"


class AccessLog(models.Model):
    """
    Tabel ini berisi log akses dari Squid Proxy.
    """
    timestamp = models.CharField(max_length=50)
    elapsed_time = models.IntegerField(help_text="Waktu yang dihabiskan untuk permintaan dalam milidetik")
    client_address = models.GenericIPAddressField()
    http_status = models.CharField(max_length=50)
    bytes = models.IntegerField(help_text="Jumlah byte yang dikirim ke klien")
    request_method = models.CharField(max_length=200)
    request_url = models.URLField()
    host = models.CharField(max_length=255, blank=True, null=True)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.client_address}"


class CacheLog(models.Model):
    """
    Tabel ini berisi log cache dari Squid Proxy.
    """
    message = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.cache_status}"


class StoreLog(models.Model):
    """
    Tabel ini berisi log store dari Squid Proxy yang mencatat penyimpanan dan penghapusan objek di cache.
    """
    timestamp = models.CharField(max_length=255)
    realese = models.CharField(max_length=255)
    flag = models.CharField(max_length=255)
    object_number = models.CharField(max_length=255) 
    hash = models.CharField(max_length=50, help_text="Tindakan seperti RELEASE, SWAPOUT, dll.")
    size = models.CharField(max_length=255)
    timestamp_expire = models.CharField(max_length=255)
    url = models.URLField()
    last_modified = models.CharField(max_length=255)
    http = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=255)
    methode = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.methode} - {self.http}"


class SquidLog(models.Model):
    """
    Tabel ini berisi semua jenis log dari Squid Proxy. 
    """
    timestamp = models.DateTimeField()
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)
    access_log = models.ForeignKey(AccessLog, on_delete=models.CASCADE, null=True, blank=True)
    cache_log = models.ForeignKey(CacheLog, on_delete=models.CASCADE, null=True, blank=True)
    store_log = models.ForeignKey(StoreLog, on_delete=models.CASCADE, null=True, blank=True)
    user_agent_log = models.ForeignKey(UserAgentLog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.server.server_name}"
    
class UserData (models.Model) :
    
    kelamin = (
        ('Laki-Laki', 'Laki-Laki'),
        ('Perempuan', 'Perempuan'),
    )
    
    data_owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ID User')
    nama_lengkap = models.CharField(max_length=255, verbose_name='Nama Lengkap')
    no_ktp = models.CharField(max_length=255, verbose_name='No Ktp', blank= False)
    jenis_kelamin = models.CharField(max_length=255, choices=kelamin, verbose_name='Jenis Kelamin')
    no_telp = models.CharField(max_length=255, verbose_name='No Telpon', blank= False)
    tempat_lahir = models.CharField(max_length=255, verbose_name='Tempat Lahir', blank= False)
    tanggal_lahir = models.DateField(verbose_name='Tanggal Lahir', blank= False)
    npwp = models.CharField(max_length=255, verbose_name='NPWP', blank= False)
    agama = models.CharField(max_length=255, verbose_name='Agama')
    alamat_ktp = models.CharField(max_length = 255, verbose_name='Alamat KTP')
    alamat_domisili = models.CharField(max_length=255, verbose_name='Alamat Domisili' )



