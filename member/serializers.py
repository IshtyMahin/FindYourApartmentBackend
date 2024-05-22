

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_number', 'user_type', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def validate(self, attrs):
        if 'password' in attrs and attrs['password'] != attrs.get('confirm_password'):
            raise serializers.ValidationError({"error": "Passwords don't match."})

        if self.instance:
            user_id = self.instance.id 
        else: user_id=None

        if User.objects.filter(username=attrs['username']).exclude(id=user_id).exists():
            raise serializers.ValidationError({"error": "Username already exists."})

        if User.objects.filter(email=attrs['email']).exclude(id=user_id).exists():
            raise serializers.ValidationError({"error": "Email already exists."})

        return attrs


    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        user.mobile_number = validated_data.get('mobile_number', '')
        user.user_type = validated_data.get('user_type', 'normal')
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)