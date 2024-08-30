from rest_framework import status, generics
from rest_framework.response import Response
from RestfulApi.serializer.AuthSerializer import AuthSerializer, AuthenticationSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class AuthApi (APIView):
    queryset =  User.objects.all()
    serializer = AuthSerializer
    
    def post(self, request) :
        serializer = self.serializer(data = request.data)
        if serializer.is_valid() :
            return Response(serializer.validated_data, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

class Auth (generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthenticationSerializer
    permission_classes= [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)