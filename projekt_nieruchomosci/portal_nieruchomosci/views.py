from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Klient, Agent, PropertyType, Property
from .serializers import KlientSerializer, AgentSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, redirect
from .serializers import KlientSerializer, AgentSerializer, PropertyTypeSerializer, PropertySerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def klient_list(request):

    if request.method == "GET":
        klienci = Klient.objects.filter(wlasciciel=request.user)
        serializer = KlientSerializer(klienci, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = KlientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=request.user)  # <-- klucz
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([AllowAny])
def klient_detail_get(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    serializer = KlientSerializer(klient)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def klient_update(request, pk):
    klient = get_object_or_404(Klient, pk=pk, wlasciciel=request.user)
    serializer = KlientSerializer(klient, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def klient_delete(request, pk):
    klient = get_object_or_404(Klient, pk=pk, wlasciciel=request.user)
    klient.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def klient_search(request):
    query = request.GET.get("q", "")
    klienci = Klient.objects.filter(
        wlasciciel=request.user,
        nazwisko__icontains=query
    )
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


@api_view(["GET", "POST"])
def propertytype_list(request):
    if request.method == "GET":
        types = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PropertyTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def propertytype_detail(request, pk):
    pt = get_object_or_404(PropertyType, pk=pk)

    if request.method == "GET":
        serializer = PropertyTypeSerializer(pt)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = PropertyTypeSerializer(pt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        pt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def propertytype_search(request):
    query = request.GET.get("q", "")
    types = PropertyType.objects.filter(name__icontains=query)
    serializer = PropertyTypeSerializer(types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def property_list(request):
    if request.method == "GET":
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == "GET":
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = PropertySerializer(property_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        property_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def property_search(request):
    q = request.GET.get("q", "")
    properties = Property.objects.filter(title__icontains=q)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



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



def propertytype_list_html(request):
    types = PropertyType.objects.all()
    return render(
        request,
        "portal_nieruchomosci/propertytype/list.html",
        {"types": types}
    )


def propertytype_create_html(request):
    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/propertytype/create.html",
            {}
        )

    elif request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        typical_features = request.POST.get("typical_features", "")
        is_residential = bool(request.POST.get("is_residential"))
        popularity_rank = request.POST.get("popularity_rank")

       
        if not name:
            error = "Nazwa typu nieruchomości jest wymagana."
            return render(
                request,
                "portal_nieruchomosci/propertytype/create.html",
                {"error": error}
            )

        
        try:
            popularity_rank = int(popularity_rank) if popularity_rank not in (None, "") else 0
        except ValueError:
            popularity_rank = 0

        PropertyType.objects.create(
            name=name,
            description=description,
            typical_features=typical_features,
            is_residential=is_residential,
            popularity_rank=popularity_rank
        )

        return redirect("propertytype-list-html")


def propertytype_detail_html(request, id):
    pt = get_object_or_404(PropertyType, id=id)

    if request.method == "POST":
        pt.delete()
        return redirect("propertytype-list-html")

    return render(
        request,
        "portal_nieruchomosci/propertytype/detail.html",
        {"type": pt}
    )


def propertytype_update_html(request, id):
    pt = get_object_or_404(PropertyType, id=id)

    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/propertytype/update.html",
            {"type": pt}
        )

    elif request.method == "POST":
        pt.name = request.POST.get("name")
        pt.description = request.POST.get("description", "")
        pt.typical_features = request.POST.get("typical_features", "")
        pt.is_residential = bool(request.POST.get("is_residential"))

        popularity_rank = request.POST.get("popularity_rank")
        try:
            pt.popularity_rank = int(popularity_rank) if popularity_rank not in (None, "") else 0
        except ValueError:
            pt.popularity_rank = 0

        if not pt.name:
            error = "Nazwa typu nieruchomości jest wymagana."
            return render(
                request,
                "portal_nieruchomosci/propertytype/update.html",
                {"type": pt, "error": error}
            )

        pt.save()
        return redirect("propertytype-detail-html", id=pt.id)


def agent_create_html(request):
    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/agent/create.html",
            {}
        )

    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        region = request.POST.get("region")
        stanowisko = request.POST.get("stanowisko")

        if not (first_name and last_name and region and stanowisko):
            error = "Wszystkie pola są wymagane."
            return render(
                request,
                "portal_nieruchomosci/agent/create.html",
                {"error": error}
            )

        Agent.objects.create(
            first_name=first_name,
            last_name=last_name,
            region=region,
            stanowisko=stanowisko
        )
        return redirect("agent-list-html")



def property_create_html(request):
    agents = Agent.objects.all()
    types = PropertyType.objects.all()

    if request.method == "GET":
        return render(
            request,
            "portal_nieruchomosci/property/create.html",
            {"agents": agents, "types": types}
        )

    elif request.method == "POST":
        title = request.POST.get("title")
        location = request.POST.get("location")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        square_meters = request.POST.get("square_meters")

        agent_id = request.POST.get("agent")
        type_id = request.POST.get("property_type")

        
        pool = bool(request.POST.get("pool"))
        sauna = bool(request.POST.get("sauna"))
        jacuzzi = bool(request.POST.get("jacuzzi"))
        lift = bool(request.POST.get("lift"))
        garage = bool(request.POST.get("garage"))
        balcony = bool(request.POST.get("balcony"))
        terrace = bool(request.POST.get("terrace"))
        garden = bool(request.POST.get("garden"))
        AC = bool(request.POST.get("AC"))
        safety_system = bool(request.POST.get("safety_system"))
        needs_renovation = bool(request.POST.get("needs_renovation"))

        
        if not (title and location and price and square_meters):
            error = "Tytuł, lokalizacja, cena i metraż są wymagane."
            return render(
                request,
                "portal_nieruchomosci/property/create.html",
                {"error": error, "agents": agents, "types": types}
            )

        
        agent_obj = Agent.objects.filter(id=agent_id).first() if agent_id else None
        type_obj = PropertyType.objects.filter(id=type_id).first() if type_id else None

        Property.objects.create(
            title=title,
            location=location,
            description=description,
            price=price,
            square_meters=square_meters,
            agent=agent_obj,
            property_type=type_obj,

            pool=pool,
            sauna=sauna,
            jacuzzi=jacuzzi,
            lift=lift,
            garage=garage,
            balcony=balcony,
            terrace=terrace,
            garden=garden,
            AC=AC,
            safety_system=safety_system,
            needs_renovation=needs_renovation,
        )

        return redirect("property-list-html")
