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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Agent

#lista properties
def property_list_html(request):
    properties = Property.objects.all()
    return render(
        request,
        "portal_nieruchomosci/property/list.html",
        {"properties": properties}
    )

def property_detail_html(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(
        request,
        "portal_nieruchomosci/property/detail.html",
        {"property": property_obj}
    )

#lista agents
def agent_list_html(request):
    agents = Agent.objects.all()
    return render(request, "portal_nieruchomosci/agent/list.html", {"agents": agents})

#detale agentow
def agent_detail_html(request, id):
    agent = get_object_or_404(Agent, id=id)
    return render(request, "portal_nieruchomosci/agent/detail.html", {"agent": agent})


#lista klientow html
def klient_list_html(request):
    klienci = Klient.objects.all()
    return render(
        request,
        "portal_nieruchomosci/klient/list.html",
        {"klienci": klienci}
    )


#dodawanie klienta htmll
def klient_create_html(request):
    if request.method == "GET":
        # tylko wyświetlamy pusty formularz
        return render(
            request,
            "portal_nieruchomosci/klient/create.html",
            {}
        )

    elif request.method == "POST":
        imie = request.POST.get("imie")
        nazwisko = request.POST.get("nazwisko")
        plec = request.POST.get("plec")

        #validation
        if not (imie and nazwisko and plec):
            error = "Wszystkie pola są wymagane."
            return render(
                request,
                "portal_nieruchomosci/klient/create.html",
                {"error": error}
            )

        #nowy klient
        Klient.objects.create(
            imie=imie,
            nazwisko=nazwisko,
            plec=plec
        )
        return redirect("klient-list-html")

def klient_search_html(request):
    query = request.GET.get("q", "")  # pobieramy ?q= z URL, domyślnie pusty string

    if query:
        klienci = Klient.objects.filter(nazwisko__icontains=query)
    else:
        klienci = Klient.objects.none()  # pusta lista gdy brak zapytania

    return render(
        request,
        "portal_nieruchomosci/klient/search.html",
        {"klienci": klienci, "query": query}
    )
