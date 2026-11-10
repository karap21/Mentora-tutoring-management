from django.urls import path
from . import views

urlpatterns = [
    path("keranjang/", views.keranjang_view, name="keranjang"),
    path("bayar/", views.bayar_view, name="bayar"),
]
