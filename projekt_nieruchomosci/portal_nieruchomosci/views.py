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
    if request.method == "POST":
        property_obj.delete()
        return redirect("property-list-html") 
    return render(
        request,
        "portal_nieruchomosci/property/detail.html",
        {"property": property_obj}
    )

def property_update_html(request, id):
    property_obj = get_object_or_404(Property, id=id)

    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/property/update.html",
            {"property": property_obj}
        )

    elif request.method == "POST":
        # pola tekst/liczby
        property_obj.title = request.POST.get("title")
        property_obj.location = request.POST.get("location")
        property_obj.description = request.POST.get("description")
        property_obj.price = request.POST.get("price")
        property_obj.square_meters = request.POST.get("square_meters")

        # checkboxy (True jeśli zaznaczone)
        property_obj.pool = bool(request.POST.get("pool"))
        property_obj.sauna = bool(request.POST.get("sauna"))
        property_obj.jacuzzi = bool(request.POST.get("jacuzzi"))
        property_obj.lift = bool(request.POST.get("lift"))
        property_obj.garage = bool(request.POST.get("garage"))
        property_obj.balcony = bool(request.POST.get("balcony"))
        property_obj.terrace = bool(request.POST.get("terrace"))
        property_obj.garden = bool(request.POST.get("garden"))
        property_obj.AC = bool(request.POST.get("AC"))
        property_obj.safety_system = bool(request.POST.get("safety_system"))
        property_obj.needs_renovation = bool(request.POST.get("needs_renovation"))

        # prosta walidacja
        if not (property_obj.title and property_obj.location and property_obj.price and property_obj.square_meters):
            error = "Tytuł, lokalizacja, cena i metraż są wymagane."
            return render(
                request,
                "portal_nieruchomosci/property/update.html",
                {"property": property_obj, "error": error}
            )

        property_obj.save()
        return redirect("property-detail-html", id=property_obj.id)


#lista agents
def agent_list_html(request):
    agents = Agent.objects.all()
    return render(request, "portal_nieruchomosci/agent/list.html", {"agents": agents})

#detale agentow
def agent_detail_html(request, id):
    agent = get_object_or_404(Agent, id=id)

    if request.method == "POST":
        agent.delete()
        return redirect("agent-list-html")

    return render(
        request,
        "portal_nieruchomosci/agent/detail.html",
        {"agent": agent}
    )

def agent_update_html(request, id):
    agent = get_object_or_404(Agent, id=id)

    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/agent/update.html",
            {"agent": agent}
        )

    elif request.method == "POST":
        agent.first_name = request.POST.get("first_name")
        agent.last_name = request.POST.get("last_name")
        agent.region = request.POST.get("region")
        agent.stanowisko = request.POST.get("stanowisko")

        if not (agent.first_name and agent.last_name and agent.stanowisko):
            error = "Imię, nazwisko i stanowisko są wymagane."
            return render(
                request,
                "portal_nieruchomosci/agent/update.html",
                {"agent": agent, "error": error}
            )

        agent.save()
        return redirect("agent-detail-html", id=agent.id)



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
def klient_detail_html(request, id):
    klient = get_object_or_404(Klient, id=id)

    if request.method == "POST":
        klient.delete()
        return redirect("klient-list-html")

    return render(
        request,
        "portal_nieruchomosci/klient/detail.html",
        {"klient": klient}
    )
def klient_update_html(request, id):
    klient = get_object_or_404(Klient, id=id)

    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/klient/update.html",
            {"klient": klient}
        )

    elif request.method == "POST":
        klient.imie = request.POST.get("imie")
        klient.nazwisko = request.POST.get("nazwisko")
        klient.plec = request.POST.get("plec")

        if not (klient.imie and klient.nazwisko and klient.plec):
            error = "Wszystkie pola są wymagane."
            return render(
                request,
                "portal_nieruchomosci/klient/update.html",
                {"klient": klient, "error": error}
            )

        klient.save()
        return redirect("klient-detail-html", id=klient.id)
