from rest_framework.validators import UniqueValidator
from webbot.models import Location, Zayavka
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Agent, Supervizor

User = get_user_model()

class ZayavkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zayavka
        fields = '__all__'

class SupervizorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervizor
        fields = ['id', 'supervizer_surname']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    hydra_id_sales = serializers.CharField(max_length=50)
    supervizer = serializers.PrimaryKeyRelatedField(queryset=Supervizor.objects.all())
    surname = serializers.CharField(max_length=255)

    class Meta:
            model = User
            fields = ('username', 'password', 'hydra_id_sales', 'supervizer', 'surname')
            extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password']
        }
        user = User.objects.create_user(**user_data)

        agent_data = {
            'user': user,
            'supervizer': validated_data['supervizer'],
            'surname': validated_data['surname'],
            'hydra_id_sales': validated_data['hydra_id_sales']
        }
        agent = Agent.objects.create(**agent_data)
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'hydra_id']