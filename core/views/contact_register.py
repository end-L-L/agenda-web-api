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

class PersonalContactRV(generics.CreateAPIView):
    
    # Obtener Usuario por ID
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Contacto_Personal, id = request.GET.get("id"))
        user = PersonalContactSerializer(user, many=False).data

        return Response(user, 200)

    # Registrar Contacto Personal
    @transaction.atomic    
    def post(self, request, *args, **kwargs):
        contact = PersonalContactSerializer(data=request.data)
        if contact.is_valid():
            
            #Grab Contact Data
            name = request.data['name']
            address = request.data['address']
            cp = request.data['cp']
            email = request.data['email']
            phone_1 = request.data['phone_1']
            phone_2 = request.data['phone_2']
            relationship = request.data['relationship']
            user = request.user
            existing_contact = Contacto_Personal.objects.filter(email=email).first()

            if existing_contact:
                return Response({"message":"Email "+email+", is already taken"},400)
            
            contact = Contacto_Personal.objects.create( name = name,
                                                        address = address,
                                                        cp = cp,
                                                        email = email,
                                                        phone_1 = phone_1,
                                                        phone_2 = phone_2,
                                                        relationship = relationship,
                                                        user = user )
            contact.save()
            return Response({"profile_created_id": contact.id }, 200)
        return Response(contact.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalContactEV(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        
        contacto = get_object_or_404(Contacto_Personal, id=request.data["id"])
        contacto.name = request.data["name"]
        contacto.address = request.data["address"]
        contacto.cp = request.data["cp"]
        contacto.phone_1 = request.data["phone_1"]
        contacto.phone_2 = request.data["phone_2"]
        contacto.relationship = request.data["relationship"]
        # Crear un objeto datetime naive
        naive_datetime = datetime.now()
        # Convertir el objeto datetime naive en un objeto datetime consciente de la zona horaria
        aware_datetime = timezone.make_aware(naive_datetime, timezone=timezone.get_current_timezone())
        #contacto.update = datetime.now()
        contacto.update = aware_datetime
        contacto.save()
        
        res = PersonalContactSerializer(contacto, many=False).data
        return Response(res,200)