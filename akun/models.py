from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class PenggunaManager(BaseUserManager):
    """Manager untuk custom user model Pengguna."""

    def create_user(self, email: str, nama: str, password: str = None, **extra_fields):
        if not email:
            raise ValueError("Email wajib diisi")
        email = self.normalize_email(email)
        extra_fields.setdefault("peran", "siswa")
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, nama=nama, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, nama: str, password: str = None, **extra_fields):
        extra_fields.setdefault("peran", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nama, password, **extra_fields)


class Pengguna(AbstractBaseUser):
    """Tabel 1: akun_pengguna (siswa, guru, admin)."""

    PERAN_CHOICES = [
        ("siswa", "Siswa"),
        ("guru", "Guru"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    peran = models.CharField(max_length=50, choices=PERAN_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = PenggunaManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nama"]

    class Meta:
        db_table = "akun_pengguna"
        constraints = [
            models.CheckConstraint(
                check=models.Q(peran__in=["siswa", "guru", "admin"]),
                name="akun_pengguna_peran_check",
            )
        ]

    def __str__(self) -> str:
        return f"{self.nama} ({self.email})"

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return self.is_superuser

    def adalah_siswa(self) -> bool:
        return self.peran == "siswa"

    def adalah_guru(self) -> bool:
        return self.peran == "guru"

    def adalah_admin(self) -> bool:
        return self.peran == "admin"

    def sudah_selesai_onboarding(self) -> bool:
        """Mengecek apakah siswa sudah mengisi kuesioner minat dan tes diagnostik (UC-02/UC-03)."""
        if not self.adalah_siswa():
            return True
        return self.kuesioner_minat.exists()


class ProfilSiswa(models.Model):
    """Tabel 2: akun_profilsiswa."""

    KELAS_CHOICES = [("X", "X"), ("XI", "XI"), ("XII", "XII")]

    pengguna = models.OneToOneField(
        Pengguna, on_delete=models.CASCADE, related_name="profil_siswa"
    )
    kelas = models.CharField(max_length=10, choices=KELAS_CHOICES)
    email_orang_tua = models.EmailField(max_length=255)
    persetujuan_siswa_pada = models.DateTimeField()

    class Meta:
        db_table = "akun_profilsiswa"
        constraints = [
            models.CheckConstraint(
                check=models.Q(kelas__in=["X", "XI", "XII"]),
                name="akun_profilsiswa_kelas_check",
            )
        ]

    def __str__(self) -> str:
        return f"Profil {self.pengguna.nama} - Kelas {self.kelas}"


class GuruMapel(models.Model):
    """Tabel 4: akun_gurumapel."""

    guru = models.ForeignKey(
        Pengguna, on_delete=models.CASCADE, related_name="mapel_diampu"
    )
    mapel = models.ForeignKey(
        "pembelajaran.Mapel", on_delete=models.PROTECT, related_name="guru_pengampu"
    )

    class Meta:
        db_table = "akun_gurumapel"
        constraints = [
            models.UniqueConstraint(
                fields=["guru", "mapel"], name="akun_gurumapel_guru_mapel_uniq"
            )
        ]

    def __str__(self) -> str:
        return f"{self.guru.nama} - {self.mapel.kode}"