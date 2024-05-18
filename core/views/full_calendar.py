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


class AgendaRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Registrar Evento en Agenda
    @transaction.atomic
    
    def post(self, request, *args, **kwargs):
        task = TaskSerializer(data=request.data)
        if task.is_valid():
            # Crear Tarea
            task = Agenda.objects.create(title=request.data['title'],
                                         date=request.data['date'],
                                         start=request.data['start'],
                                         end=request.data['end'],
                                         partner=request.data['partner'],
                                         place=request.data['place'],
                                         description=request.data['description'],
                                         user = request.user)
            task.save()
            
            return Response({"id": task.id}, 201)
        
        return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar Evento en Agenda
    def delete(self, request, *args, **kwargs):
        task = get_object_or_404(Agenda, id=request.GET.get("id"))
        try:
            task.delete()
            return Response({"message":"event deleted"},200)
        except Exception as e:
            return Response({"message":"error"},400)

class TasksByUser(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        task = Agenda.objects.filter(user = request.user).order_by("id")
        lista = AgendaSerializer(task, many=True).data
        
        return Response(lista, 200)


class ContactNamesByUser(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        personal_contacts = Personal_Contact.objects.filter(user=request.user)
        personal_contact_names = [contact.name for contact in personal_contacts]

        business_contacts = Business_Contact.objects.filter(user=request.user)
        business_contact_names = [contact.name for contact in business_contacts]

        all_contact_names = {
            "personal_contacts": personal_contact_names,
            "business_contacts": business_contact_names
        }

        return Response(all_contact_names, 200)