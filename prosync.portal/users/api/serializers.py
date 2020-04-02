from ..models import Consumer
from product.models import Product
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = '__all__'


class ConsumerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Consumer
        fields = ['con_name', 'email', 'phone', 'username', 'password', 'password2']

    def save(self, **kwargs):
        consumer = Consumer(
            con_name=self.validated_data['con_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone=self.validated_data['phone'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password_mismatch': 'The two password fields didn’t match.'})

        consumer.password = make_password(password)
        consumer.save()
        return consumer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = []


class RetailerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = []


class AgentRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, **kwargs):

        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password_mismatch': 'The two password fields didn’t match.'})

        user.set_password(password)
        user.save()
        return user