from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Klient, Agent, PropertyType, Property
from .serializers import (
    KlientSerializer,
    AgentSerializer,
    PropertyTypeSerializer,
    PropertySerializer,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q 
from django.http import HttpResponseForbidden 
from django.contrib.auth.models import Group, User


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def klient_list(request):
    if request.method == "GET":
        klienci = Klient.objects.filter(user=request.user)
        serializer = KlientSerializer(klienci, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = KlientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
    klient = get_object_or_404(Klient, pk=pk, user=request.user)
    serializer = KlientSerializer(klient, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def klient_delete(request, pk):
    klient = get_object_or_404(Klient, pk=pk, user=request.user)
    klient.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def klient_search(request):
    query = request.GET.get("q", "")
    klienci = Klient.objects.filter(
        user=request.user,
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
    agent = get_object_or_404(Agent, pk=pk)
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

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def propertytype_properties(request, pk):
    pt = get_object_or_404(PropertyType, pk=pk)
    props = Property.objects.filter(property_type=pt)
    serializer = PropertySerializer(props, many=True)
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




def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('property-list-html')
            elif hasattr(user, 'agent_profile'):
                return redirect('agent-my-offers') 
            else:
                return redirect('property-list-html') 
        else:
            return render(request, 'portal_nieruchomosci/login.html', {'error': 'Nieprawidłowe dane'})
            
    return render(request, 'portal_nieruchomosci/login.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        role = request.POST.get('role')
        
        
        imie = request.POST.get('imie')
        nazwisko = request.POST.get('nazwisko')

        if pass1 != pass2:
            return render(request, 'portal_nieruchomosci/signup.html', {'error': 'Hasła muszą być takie same!'})
        
        if not (imie and nazwisko):
             return render(request, 'portal_nieruchomosci/signup.html', {'error': 'Imię i nazwisko są wymagane!'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'portal_nieruchomosci/signup.html', {'error': 'Taki login jest już zajęty!'})

        
        user = User.objects.create_user(username=username, password=pass1)
        
        
        if role == 'agent':
            group, _ = Group.objects.get_or_create(name='Agenci')
            user.groups.add(group)
            Agent.objects.create(
                user=user, 
                first_name=imie, 
                last_name=nazwisko,
                region="PL", 
                stanowisko="A"
            )
        elif role == 'client':
            group, _ = Group.objects.get_or_create(name='Klienci')
            user.groups.add(group)
            Klient.objects.create(
                user=user,
                imie=imie,
                nazwisko=nazwisko,
                plec="I"
            )

        user.save()
        return redirect('user-login')

    return render(request, 'portal_nieruchomosci/signup.html')




@login_required(login_url='user-login')
def agent_my_offers(request):
    if not hasattr(request.user, 'agent_profile'):
        return render(request, "portal_nieruchomosci/login.html", {"error": "Brak uprawnień agenta!"})
        
    agent = request.user.agent_profile
    properties = Property.objects.filter(agent=agent)
    
    return render(request, "portal_nieruchomosci/agent/my_offers.html", {"properties": properties})

@login_required(login_url='user-login')
def agent_my_clients(request):
    if not hasattr(request.user, 'agent_profile'):
        return redirect('property-list-html')

    agent = request.user.agent_profile
    
    
    moj_klienci = Klient.objects.filter(opiekun=agent)
    
    
    wolni_klienci = Klient.objects.filter(opiekun__isnull=True)
    
    return render(request, "portal_nieruchomosci/agent/my_clients.html", {
        "moj_klienci": moj_klienci,
        "wolni_klienci": wolni_klienci
    })

@login_required(login_url='user-login')
def przypisz_klienta(request, id):
    if request.method == "POST" and hasattr(request.user, 'agent_profile'):
        klient = get_object_or_404(Klient, id=id)
        if klient.opiekun is None:
            klient.opiekun = request.user.agent_profile
            klient.save()
    return redirect('agent-my-clients')




def property_list_html(request):
    properties = Property.objects.all()
    return render(request, "portal_nieruchomosci/property/list.html", {"properties": properties})


def property_detail_html(request, id):
    property_obj = get_object_or_404(Property, id=id)
    
    if request.method == "POST":
        is_owner_agent = hasattr(request.user, 'agent_profile') and property_obj.agent == request.user.agent_profile
        
        if request.user.is_superuser or is_owner_agent:
            property_obj.delete()
            if is_owner_agent:
                return redirect("agent-my-offers")
            return redirect("property-list-html")
        else:
             return render(request, "portal_nieruchomosci/login.html", {"error": "Brak uprawnień do usunięcia!"})
        
    return render(request, "portal_nieruchomosci/property/detail.html", {"property": property_obj})


@login_required(login_url='user-login')
def property_create_html(request):
    is_agent = hasattr(request.user, 'agent_profile')
    if not (request.user.is_superuser or is_agent):
        return render(request, "portal_nieruchomosci/login.html", {"error": "Tylko agenci mogą dodawać oferty."})

    agents = Agent.objects.all()
    types = PropertyType.objects.all()

    if request.method == "GET":
        return render(request, "portal_nieruchomosci/property/create.html", {"agents": agents, "types": types})

    elif request.method == "POST":
        title = request.POST.get("title")
        location = request.POST.get("location")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        square_meters = request.POST.get("square_meters")

        
        if is_agent:
            agent_obj = request.user.agent_profile
        else:
            agent_id = request.POST.get("agent")
            agent_obj = Agent.objects.filter(id=agent_id).first() if agent_id else None

        type_id = request.POST.get("property_type")
        type_obj = PropertyType.objects.filter(id=type_id).first() if type_id else None

        
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
            return render(request, "portal_nieruchomosci/property/create.html", {"error": error, "agents": agents, "types": types})

        Property.objects.create(
            title=title, location=location, description=description, price=price, square_meters=square_meters,
            agent=agent_obj, property_type=type_obj,
            pool=pool, sauna=sauna, jacuzzi=jacuzzi, lift=lift, garage=garage,
            balcony=balcony, terrace=terrace, garden=garden, AC=AC,
            safety_system=safety_system, needs_renovation=needs_renovation,
        )
        
        if is_agent:
            return redirect("agent-my-offers")
        return redirect("property-list-html")

@login_required(login_url='user-login')
def property_update_html(request, id):
    property_obj = get_object_or_404(Property, id=id)

    
    is_owner_agent = hasattr(request.user, 'agent_profile') and property_obj.agent == request.user.agent_profile
    if not (request.user.is_superuser or is_owner_agent):
        return render(request, "portal_nieruchomosci/login.html", {"error": "Nie możesz edytować tej oferty."})

    if request.method == "GET":
        return render(request, "portal_nieruchomosci/property/update.html", {"property": property_obj})

    elif request.method == "POST":
        property_obj.title = request.POST.get("title")
        property_obj.location = request.POST.get("location")
        property_obj.description = request.POST.get("description")
        property_obj.price = request.POST.get("price")
        property_obj.square_meters = request.POST.get("square_meters")

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

        if not (property_obj.title and property_obj.location and property_obj.price and property_obj.square_meters):
            error = "Pola wymagane nie mogą być puste."
            return render(request, "portal_nieruchomosci/property/update.html", {"property": property_obj, "error": error})

        property_obj.save()
        return redirect("property-detail-html", id=property_obj.id)




def agent_list_html(request):
    agents = Agent.objects.all()
    return render(request, "portal_nieruchomosci/agent/list.html", {"agents": agents})


def agent_detail_html(request, id):
    agent = get_object_or_404(Agent, id=id)
    if request.method == "POST":
        if not request.user.is_superuser:
            return render(request, "portal_nieruchomosci/login.html", {"error": "Brak uprawnień!"})
        agent.delete()
        return redirect("agent-list-html")
    return render(request, "portal_nieruchomosci/agent/detail.html", {"agent": agent})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def agent_update_html(request, id):
    agent = get_object_or_404(Agent, id=id)
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/agent/update.html", {"agent": agent})
    elif request.method == "POST":
        agent.first_name = request.POST.get("first_name")
        agent.last_name = request.POST.get("last_name")
        agent.region = request.POST.get("region")
        agent.stanowisko = request.POST.get("stanowisko")
        if not (agent.first_name and agent.last_name and agent.stanowisko):
            error = "Dane wymagane."
            return render(request, "portal_nieruchomosci/agent/update.html", {"agent": agent, "error": error})
        agent.save()
        return redirect("agent-detail-html", id=agent.id)

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def agent_create_html(request):
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/agent/create.html", {})
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        region = request.POST.get("region")
        stanowisko = request.POST.get("stanowisko")
        Agent.objects.create(first_name=first_name, last_name=last_name, region=region, stanowisko=stanowisko)
        return redirect("agent-list-html")




@login_required(login_url='user-login')
@permission_required('portal_nieruchomosci.view_klient', raise_exception=True)
def klient_list_html(request):
    klienci = Klient.objects.all()
    return render(request, "portal_nieruchomosci/klient/list.html", {"klienci": klienci})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def klient_create_html(request):
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/klient/create.html", {})
    elif request.method == "POST":
        imie = request.POST.get("imie")
        nazwisko = request.POST.get("nazwisko")
        plec = request.POST.get("plec")
        if not (imie and nazwisko and plec):
            return render(request, "portal_nieruchomosci/klient/create.html", {"error": "Błąd danych"})
        Klient.objects.create(imie=imie, nazwisko=nazwisko, plec=plec)
        return redirect("klient-list-html")

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def klient_search_html(request):
    query = request.GET.get("q", "")
    if query:
        klienci = Klient.objects.filter(nazwisko__icontains=query)
    else:
        klienci = Klient.objects.none()
    return render(request, "portal_nieruchomosci/klient/search.html", {"klienci": klienci, "query": query})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def klient_detail_html(request, id):
    klient = get_object_or_404(Klient, id=id)
    if request.method == "POST":
        klient.delete()
        return redirect("klient-list-html")
    return render(request, "portal_nieruchomosci/klient/detail.html", {"klient": klient})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def klient_update_html(request, id):
    klient = get_object_or_404(Klient, id=id)
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/klient/update.html", {"klient": klient})
    elif request.method == "POST":
        klient.imie = request.POST.get("imie")
        klient.nazwisko = request.POST.get("nazwisko")
        klient.plec = request.POST.get("plec")
        klient.save()
        return redirect("klient-detail-html", id=klient.id)




def propertytype_list_html(request):
    types = PropertyType.objects.all()
    return render(request, "portal_nieruchomosci/propertytype/list.html", {"types": types})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def propertytype_create_html(request):
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/propertytype/create.html", {})
    elif request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        typical_features = request.POST.get("typical_features", "")
        is_residential = bool(request.POST.get("is_residential"))
        popularity_rank = request.POST.get("popularity_rank")
        try:
            popularity_rank = int(popularity_rank) if popularity_rank else 0
        except ValueError:
            popularity_rank = 0

        PropertyType.objects.create(name=name, description=description, typical_features=typical_features, is_residential=is_residential, popularity_rank=popularity_rank)
        return redirect("propertytype-list-html")

def propertytype_detail_html(request, id):
    pt = get_object_or_404(PropertyType, id=id)
    if request.method == "POST":
        if not request.user.is_superuser:
             return render(request, "portal_nieruchomosci/login.html", {"error": "Brak uprawnień"})
        pt.delete()
        return redirect("propertytype-list-html")
    return render(request, "portal_nieruchomosci/propertytype/detail.html", {"type": pt})

@user_passes_test(lambda u: u.is_superuser, login_url='user-login')
def propertytype_update_html(request, id):
    pt = get_object_or_404(PropertyType, id=id)
    if request.method == "GET":
        return render(request, "portal_nieruchomosci/propertytype/update.html", {"type": pt})
    elif request.method == "POST":
        pt.name = request.POST.get("name")
        pt.description = request.POST.get("description", "")
        pt.typical_features = request.POST.get("typical_features", "")
        pt.is_residential = bool(request.POST.get("is_residential"))
        popularity_rank = request.POST.get("popularity_rank")
        try:
            pt.popularity_rank = int(popularity_rank) if popularity_rank else 0
        except ValueError:
            pt.popularity_rank = 0
        pt.save()
        return redirect("propertytype-detail-html", id=pt.id)