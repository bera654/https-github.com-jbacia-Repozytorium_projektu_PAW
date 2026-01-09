"""
URL configuration for projekt_nieruchomosci project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    #klient
    path("klienci/", views.klient_list, name="klient-list"),
    path("klienci/<int:pk>/", views.klient_detail, name="klient-detail"),
    path("klienci/search/", views.klient_search, name="klient-search"),

    #agent
    path("agenci/", views.agent_list, name="agent-list"),
    path("agenci/<int:pk>/", views.agent_detail, name="agent-detail"),
    path("html/agents/", views.agent_list_html, name="agent-list-html"),
    path("html/agents/<int:id>/", views.agent_detail_html, name="agent-detail-html"),
    path("html/agents/<int:id>/edytuj/",views.agent_update_html,name="agent-update-html"),


    #properties 
    path("html/properties/", views.property_list_html, name="property-list-html"),
    path("html/properties/<int:id>/", views.property_detail_html, name="property-detail-html"),
    path("html/properties/<int:id>/edytuj/",views.property_update_html,name="property-update-html"),



    
    #klient html
    path("html/klienci/", views.klient_list_html, name="klient-list-html"),
    path("html/klienci/dodaj/", views.klient_create_html, name="klient-create-html"),
    path("html/klienci/search/", views.klient_search_html, name="klient-search-html"),
    path("html/klienci/<int:id>/", views.klient_detail_html, name="klient-detail-html"),
    path("html/klienci/<int:id>/edytuj/",views.klient_update_html,name="klient-update-html"),

    



]
