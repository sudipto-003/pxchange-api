from rest_framework import serializers
from .models import C_User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerialize(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = C_User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords don\'t match')
        
        data.pop('password2')
        return data

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(
            validated_data['email'],
            validated_data['password']
        )

        user.username = validated_data['username']
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        user = C_User.objects.get(email=obj['email'])

        ut = RefreshToken.for_user(user)

        return {'refresh': str(ut), 'access': str(ut.access_token)}

    def validate(self, data):
        user = authenticate(**data)

        if not user:
            raise AuthenticationFailed('Invalid email or password')
        if not user.verified:
            raise AuthenticationFailed('User email is not verified')
        if not user.is_active:
            raise AuthenticationFailed('User account is blocked. Contracct Admin')
        
        return data

    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = C_User
        fields = ['email', 'username', 'verified', 'is_active', 'auth_provider']
