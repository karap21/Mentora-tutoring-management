from django.test import TestCase, Client
from django.urls import reverse
from akun.models import Pengguna


class LandingPageDanAutentikasiTest(TestCase):
    """Pengujian Unit & Integrasi Halaman Beranda dan Autentikasi Mentora-LMS."""

    def setUp(self):
        self.client = Client()
        self.siswa = Pengguna.objects.create_user(
            email="siswa.test@mentora.id",
            nama="Siswa Uji",
            password="Mentora123!",
            peran="siswa",
        )
        self.guru = Pengguna.objects.create_user(
            email="guru.test@mentora.id",
            nama="Guru Uji",
            password="Mentora123!",
            peran="guru",
        )
        self.admin_user = Pengguna.objects.create_superuser(
            email="admin.test@mentora.id",
            nama="Admin Uji",
            password="Mentora123!",
        )

    def test_halaman_beranda_200_dan_template_benar(self):
        """Memastikan rute publik '/' mengembalikan status 200, elemen wajib DPPL Bab 5.1, SKPL BR-01, & Motion."""
        response = self.client.get(reverse("beranda"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "beranda.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Mentora-LMS")
        self.assertContains(response, "Simulasi Mesin Adaptif Mentora")
        # DPPL Bab 5.1: Penjelasan singkat, daftar paket, tombol Daftar dan Masuk
        self.assertContains(response, reverse("daftar"))
        self.assertContains(response, reverse("masuk"))
        self.assertContains(response, "BDL-SAINS")
        self.assertContains(response, "BDL-BHS")
        self.assertContains(response, "BDL-FULL")
        # Motion scroll-reveal & stagger attributes
        self.assertContains(response, "data-motion-reveal")
        self.assertContains(response, "data-motion-stagger")

    def test_halaman_syarat_ketentuan_200(self):
        """Memastikan rute '/syarat-ketentuan/' mengembalikan status 200 dan me-render syarat_ketentuan.html."""
        response = self.client.get(reverse("syarat_ketentuan"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "syarat_ketentuan.html")
        self.assertContains(response, "Syarat dan Ketentuan Penggunaan Mentora-LMS")

    def test_login_siswa_berhasil_dan_redirect_ke_dasbor_siswa(self):
        """Memastikan login akun siswa mengarahkan ke /siswa/."""
        response = self.client.post(
            reverse("masuk"),
            {"email": "siswa.test@mentora.id", "password": "Mentora123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dasbor_siswa"))

    def test_login_guru_berhasil_dan_redirect_ke_dasbor_guru(self):
        """Memastikan login akun guru mengarahkan ke /guru/."""
        response = self.client.post(
            reverse("masuk"),
            {"email": "guru.test@mentora.id", "password": "Mentora123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dasbor_guru"))

    def test_login_admin_berhasil_dan_redirect_ke_kelola_guru(self):
        """Memastikan login akun admin mengarahkan ke /admin-panel/guru/."""
        response = self.client.post(
            reverse("masuk"),
            {"email": "admin.test@mentora.id", "password": "Mentora123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("kelola_guru"))

    def test_login_gagal_kata_sandi_salah(self):
        """Memastikan pesan galat muncul bila kata sandi salah (UC-02)."""
        response = self.client.post(
            reverse("masuk"),
            {"email": "siswa.test@mentora.id", "password": "SalahPassword123!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email atau kata sandi salah")

    def test_login_gagal_akun_nonaktif(self):
        """Memastikan akun yang dinonaktifkan ditolak dengan pesan yang sesuai."""
        self.siswa.is_active = False
        self.siswa.save()

        response = self.client.post(
            reverse("masuk"),
            {"email": "siswa.test@mentora.id", "password": "Mentora123!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Akun Anda telah dinonaktifkan oleh Admin.")

    def test_keluar_menghapus_sesi_dan_redirect_ke_login(self):
        """Memastikan /akun/keluar/ mengakhiri sesi dan mengarahkan kembali ke login."""
        self.client.login(username="siswa.test@mentora.id", password="Mentora123!")
        response = self.client.get(reverse("keluar"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("masuk"))
