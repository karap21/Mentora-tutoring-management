from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from akun import views as akun_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", akun_views.beranda_view, name="beranda"),
    path("syarat-ketentuan/", akun_views.syarat_ketentuan_view, name="syarat_ketentuan"),
    path("akun/", include("akun.urls")),
    path("siswa/", akun_views.dasbor_siswa_view, name="dasbor_siswa"),
    path("guru/", akun_views.dasbor_guru_view, name="dasbor_guru"),
    path("admin-panel/guru/", akun_views.kelola_guru_view, name="kelola_guru"),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)