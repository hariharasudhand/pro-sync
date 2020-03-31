from ..models import Consumer
from product.models import Product
from rest_framework import serializers
from django.contrib.auth.models import User

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = ['con_name', 'status', 'email', 'phone', 'username']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = []


class RetailerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = []