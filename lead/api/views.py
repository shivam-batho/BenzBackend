from django.shortcuts import render
from urllib import request , response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


@api_view(['POST'])
def loginUser(request):
    serializerToken = GeneratePairTokenSerializer(data = request.data )
    if serializerToken.is_valid():
        return Response(serializerToken.validated_data, status = status.HTTP_202_ACCEPTED)
    return Response(serializerToken.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addUser(request ):
    if request.method == 'POST':
        flat_data = {key: value[0] if isinstance(value, list) else value for key, value in request.POST.items()}
        userSerializer = UserSerializer(data = flat_data)
        if userSerializer.is_valid(raise_exception = True):
            userSerializer.save()
            return Response({'status':201,'message':'User Created Successfully !'} , status=status.HTTP_201_CREATED)
        return Response({'status':400 , 'message':'Failed to Create User !'} , status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def getUsersList(request):
    if request.method == 'GET':
        user = User.objects.all()
        if user:
            userSerializer = UserSerializer(user , many = True)
            return Response({'status':200,'data':userSerializer.data } , status=status.HTTP_200_OK)
        return Response({'status':404, 'message':'No Data Found'} , status=status.HTTP_404_NOT_FOUND)
