from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
from django.shortcuts import render, redirect
from rest_framework import viewsets
from . import models
from . import serializers
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
from .models import UserAccount
from .serializers import DepositSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordChangeSerializer
# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset=models.UserProfile.objects.all()
    serializer_class=serializers.UserProfileSerializer
    

class UserRegistrationsApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'http://127.0.0.1:8000/user/activate/{uid}/{token}/'
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
    def post(self,request):
        serializer=serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']  
            
            user=authenticate(username=username,password=password)   
            
            if user:
                token,_=Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':"Invalid Credential"})
        return Response(serializer.errors)
                       
                                             
class UserLogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    
    
class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_account = get_object_or_404(UserAccount, user=request.user)
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user_account=user_account)
            return Response({"message": "Deposit successful", "new_balance": user_account.balance}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully. A confirmation email has been sent to your email address."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   