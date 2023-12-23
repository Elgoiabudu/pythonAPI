from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

@api_view(['GET'])
def get_users(request):    
    if request.method == 'GET':
        users = User.objects.all()                          #Retorna todos os objetos User do banco de dados (Retorna um QUERYSET)
        serializer = UserSerializer(users, many=True)       #Serializa o objeto data em um Json (Tem varios parametros pois é um QUERYSET)
        return Response(serializer.data)                    #Retorna os dados serializados
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def get_by_nick(request, nick):    
    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = UserSerializer(user)
        return Response(serializer.data) 

    if request.method == 'PUT': #Modo mais simplificado para fazer um put. Atenção: caso o nick já exista ele cria um novo registro.
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#CRUD completo
@api_view(['GET','POST','PUT','DELETE'])
def user_manager(request):

    #Buscando um Registro
    if request.method == 'GET':        
        try:                                                                #Checa se existe um parametro user (/?user=...)
            if request.GET['user']:
                user_nickname = request.GET['user']                         #Realiza o GET pelo parametro
                try:
                    user = User.objects.get(pk=user_nickname)               #Faz o GET do objeto no banco de dados 
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserSerializer(user)                           #Serializa o objeto data em um Json
                return Response(serializer.data)                            #Retorna o objeto data serializado
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                    
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    #Criando um novo registro
    if request.method == 'POST':
        new_user = request.data
        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    #Editando um registro
    if request.method == 'PUT':        
        nickname = request.data['user_nickname']                                #Recebe o valor a ser buscado na base de dados
        
        try:                                                                    #Tenta Verifica se o valor existe na base de dados
            update_user = User.objects.get(pk=nickname)                         #Realiza a busca na base de dados
        
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)                   #Caso o valor não exista na base de dados, retorna 404

        serializer = UserSerializer(update_user, data=request.data)             #Caso o valor ersteja de acordo, os dados são serializados

        if serializer.is_valid():                                               #Se o objeto for valido
            serializer.save()                                                   #Atualizando o registro
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)    #Registro atualizado, retorna 201
    
        return Response(status=status.HTTP_404_NOT_FOUND)                       #Caso o valor não exista na base de dados, retorna 404
    
    #Deletando um registro
    if request.method == 'DELETE':        
        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)