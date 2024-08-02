from .import serializers
from django.shortcuts import render, redirect
from rest_framework import viewsets
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import login,logout
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import DepositSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordChangeSerializer
from .serializers import UserSerializer
from rest_framework import mixins, generics
import logging

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileList(generics.ListCreateAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return models.UserProfile.objects.filter(user_id=user_id) 
    

class UserRegistrationsApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'http://pet-adopt-website-picku.onrender.com/user/activate/{uid}/{token}/'
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your email for confirmation")
        return Response(serializer.errors)

    
def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                request.session['user_id'] = user.id 
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credentials"})
        return Response(serializer.errors)
                       
                                             
class UserLogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    

    
class DepositAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = DepositSerializer

    def get_object(self):
        # Retrieve the UserProfile instance for the authenticated user
        return self.queryset.get(user=self.request.user)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    
    
class PasswordChangeView(APIView):
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully. A confirmation email has been sent to your email address."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   