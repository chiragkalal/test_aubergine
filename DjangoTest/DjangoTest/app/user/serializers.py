from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, max_length=255)
    name = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'name', 'city', 'password')

    def validate(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if user:
            raise serializers.ValidationError(
                {'email': 'User With this email is already exist in the system.'}
            )

        return validated_data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, validated_data):
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = authenticate(username=email, password=password)
        
        if user.first_time_login == False:
            user.first_time_login = True
            user.refresh_token = user.generate_refresh_token()
        
        user.save()

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'access_token': user.token,
            'refresh_token': user.refresh_token
        }