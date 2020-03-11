from ..models import Consumer
from product.models import Product
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        # fields = ['con_name', 'status', 'email', 'phone']
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = ['con_name', 'status', 'email', 'phone', 'username']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        # fields = ['pro_name', 'pro_price', 'exp_duration']
        fields = []
