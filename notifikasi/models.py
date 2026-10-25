from django.db import models
from django.utils import timezone


class Notifikasi(models.Model):
    """Tabel 25: notifikasi_notifikasi."""

    pengguna = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="notifikasi")
    judul = models.CharField(max_length=255)
    pesan = models.TextField()
    tautan = models.CharField(max_length=255, null=True, blank=True)
    dibaca = models.BooleanField(default=False)
    dibuat_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "notifikasi_notifikasi"

    def tandai_dibaca(self) -> None:
        pass


class LogEmailProgres(models.Model):
    """Tabel 26: notifikasi_logemailprogres."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="log_email_progres")
    periode_mulai = models.DateField()
    periode_akhir = models.DateField()
    status = models.CharField(max_length=50)
    dikirim_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "notifikasi_logemailprogres"