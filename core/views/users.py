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
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date

class RegisterView(generics.CreateAPIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grab user data
            role = 'user'
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password1']

            existing_user = User.objects.filter(email=email).first()
            existing_identifier = Profiles.objects.filter(identifier=request.data["identifier"]).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)
            
            if existing_identifier:
                return Response({"message":"Identifier "+request.data["identifier"]+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Create a profile for the user
            profile = Profiles.objects.create(user=user, 
                                              identifier=request.data["identifier"], 
                                              job=request.data["job"], 
                                              start_time=request.data["start_time"], 
                                              end_time=request.data["end_time"])
            profile.save()

            return Response({"profile_created_id": profile.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    