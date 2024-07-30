from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""

    class Meta:
        model = User
        exclude = ['id', 'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'groups',
                   'user_permissions', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint"""
    old_password = serializers.CharField(required=True, validators=[validate_password])
    new_password = serializers.CharField(required=True, validators=[validate_password])
