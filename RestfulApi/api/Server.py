# note yang bisa diimport hanyalah class ataupun function

from rest_framework import generics
from rest_framework import pagination
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from RestfulApi.models import ProxyServerInfo
from RestfulApi.serializer.ServerSerializer import ServerSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class ServerGet (generics.ListCreateAPIView):
    queryset = ProxyServerInfo.objects.all()
    serializer_class = ServerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
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

class UpdateDeleteServer(generics.RetrieveUpdateDestroyAPIView) :
    queryset = ProxyServerInfo.objects.all()
    serializer_class = ServerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Updated",
            "data": serializer.data
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Deleted",
        }
        return Response(response, status=status.HTTP_200_OK)