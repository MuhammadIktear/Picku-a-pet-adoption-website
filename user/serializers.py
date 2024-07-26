from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import UserAccount,UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email= serializers.SerializerMethodField()
    class Meta:
        model = models.UserProfile
        fields = '__all__'       
    def get_username(self, obj):
        return obj.user.username 
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name  
    def get_email(self, obj):
        return obj.user.email                     
        

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active=False
        account.save()
        last_account = UserAccount.objects.all().order_by('account_no').last()
        if last_account:
            account_no = last_account.account_no + 1
        else:
            account_no = 10000

        user_account = UserAccount(user=account, account_no=account_no, balance=0)
        user_account.save()
        UserProfile.objects.create(user=account)
        return account

    
class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

class UserAccountSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True, source='user.userprofile')

    class Meta:
        model = UserAccount
        fields = ['id', 'account_no', 'balance', 'user', 'user_profile']        
    
class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be greater than zero.")
        return value

    def save(self, user_account):
        amount = self.validated_data['amount']
        user_account.balance += amount
        user_account.save()
        self.send_confirmation_email(user_account.user.email, amount, user_account.balance)
        return user_account

    def send_confirmation_email(self, email, amount, new_balance):
        subject = 'Deposit Confirmation'
        message = f'You have successfully deposited ${amount}. Your new balance is ${new_balance}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        self.send_confirmation_email(user.email)
        return user

    def send_confirmation_email(self, email):
        subject = 'Password Change Confirmation'
        message = 'Your password has been successfully changed.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)   