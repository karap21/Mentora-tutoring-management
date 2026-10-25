from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .decorators import peran_wajib
from .models import Pengguna


def beranda_view(request):
    """Halaman beranda publik (/)."""
    return render(request, "beranda.html")


def syarat_ketentuan_view(request):
    """Halaman Syarat dan Ketentuan (/syarat-ketentuan/)."""
    return render(request, "syarat_ketentuan.html")


def masuk_view(request):
    """
    Realisasi UC-02: Login untuk Siswa, Guru, dan Admin.
    Mencocokkan email & hash bcrypt di tabel akun_pengguna, membuat sesi,
    dan mengarahkan pengguna ke dasbor sesuai peran.
    """
    if request.user.is_authenticated:
        return _arahkan_sesuai_peran(request.user)

    form = LoginForm(request.POST or None)
    pesan_galat = None

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]

        # Cek apakah akun ada tetapi dinonaktifkan admin (Alur Alternatif UC-02)
        pengguna_db = Pengguna.objects.filter(email__iexact=email).first()
        if pengguna_db and not pengguna_db.is_active:
            pesan_galat = "Akun Anda telah dinonaktifkan oleh Admin."
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return _arahkan_sesuai_peran(user)
            else:
                # Pesan umum tanpa menyebut mana yang salah (Alur Alternatif UC-02)
                pesan_galat = "Email atau kata sandi salah"

    return render(request, "akun/masuk.html", {"form": form, "pesan_galat": pesan_galat})


def keluar_view(request):
    """Realisasi UC-02: Logout pengguna dan hapus sesi."""
    logout(request)
    messages.info(request, "Anda telah berhasil keluar dari sesi.")
    return redirect("masuk")


def _arahkan_sesuai_peran(user: Pengguna):
    """Helper protected untuk mengarahkan pengguna ke dasbor sesuai perannya."""
    if user.adalah_admin():
        return redirect("kelola_guru")
    elif user.adalah_guru():
        return redirect("dasbor_guru")
    return redirect("dasbor_siswa")


@peran_wajib("siswa")
def dasbor_siswa_view(request):
    """Halaman Dasbor Siswa (/siswa/)."""
    rekomendasi_terbaru = request.user.rekomendasi.select_related("mapel").order_by("-dibuat_pada").first()
    langganan_aktif = request.user.langganan.select_related("paket").all()
    notifikasi_list = request.user.notifikasi.order_by("-dibuat_pada")[:5]
    return render(
        request,
        "pembelajaran/dasbor_siswa.html",
        {
            "rekomendasi": rekomendasi_terbaru,
            "langganan_list": langganan_aktif,
            "notifikasi_list": notifikasi_list,
        },
    )


@peran_wajib("guru")
def dasbor_guru_view(request):
    """Halaman Dasbor Guru (/guru/)."""
    mapel_diampu = request.user.mapel_diampu.select_related("mapel").all()
    return render(request, "guru/dasbor_guru.html", {"mapel_diampu": mapel_diampu})


@peran_wajib("admin")
def kelola_guru_view(request):
    """Halaman Admin Kelola Guru (/admin-panel/guru/)."""
    daftar_guru = Pengguna.objects.filter(peran="guru").prefetch_related("mapel_diampu__mapel")
    return render(request, "admin_panel/kelola_guru.html", {"daftar_guru": daftar_guru})


# --- Kerangka / Stub View Lainnya ---
def daftar_view(request):
    """Stub UC-01: Registrasi akun siswa."""
    pass


@peran_wajib("siswa")
def profil_view(request):
    """Stub Profil siswa."""
    pass