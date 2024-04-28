from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from core.serializers import *
from core.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date

class BusinessContactAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        contact = Business_Contact.objects.filter(user__is_active = 1).order_by("id")
        lista = BusinessContactSerializer(contact, many=True).data
      
        return Response(lista, 200)
    
class BusinessContactByUser(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        contact = Business_Contact.objects.filter(user = request.user).order_by("id")
        lista = BusinessContactSerializer(contact, many=True).data

        return Response(lista, 200)

class BusinessContactRV(generics.CreateAPIView):
    
    # Obtener contact por ID
    def get(self, request, *args, **kwargs):
        contact = get_object_or_404(Business_Contact, id = request.GET.get("id"))
        contact = BusinessContactSerializer(contact, many=False).data

        return Response(contact, 200)

    # Registrar contact Empresarial
    @transaction.atomic    
    def post(self, request, *args, **kwargs):
        contact = BusinessContactSerializer(data=request.data)
        if contact.is_valid():
         
            # Grab Contact Data
            name = request.data['name']
            sector = request.data['sector']
            address = request.data['address']
            cp = request.data['cp']
            legal_representative = request.data['legal_representative']
            phone_1 = request.data['phone_1']
            email = request.data['email']
            user = request.user
            existing_contact = Business_Contact.objects.filter(email=email).first()

            if existing_contact:
                return Response({"message":"Email "+email+", is already taken"},400)
         
            contact = Business_Contact.objects.create(  name = name,
                                                        sector = sector,
                                                        address = address,
                                                        cp = cp,
                                                        legal_representative = legal_representative,
                                                        phone_1 = phone_1,
                                                        email = email,
                                                        user = user)
            contact.save()
            return Response({"contact_created_id": contact.id }, 200)
        return Response(contact.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessContactEV(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
     
        # Grab Contact Data
        contact = get_object_or_404(Business_Contact, id = request.data['id'])
        contact.name = request.data['name']
        contact.sector = request.data['sector']
        contact.address = request.data['address']
        contact.cp = request.data['cp']
        contact.legal_representative = request.data['legal_representative']
        contact.phone_1 = request.data['phone_1']
        contact.email = request.data['email']
        contact.save()

        response = BusinessContactSerializer(contact, many=False).data
        return Response({"contact_updated_id": contact.id }, 200)
   

      
   
   
