# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken

# # Serializer for user registration
# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user

# # Serializer for user details
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']

# # Serializer to get token for a user
# class UserTokenSerializer(serializers.ModelSerializer):
#     token = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'token']

#     def get_token(self, obj):
#         refresh = RefreshToken.for_user(obj)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token,Product,Cart

class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']  # Include phone number

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),  # Hash the password
            phone=validated_data.get('phone', '')
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone']  # Include phone number

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category']


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    class Meta:
        model = Cart  # Assuming you have a Cart model
        fields = ['user', 'product','quantity']  # Adjust according to your fields