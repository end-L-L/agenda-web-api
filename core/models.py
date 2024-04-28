from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.core.validators import MinValueValidator

# Token de Autenticación
class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


# Perfil de Usuario
class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    identifier = models.CharField(max_length=255,null=True, blank=True)
    start_time = models.CharField(max_length=255,null=True, blank=True)
    end_time = models.CharField(max_length=255,null=True, blank=True)
    job = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil de Usuario: "+ "Nombre: " +self.user.first_name+" Job: "+self.job


# Contacto Personal    
class Personal_Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    cp = models.CharField(max_length=255,null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    phone_1 = models.CharField(max_length=255,null=True, blank=True)
    phone_2 = models.CharField(max_length=255,null=True, blank=True)
    relationship = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return "Contacto Personal: "+ "ID: " +self.id+" Name: "+self.name
    

# Contacto Empresarial
class Business_Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    sector = models.CharField(max_length=255,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    cp = models.CharField(max_length=255,null=True, blank=True)
    legal_representative = models.CharField(max_length=255,null=True, blank=True)
    phone_1 = models.CharField(max_length=255,null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return "Contacto Empresarial: "+ "ID: " +self.id+" Name: "+self.name