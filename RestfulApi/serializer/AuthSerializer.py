# Note : bahwa token respon tidak bisa di dalam respon
# Note : rest frame work mendukung serilaizer untuk melakukan validator secara induvidu maupun dalam satu enkapsulasi object
# Note : rest frame work juga mendkung serlializer untuk melakukan inputan data multiple
# context : dapat  digunakan untuk layaknya verbose name ini diserializer misal (dara=data, context)
# Note : serializers tidak boleh mengembalikan nilai espon
# Note : enpoint api bisa menggunakan beberapa proses atentikasi sekaligus untuk mencari yang paling benar
# Note : variabel django memiliki decode dan encode
# Note : Authentication memiliki base autentikasi
# Note : menambahkan fungsi get authorization
# Note : access token memang ada di dokmentasi restfraework

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import User

import base64
import binascii

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.translation import gettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions

# Authentication Serializer


class AuthenticationSerializer (serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def get_jwt_token(self, user):
        pengguna = user
        token_raw = RefreshToken.for_user(pengguna)
        return token_raw, token_raw.access_token

    def validate(self, attrs):
        try:
            # mengambil username dan password dari imput user
            username = attrs.get('username')
            password = attrs.get('password')

            # autenticate user
            user = authenticate(username=username, password=password)
            validasi_key_token_null = Token.objects.filter(user=user)

            # mengambil key
            if user and validasi_key_token_null:
                token = Token.objects.get(user=user)
                jwt_refresh, jwt_access = self.get_jwt_token(user)
                respon = {
                    "user_id": user.id,
                    "key": token.key,
                    "jwt_refresh": str(jwt_refresh),
                    "jwt_access": str(jwt_access),
                    "status": status.HTTP_200_OK,
                    "message": True
                }
                return respon
            elif user:
                token, created = Token.objects.get_or_create(user=user)
                jwt_refresh, jwt_access = self.get_jwt_token(user)
                respon = {
                    "user_id": user.id,
                    "key": token.key,
                    "jwt_refresh": str(jwt_refresh),
                    "jwt_access": str(jwt_access),
                    "status": status.HTTP_200_OK,
                    "message": True
                }
                return respon
            else:
                raise serializers.ValidationError(
                    "Username atau password tidak valid.")

        except:
            respon = {
                "user_id": None,
                "key": None,
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "message": False
            }
            return respon


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication (BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword


class DoubleTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):

        header = get_authorization_header(request)

        if (isinstance(auth, bytes)):
            auths = header.decode(HTTP_HEADER_ENCODING)

        auth = auths.split()

        if len(auth) != 3:
            raise AuthenticationFailed('Autentikasi Gagal')

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        
        elif len(auth) > 3:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        jwt_token = auth[1]  # Token Simple JWT
        auth_token = auth[2]  # Token AuthToken

        user = None

        # Validasi Token Simple JWT
        try:
            # Decode token untuk mendapatkan user dari Simple JWT
            payload = AccessToken(jwt_token)
            user = User.objects.get(id=payload['user_id'])
        except Exception:
            raise AuthenticationFailed('JWT token is invalid or expired.')

        # Validasi AuthToken
        try:
            auth_token_instance = Token.objects.get(key=auth_token)
            if auth_token_instance.user != user:
                raise AuthenticationFailed(
                    'Auth token is invalid or does not match user for the JWT.')
        except Token.DoesNotExist:
            raise AuthenticationFailed('Auth token is invalid.')

        # Token validasi sukses
        return (user, None)  # Mengembalikan user jika berhasil


def email_filter(value) :
    email_split = value.split('@')
    email_domain = email_split[1].split('.')
    email_provider = email_domain[0]

    if (email_provider) :
        raise serializers.ValidationError('Tidak Boleh Masukan Email Gmail')

    return value

class AuthSerializer (serializers.Serializer):
    email = serializers.EmailField(validators=[email_filter])
    # Note function validators bisa di gunakan ke complete set fields melewati kelas meta



# Dibawah ini merupakan valdator yang digunakan untuk dalam kelas meta
# from rest_framework import serializers  
# from rest_framework.validators import UniqueTogetherValidator  
# from .models import Event  # pastikan Anda mengimpot model Event  

# class EventSerializer(serializers.ModelSerializer):
#    class Meta:
#       model = User
#       fields = ['id', 'username', 'email']
#       validators = [
#           User.objects.all()
#           fields = ['id', 'username', 'password']
#       ]


# class EventSerializer(serializers.ModelSerializer):  
#    class Meta:  
#        model = Event  # Definisikan model yang sesuai  
#        fields = ['name', 'room_number', 'date']  
#        validators = [  
#            UniqueTogetherValidator(  
#                queryset=Event.objects.all(),  
#                fields=['room_number', 'date']  
#            )  
#        ]