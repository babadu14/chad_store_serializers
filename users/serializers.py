from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','username','phone_number','password', 'password2','first_name', 'last_name')

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({'password':'passwords do not match'})
            return attrs
        
        def create(self, validated_data):
            validated_data.pop('passowrd2')
            user = User.objects.create_user(**validated_data)
            return user


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required =True)
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password']

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password =  make_password(password)
        return super().update(instance, validated_data)