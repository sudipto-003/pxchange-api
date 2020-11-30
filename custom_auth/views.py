from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import *
from .models import C_User
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.urls import reverse
from .utils import Util
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserRegistration(generics.GenericAPIView):
    serializer_class = UserRegisterSerialize
    permissions = [AllowAny, ]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user).access_token
        domain = get_current_site(request).domain
        rel_url = reverse('user_verification')
        abs_url = f'http://{domain}{rel_url}?token={token}'
        content = f'''\
            Hi {user.username},

            Please verify your account by clicking the following url, and then login in to continue.

            {abs_url}
        '''
        email = {
            'subject': 'User email verification',
            'email_body': content,
            'email_to': user.email
        }
        Util.send_verification_mail(email)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerificationResend(generics.GenericAPIView):
    permissions = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        user_email = request.data['email']
        user = C_User.objects.get(email=user_email)

        token = RefreshToken.for_user(user).access_token
        domain = get_current_site(request).domain
        rel_url = reverse('user_verification')
        abs_url = f'http://{domain}{rel_url}?token={token}'
        content = f'''\
            Hi {user.username},

            Please verify your account by clicking the following url, and then login in to continue.

            {abs_url}
        '''
        email = {
            'subject': 'User email verification link resend',
            'email_body': content,
            'email_to': user.email
        }
        Util.send_verification_mail(email)

        return Response(status=status.HTTP_200_OK)



class UserVerification(generics.GenericAPIView):
    permissions = [AllowAny, ]
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = C_User.objects.get(id=payload['user_id'])
            if not user.verified:
                user.verified = True
                user.is_active = True
                user.save()
            
            #return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return HttpResponseRedirect(redirect_to='http://localhost:8080/#/login')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        try:
            u_pk = kwargs.get('pk', None)
            if u_pk:
                user = C_User.objects.get(pk=kwargs['pk'])
            else:
                user = request.user
        except C_User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)

        return Response(serializer.data)


class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permissions = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class UserLogout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request, *args, **kwargs):
        try:
            token = request.data['refresh_token']
            RefreshToken(token).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'error': 'Bad Token'}, status=status.HTTP_400_BAD_REQUEST)


class Ping(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to='http://localhost:8080/#/login')