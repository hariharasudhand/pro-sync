from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from users.models import Consumer
from . import serializers
from users.api.models import MyOwnToken
from users.models import Consumer, Profile


class ConsumerView(generics.ListAPIView):
    queryset = Consumer.objects.all()
    serializer_class = serializers.ConsumerSerializer


@api_view(['GET', ])
def api_detail_consumer_view(request, id):

    try:
        con = Consumer.objects.get(id=id)

    except Consumer.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.ConsumerSerializer(con)
        return Response(serializer.data)


@api_view(['POST', ])
def api_consumer_register_view(request):
    if request.method == "POST":
        serializer = serializers.ConsumerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            consumer = serializer.save()

            token = MyOwnToken.objects.create(consumer=consumer)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def api_product_check_view(request):
    if request.method == "POST":
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.initial_data.get('token')
            try:
                con = MyOwnToken.objects.get(key=token)
            except MyOwnToken.DoesNotExist:
                return Response(data={'response': "Consumer Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)
            consumer = Consumer.objects.get(id=con.consumer_id)
            data = {
                'response': "Product Patched Successfully",
                'token': token,
                'consumer_name': consumer.con_name,
                'consumer_email': consumer.email,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def api_retailer_login_view(request):
    if request.method == "POST":
        serializer = serializers.RetailerSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.initial_data.get('token')
            username = serializer.initial_data.get('username')
            password = serializer.initial_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                try:
                    tok = Token.objects.get(user=user)
                    if tok.key == token or token == '':
                        return Response({'token': tok.key}, status=status.HTTP_200_OK)
                    else:
                        return Response({'response': "UNAUTHORIZED Token"}, status=status.HTTP_401_UNAUTHORIZED)
                except Token.DoesNotExist:
                    tok = Token.objects.create(user=user)
                    return Response({'token': tok.key}, status=status.HTTP_201_CREATED)
            else:
                try:
                    user_ = User.objects.get(username=username)
                    return Response({'response': "Password Mismatch"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                except User.DoesNotExist:
                    return Response({'response': "Retailer Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def api_agent_register_view(request):
    if request.method == 'POST':
        serializer = serializers.AgentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            phone = serializer.initial_data.get('phone')

            token = Token.objects.create(user=user)

            profile = Profile.objects.get(user_id=user.id)
            profile.phone = phone
            profile.user_token = token.key
            profile.status = 'ACTIVE'
            profile.force_login = True
            profile.save()
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)