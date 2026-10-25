from django.db import models
from django.utils import timezone


class KuesionerMinat(models.Model):
    """Tabel 23: rekomendasi_kuesionerminat."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="kuesioner_minat")
    mapel_diminati = models.ForeignKey("pembelajaran.Mapel", on_delete=models.PROTECT)
    tujuan_belajar = models.CharField(max_length=50)
    diisi_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "rekomendasi_kuesionerminat"


class Rekomendasi(models.Model):
    """Tabel 24: rekomendasi_rekomendasi."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="rekomendasi")
    mapel = models.ForeignKey("pembelajaran.Mapel", on_delete=models.PROTECT)
    sumber = models.CharField(max_length=50)
    dibuat_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "rekomendasi_rekomendasi"