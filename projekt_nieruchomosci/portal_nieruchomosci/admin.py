from django.contrib import admin
from .models import PropertyType, Agent, Property, Klient


# Register your models here.
admin.site.register(PropertyType)
admin.site.register(Agent)
admin.site.register(Property)
admin.site.register(Klient)