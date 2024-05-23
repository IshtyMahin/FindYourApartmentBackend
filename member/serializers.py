

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
            userId = self.instance.id 
        else: userId=None

        if User.objects.filter(username=attrs['username']).exclude(id=userId).exists():
            raise serializers.ValidationError({"error": f"User with username '{attrs.username}' already exists"})

        if User.objects.filter(email=attrs['email']).exclude(id=userId).exists():
            raise serializers.ValidationError({"error": "A user with that email already exists"})

        return attrs


    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            mobile_number=validated_data['mobile_number'],
            user_type=validated_data['user_type'],
        )
        user.save()
        return user

    def update(self, instance, validated_data):
       
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        instance.save()
        return instance



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self,value):
        try:
           user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "We donot find any user with this email"})
        
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


    
        
        