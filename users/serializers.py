from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabet characters are allowed.')
    first_name = serializers.CharField(label="First name", required=True, max_length=100, validators=[alpha])
    last_name = serializers.CharField(label="Last name", required=True, max_length=100, validators=[alpha])
    password = serializers.CharField(label="Password", required=True, write_only=True)
    password2 = serializers.CharField(label="Confirm Password", required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
        )
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields don't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user