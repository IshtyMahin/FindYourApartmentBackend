
from django.shortcuts import redirect
from rest_framework import viewsets,generics
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from rest_framework.authtoken.models import Token

from .models import User
from django.contrib.auth import authenticate,login,logout 

# for sending email 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
def verify_token(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        userData = serializer.data
        return Response({'message': 'Valid Token','user': userData})
    
    except AuthenticationFailed:
        return Response({'message': 'Invalid Token'})


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def is_superuser(self, request, pk=None):
        user_id = pk
        try:
            user = User.objects.get(pk=user_id)
            return Response({'user_id': user_id,'user_type':user.user_type})
        except User.DoesNotExist:
            return Response({'error': 'User with this id does not exist'})


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ",token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ",uid)
            confirm_link = f"https://findyourapartmentbackend.onrender.com/api/users/active/{uid}/{token}"
            email_subject = "Confirm your Email"
            email_body = render_to_string("confirm_email.html",{"confirm_link":confirm_link})
            email = EmailMultiAlternatives(email_subject, '',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
    
def activate(request,uid64,token):
    try: 
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('https://findyourapartmentbackend.onrender.com/login')
    else:
        return redirect('https://findyourapartmentbackend.onrender.com/register')
    
    
    
class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User with username ' + username+' does not exist'})
            
            user = authenticate(username=username, password=password)
            
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request,user)
                return Response({'token':token.key,'user_type':user.user_type,'user_id':user.id})
            else:
                return Response({'error':'Password is incorrect'})
            
        return Response(serializer.error) 
    
class UserLogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    
    
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = generics.get_object_or_404(User, pk=pk)
        return user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
from .serializers import ResetPasswordRequestSerializer,ResetPasswordSerializer
    
class ResetPasswordRequestView(APIView):
    def post(self,request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://findyourapartmemt.netlify.app/reset_password/{uid}/{token}"
            email_subject = "Request for reset password"
            email_body = render_to_string("resetPassword.html",{"confirm_link":confirm_link})
            email = EmailMultiAlternatives(email_subject, '',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response("Check your mail for password reset email")
        return Response(serializer.errors)

class ResetPasswordView(APIView):
    def post(self,request,uid64,token):
        serializer = ResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            
            try:
                uid = urlsafe_base64_decode(uid64).decode()
                user = User._default_manager.get(pk=uid)
            except(User.DoesNotExist):
                user = None
                
            if user and default_token_generator.check_token(user,token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response("Successfully reset your password")
            else:
                return Response({'error':'Resent password link is not valid'})
            