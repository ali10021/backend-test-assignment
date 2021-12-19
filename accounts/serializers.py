from rest_framework import serializers
from .models import(
    User,
    Country,
)
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    
    confirmPassword = serializers.CharField(max_length=200, write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirmPassword', 'first_name', 'last_name', 'gender', 'age', 'city','country')
        write_only_fields = ['confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True},
        }
        
        
    def validate(self, attrs):
        if self.instance != None:
            if attrs.get('confirmPassword'):        
                if attrs['confirmPassword'] == attrs['password']:
                    del attrs['confirmPassword']
                    return super().validate(attrs)
                else:
                    raise serializers.ValidationError("passwords did not match")
            else:
                return super().validate(attrs)
        
        else:
            if attrs['confirmPassword'] == attrs['password']:
                del attrs['confirmPassword']
                return super().validate(attrs)
            else:
                raise serializers.ValidationError("passwords did not match")    
        
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        # hashing the password for security
        user.set_password(user.password)
        user.save()
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'gender', 'age', 'country', 'city')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
