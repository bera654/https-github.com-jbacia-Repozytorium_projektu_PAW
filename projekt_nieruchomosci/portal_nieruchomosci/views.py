from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Klient, Agent
from .serializers import KlientSerializer, AgentSerializer



@api_view(["GET", "POST"])
def klient_list(request):

    
    if request.method == "GET":
        klienci = Klient.objects.all()
        serializer = KlientSerializer(klienci, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = KlientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def klient_detail(request, pk):
    
    try:
        klient = Klient.objects.get(pk=pk)
    except Klient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = KlientSerializer(klient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = KlientSerializer(klient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        klient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def klient_search(request):
   
    query = request.GET.get("q", "")
    klienci = Klient.objects.filter(nazwisko__icontains=query)
    serializer = KlientSerializer(klienci, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET", "POST"])
def agent_list(request):
    
    if request.method == "GET":
        agenci = Agent.objects.all()
        serializer = AgentSerializer(agenci, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def agent_detail(request, pk):
   
    try:
        agent = Agent.objects.get(pk=pk)
    except Agent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AgentSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
