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


         
    
    
