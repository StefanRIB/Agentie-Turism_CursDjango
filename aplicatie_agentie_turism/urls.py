from django.urls import path, re_path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
    path("info/", views.info, name="info"),
    path("log/", views.log_accesari, name="log_accesari"),
    path("istoric/", views.istoric_site, name="istoric_site"),
    path("despre/", views.despre, name="despre"),
    re_path(r'^accesare(?P<id>\d+)$', views.detalii_accesare, name="detalii_accesare"),
    path("servicii_turism", views.servicii_turism, name="servicii_turism"),
    path("contact/", views.in_lucru, name="contact"),
    path("cos_virtual/", views.in_lucru, name="cos_virtual"),
    path('produse/', views.lista_produse, name='lista_produse'),
    path('produs/<int:pk>/', views.detalii_produs, name='detalii_produs'),
    path('categorii/<str:nume_categorie>/', views.lista_produse, name='produse_categorie'),
]
