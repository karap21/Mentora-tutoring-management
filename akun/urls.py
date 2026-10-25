from django.urls import path
from . import views

urlpatterns = [
    path("masuk/", views.masuk_view, name="masuk"),
    path("keluar/", views.keluar_view, name="keluar"),
    path("daftar/", views.daftar_view, name="daftar"),
    path("profil/", views.profil_view, name="profil"),
]