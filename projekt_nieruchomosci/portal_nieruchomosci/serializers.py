from rest_framework import serializers
from .models import (
    PropertyType,
    Agent,
    Property,
    Klient,
    MONTHS,
    TRANSACTION_TYPES,
)

from .models import PropertyType

class PropertyTypeSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True, max_length=50)
    description = serializers.CharField(allow_blank=True, required=False)
    typical_features = serializers.CharField(allow_blank=True, required=False, max_length=200)
    is_residential = serializers.BooleanField(default=True)
    popularity_rank = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return PropertyType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.typical_features = validated_data.get("typical_features", instance.typical_features)
        instance.is_residential = validated_data.get("is_residential", instance.is_residential)
        instance.popularity_rank = validated_data.get("popularity_rank", instance.popularity_rank)
        instance.save()
        return instance


class AgentSerializer(serializers.Serializer):
    """Serializer dla modelu Agent."""

    id = serializers.IntegerField(read_only=True)

    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)

    
    stanowisko = serializers.ChoiceField(
        choices=Agent.Stanowisko,
        default=Agent.Stanowisko[0][0]  
    )

    region = serializers.CharField(required=True, max_length=2)

    def create(self, validated_data):
        return Agent.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.stanowisko = validated_data.get("stanowisko", instance.stanowisko)
        instance.region = validated_data.get("region", instance.region)
        instance.save()
        return instance


class PropertySerializer(serializers.Serializer):
    """Serializer dla modelu Property."""

    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(required=True, max_length=100)

  
    listing_month = serializers.ChoiceField(
        choices=MONTHS.choices,
        default=MONTHS.choices[0][0]  
    )

   
    transaction_type = serializers.ChoiceField(
        choices=TRANSACTION_TYPES,
        default=TRANSACTION_TYPES[0][0]  
    )

    
    agent = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(),
        allow_null=True,
        required=False
    )
    property_type = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all(),
        allow_null=True,
        required=False
    )

    available_units = serializers.IntegerField(default=1)
    square_meters = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        allow_null=True,
        required=False
    )

    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        allow_null=True,
        required=False
    )

    location = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False
    )

    description = serializers.CharField(
        allow_blank=True,
        required=False
    )

    
    pool = serializers.BooleanField(default=True)
    sauna = serializers.BooleanField(default=True)
    jacuzzi = serializers.BooleanField(default=True)
    lift = serializers.BooleanField(default=True)
    garage = serializers.BooleanField(default=True)
    balcony = serializers.BooleanField(default=True)
    terrace = serializers.BooleanField(default=True)
    garden = serializers.BooleanField(default=True)
    AC = serializers.BooleanField(default=True)
    safety_system = serializers.BooleanField(default=True)
    needs_renovation = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.listing_month = validated_data.get("listing_month", instance.listing_month)
        instance.transaction_type = validated_data.get("transaction_type", instance.transaction_type)
        instance.agent = validated_data.get("agent", instance.agent)
        instance.property_type = validated_data.get("property_type", instance.property_type)
        instance.available_units = validated_data.get("available_units", instance.available_units)
        instance.square_meters = validated_data.get("square_meters", instance.square_meters)
        instance.price = validated_data.get("price", instance.price)
        instance.location = validated_data.get("location", instance.location)
        instance.description = validated_data.get("description", instance.description)
        instance.pool = validated_data.get("pool", instance.pool)
        instance.sauna = validated_data.get("sauna", instance.sauna)
        instance.jacuzzi = validated_data.get("jacuzzi", instance.jacuzzi)
        instance.lift = validated_data.get("lift", instance.lift)
        instance.garage = validated_data.get("garage", instance.garage)
        instance.balcony = validated_data.get("balcony", instance.balcony)
        instance.terrace = validated_data.get("terrace", instance.terrace)
        instance.garden = validated_data.get("garden", instance.garden)
        instance.AC = validated_data.get("AC", instance.AC)
        instance.safety_system = validated_data.get("safety_system", instance.safety_system)
        instance.needs_renovation = validated_data.get("needs_renovation", instance.needs_renovation)
        instance.save()
        return instance


class KlientSerializer(serializers.Serializer):
    """Serializer dla modelu Klient."""

    id = serializers.IntegerField(read_only=True)

    imie = serializers.CharField(required=True, max_length=50)
    nazwisko = serializers.CharField(required=True, max_length=100)

    plec = serializers.ChoiceField(
        choices=Klient.PLEC_WYBOR,
        default=Klient.PLEC_WYBOR[2][0]  
    )

   
    data_dodania = serializers.DateField(read_only=True)
    wlasciciel = serializers.ReadOnlyField(source="wlasciciel.username")

    def create(self, validated_data):
        return Klient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.imie = validated_data.get("imie", instance.imie)
        instance.nazwisko = validated_data.get("nazwisko", instance.nazwisko)
        instance.plec = validated_data.get("plec", instance.plec)
        instance.save()
        return instance
    
    


