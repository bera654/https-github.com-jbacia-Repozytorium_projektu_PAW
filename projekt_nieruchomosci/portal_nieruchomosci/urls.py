from django.urls import path
from . import views

urlpatterns = [
    # =========================
    # KLIENT API (LAB 9 - rozbite)
    # =========================
    path("klienci/", views.klient_list, name="klient-list"),
    path("klienci/search/", views.klient_search, name="klient-search"),

    # GET detail (AllowAny / public)
    path("klienci/<int:pk>/", views.klient_detail_get, name="klient-detail"),

    # PUT update (Session/Basic + IsAuthenticated)
    path("klienci/update/<int:pk>/", views.klient_update, name="klient-update"),

    # DELETE (Token only + IsAuthenticated)
    path("klienci/delete/<int:pk>/", views.klient_delete, name="klient-delete"),


    # =========================
    # AGENT API
    # =========================
    path("agenci/", views.agent_list, name="agent-list"),
    path("agenci/<int:pk>/", views.agent_detail, name="agent-detail"),


    # =========================
    # PROPERTY TYPE API
    # =========================
    path("property-types/", views.propertytype_list, name="propertytype-list"),
    path("property-types/search/", views.propertytype_search, name="propertytype-search"),
    path("property-types/<int:pk>/", views.propertytype_detail, name="propertytype-detail"),

    # Zadanie 5 / “members” analog: properties należące do typu
    path(
        "property-types/<int:pk>/properties/",
        views.propertytype_properties,
        name="propertytype-properties",
    ),


    # =========================
    # PROPERTY API
    # =========================
    path("properties/", views.property_list, name="property-list"),
    path("properties/search/", views.property_search, name="property-search"),
    path("properties/<int:pk>/", views.property_detail, name="property-detail"),


    # =========================
    # HTML - AGENT
    # =========================
    path("html/agents/", views.agent_list_html, name="agent-list-html"),
    path("html/agents/dodaj/", views.agent_create_html, name="agent-create-html"),
    path("html/agents/<int:id>/", views.agent_detail_html, name="agent-detail-html"),
    path("html/agents/<int:id>/edytuj/", views.agent_update_html, name="agent-update-html"),


    # =========================
    # HTML - PROPERTY
    # =========================
    path("html/properties/", views.property_list_html, name="property-list-html"),
    path("html/properties/dodaj/", views.property_create_html, name="property-create-html"),
    path("html/properties/<int:id>/", views.property_detail_html, name="property-detail-html"),
    path("html/properties/<int:id>/edytuj/", views.property_update_html, name="property-update-html"),


    # =========================
    # HTML - KLIENT
    # =========================
    path("html/klienci/", views.klient_list_html, name="klient-list-html"),
    path("html/klienci/dodaj/", views.klient_create_html, name="klient-create-html"),
    path("html/klienci/search/", views.klient_search_html, name="klient-search-html"),
    path("html/klienci/<int:id>/", views.klient_detail_html, name="klient-detail-html"),
    path("html/klienci/<int:id>/edytuj/", views.klient_update_html, name="klient-update-html"),


    # =========================
    # HTML - PROPERTY TYPE
    # =========================
    path("html/property-types/", views.propertytype_list_html, name="propertytype-list-html"),
    path("html/property-types/dodaj/", views.propertytype_create_html, name="propertytype-create-html"),
    path("html/property-types/<int:id>/", views.propertytype_detail_html, name="propertytype-detail-html"),
    path("html/property-types/<int:id>/edytuj/", views.propertytype_update_html, name="propertytype-update-html"),
]
