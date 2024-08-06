from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .import models
from rest_framework.permissions import IsAuthenticated,AllowAny
from .import serializers
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class ContactUsViewset(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ContactUsSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        contact_data = {
            'name': user.username, 
            'email': user.email,
            'message': message
        }

        serializer = self.serializer_class(data=contact_data)
        if serializer.is_valid():
            serializer.save()
            self.send_email(contact_data)

            return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, contact_data):
        subject = 'Received Contact Message'
        message = f"""
        Hello,

        You have received a new contact message.

        Details:
        Name: {contact_data.get('name')}
        Email: {contact_data.get('email')}
        Message: {contact_data.get('message')}

        Best Regards,
        PICKU Team
        """

        recipient_email = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")