from typing import Any, Dict, Tuple
from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.server_name

class UserAgentLog(models.Model):
    """
    Tabel ini berisi informasi log User-Agent dari permintaan HTTP.
    """
    timestamp = models.DateTimeField()
    user_agent = models.CharField(max_length=1024)
    ip_address = models.GenericIPAddressField()
    request_url = models.URLField()
    http_method = models.CharField(max_length=10)
    response_status = models.CharField(max_length=10)
    response_size = models.IntegerField()
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.user_agent}"


class AccessLog(models.Model):
    """
    Tabel ini berisi log akses dari Squid Proxy.
    """
    timestamp = models.DateTimeField()
    elapsed_time = models.IntegerField(help_text="Waktu yang dihabiskan untuk permintaan dalam milidetik")
    client_address = models.GenericIPAddressField()
    result_code = models.CharField(max_length=50)
    bytes = models.IntegerField(help_text="Jumlah byte yang dikirim ke klien")
    request_method = models.CharField(max_length=10)
    request_url = models.URLField()
    username = models.CharField(max_length=255, blank=True, null=True)
    hierarchy_code = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.client_address}"


class CacheLog(models.Model):
    """
    Tabel ini berisi log cache dari Squid Proxy.
    """
    timestamp = models.DateTimeField()
    cache_status = models.CharField(max_length=50, help_text="Status cache seperti HIT, MISS, dll.")
    client_address = models.GenericIPAddressField()
    bytes = models.IntegerField(help_text="Jumlah byte yang di-cache")
    request_method = models.CharField(max_length=10)
    request_url = models.URLField()
    mime_type = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.cache_status}"


class StoreLog(models.Model):
    """
    Tabel ini berisi log store dari Squid Proxy yang mencatat penyimpanan dan penghapusan objek di cache.
    """
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=50, help_text="Tindakan seperti RELEASE, SWAPOUT, dll.")
    object_size = models.IntegerField(help_text="Ukuran objek dalam byte")
    request_url = models.URLField()
    client_address = models.GenericIPAddressField()
    http_status = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=255)
    server = models.ForeignKey(ProxyServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.request_url}"


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




# class Server(models.Model):
#     SERVER_TYPES = (
#         ('postgresql', 'PostgreSQL'),
#         ('squid', 'Squid'),
#     )

#     name = models.CharField(max_length=255)
#     ip_address = models.GenericIPAddressField()
#     server_type = models.CharField(max_length=20, choices=SERVER_TYPES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Server'
#         verbose_name_plural = 'Servers'

#     def __str__(self):
#         return f"{self.name} ({self.get_server_type_display()})"


# class Cache(models.Model):
#     server = models.ForeignKey(
#         Server, on_delete=models.CASCADE, related_name='caches')
#     key = models.CharField(max_length=255)
#     value = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['server', 'key']
#         verbose_name = 'Cache'
#         verbose_name_plural = 'Caches'

#     def __str__(self):
#         return f"{self.key} on {self.server.name}"


# class MonitoringMetric(models.Model):
#     server = models.ForeignKey(
#         Server, on_delete=models.CASCADE, related_name='metrics')
#     metric_name = models.CharField(max_length=255)
#     value = models.FloatField()
#     recorded_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-recorded_at']
#         verbose_name = 'Monitoring Metric'
#         verbose_name_plural = 'Monitoring Metrics'

#     def __str__(self):
#         return f"{self.metric_name} for {self.server.name} at {self.recorded_at}"


# class User (models.Model):
#     Activate_Coice = (
#         (True, 'Activate'),
#         (False, 'Deactivate'),
#     )
#     userid = models.CharField(
#         max_length=20, primary_key=True, default="not fill yet", null=False)
#     username = models.CharField(
#         max_length=20, primary_key=False, default="not fill yet", null=False, verbose_name='User Name')
#     password = models.CharField(
#         max_length=20, primary_key=False, default="not fill yet", null=False, verbose_name='User Password')
#     email = models.EmailField(
#         max_length=20, primary_key=False, default="not fill yet", null=False, unique=True, verbose_name='User Email')
#     image = models.ImageField(upload_to='user_images/', blank=True, null=True)
#     activate = models.BooleanField(choices=Activate_Coice)
#     date_create = models.DateField(auto_now=True)


# class AccessLog(models.Model):
#     timestamp = models.DateTimeField()
#     ip_address = models.GenericIPAddressField()
#     method = models.CharField(max_length=8)  # e.g., GET, POST
#     url = models.URLField()
#     http_version = models.CharField(max_length=8)  # e.g., HTTP/1.1
#     response_code = models.IntegerField()  # HTTP status code
#     response_size = models.IntegerField()  # Size of response in bytes
#     referer = models.URLField(blank=True, null=True)  # Referer URL
#     user_agent = models.TextField(blank=True, null=True)  # User-Agent string

#     class Meta:
#         verbose_name = "Access Log"
#         verbose_name_plural = "Access Logs"
#         ordering = ['-timestamp']

#     def __str__(self):
#         return f"{self.timestamp} - {self.ip_address} - {self.url} - {self.response_code}"


# class StoreLog(models.Model):
#     timestamp = models.FloatField()  # Untuk menyimpan timestamp
#     status = models.CharField(max_length=10)  # Status response (RELEASE, etc.)
#     request_id = models.CharField(max_length=50)  # ID permintaan
#     cache_key = models.CharField(max_length=100)  # Kunci cache
#     http_status_code = models.IntegerField()  # Kode status HTTP
#     time_taken = models.FloatField()  # Waktu yang diambil
#     response_size = models.IntegerField()  # Ukuran respons
#     error_code = models.IntegerField()  # Kode error
#     content_type = models.CharField(max_length=50)  # Jenis konten
#     size = models.CharField(max_length=20)  # Ukuran
#     method = models.CharField(max_length=10)  # Metode HTTP (GET, POST, etc.)
#     url = models.URLField()  # URL yang diakses

#     class Meta:
#         verbose_name = "Squid Log"
#         verbose_name_plural = "Squid Logs"
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.timestamp} - {self.method} {self.url}"


# class RefererLog(models.Model):
#     # Tanggal dan waktu ketika permintaan dilakukan
#     timestamp = models.DateTimeField()
#     src_ip = models.GenericIPAddressField()  # Alamat IP sumber
#     # Nama pengguna (jika ada)
#     username = models.CharField(max_length=100, blank=True, null=True)
#     referrer = models.URLField(max_length=200)  # URL referer
#     url = models.URLField(max_length=200)  # URL yang diminta
#     status_code = models.IntegerField()  # Kode status HTTP
#     size = models.IntegerField()  # Ukuran respons dalam byte

#     class Meta:
#         verbose_name = "Referer Log"
#         verbose_name_plural = "Referer Logs"
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.timestamp} - {self.src_ip} - {self.url}"


# class UserAgentLog(models.Model):
#     # Tanggal dan waktu ketika permintaan dilakukan
#     timestamp = models.DateTimeField()
#     src_ip = models.GenericIPAddressField()  # Alamat IP sumber
#     # Nama pengguna (jika ada)
#     username = models.CharField(max_length=100, blank=True, null=True)
#     user_agent = models.TextField()  # String user agent
#     url = models.URLField(max_length=200)  # URL yang diminta
#     status_code = models.IntegerField()  # Kode status HTTP
#     size = models.IntegerField()  # Ukuran respons dalam byte

#     class Meta:
#         verbose_name = "User Agent Log"
#         verbose_name_plural = "User Agent Logs"
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.timestamp} - {self.src_ip} - {self.user_agent}"
