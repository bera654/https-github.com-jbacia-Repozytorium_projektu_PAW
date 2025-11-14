from django.contrib import admin
from .models import PropertyType, Agent, Property, Klient

class AgentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'stanowisko', 'region']
    list_filter = ['stanowisko', 'region']
    search_fields = ['first_name', 'last_name','stanowisko', 'region']

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_residential', 'popularity_rank']
    list_filter = ['is_residential', 'popularity_rank', 'typical_features']
    search_fields = ['name', 'description', 'typical_features']


class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'transaction_type', 'agent', 'property_type',
        'price', 'square_meters', 'location'
    ]
    list_filter = [
        'transaction_type', 'property_type', 'listing_month',
        'pool', 'sauna', 'jacuzzi','lift', 'garage','balcony','terrace','AC','safety_system','needs_renovation', 'garden', 'price', 'square_meters', 'location' 
    ]
    search_fields = [
        'title', 'location', 'description','property_type'
    ]


class KlientAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'plec', 'data_dodania']
    list_filter = ['plec']
    search_fields = ['imie', 'nazwisko']


# REGISTER MODELS
admin.site.register(Agent, AgentAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Klient, KlientAdmin)