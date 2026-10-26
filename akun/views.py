from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .decorators import peran_wajib
from .models import Pengguna


def beranda_view(request):
    """Halaman beranda publik (/)."""
    from django.conf import settings
    from pembelajaran.models import Mapel, Modul, Kuis, Achievement
    from langganan.models import Paket

    try:
        daftar_mapel = list(Mapel.objects.all().order_by("kode")[:12])
        daftar_paket = list(
            Paket.objects.filter(aktif=True)
            .prefetch_related("paket_mapel__mapel")
            .order_by("jenis", "-harga_per_bulan", "kode")[:12]
        )
        daftar_achievement = list(Achievement.objects.all().order_by("kode")[:4])
        total_mapel = Mapel.objects.count()
        total_modul = Modul.objects.count()
        total_kuis = Kuis.objects.count()
    except Exception:
        daftar_mapel = []
        daftar_paket = []
        daftar_achievement = []
        total_mapel = 0
        total_modul = 0
        total_kuis = 0

    context = {
        "daftar_mapel": daftar_mapel,
        "daftar_paket": daftar_paket,
        "daftar_achievement": daftar_achievement,
        "total_mapel": total_mapel,
        "total_modul": total_modul,
        "total_kuis": total_kuis,
        "ambang_pretest": getattr(settings, "AMBANG_PRETEST", 85),
        "ambang_kuis_dasar": getattr(settings, "AMBANG_KUIS_DASAR", 75),
        "durasi_min": getattr(settings, "DURASI_MIN", 1),
        "durasi_max": getattr(settings, "DURASI_MAX", 12),
        "durasi_diskon": getattr(settings, "DURASI_DISKON", 12),
        "persen_diskon": getattr(settings, "PERSEN_DISKON", 20),
        "masa_berlaku_token_jam": getattr(settings, "MASA_BERLAKU_TOKEN_JAM", 72),
        "interval_laporan_hari": getattr(settings, "INTERVAL_LAPORAN_HARI", 14),
    }
    return render(request, "beranda.html", context)


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
