from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from RestfulApi.models import SquidLog
from RestfulApi.serializer.SquidSerializer import SquidLogSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter



class getCache (generics.ListCreateAPIView):
    queryset = SquidLog.objects.all()
    serializer_class = SquidLogSerializer
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


class CacheUpdateDelete (generics.RetrieveUpdateDestroyAPIView):
    queryset = SquidLog.objects.all()
    serializer_class = SquidLogSerializer
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
