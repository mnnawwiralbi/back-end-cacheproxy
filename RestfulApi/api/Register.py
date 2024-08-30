from rest_framework import status, generics
from rest_framework.response import Response
from RestfulApi.serializer.AuthSerializer import AuthSerializer, AuthenticationSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAdminUser
from RestfulApi.serializer.RegisterSerializer import AccountSerializerRegisterSuperUser, AccountSerializerRegister

class RegisterSuperUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializerRegisterSuperUser
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': 'Failed to fetch data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()  # This will call the create method in the serializer
            return Response({'message': 'Success: Data created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Failed to create data', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializerRegister
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': 'Failed to fetch data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()  # This will call the create method in the serializer
            return Response({'message': 'Success: Data created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Failed to create data', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
