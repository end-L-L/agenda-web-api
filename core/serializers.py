from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class ProfilesSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Profiles
        fields = "__all__"

class PersonalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Contact
        fields = "__all__"

class BusinessContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Contact
        fields = "__all__"