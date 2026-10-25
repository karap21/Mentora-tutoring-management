from django.db import models
from django.utils import timezone


class Paket(models.Model):
    """Tabel 12: langganan_paket (PRODUK)."""

    kode = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=255)
    jenis = models.CharField(max_length=50)
    harga_per_bulan = models.IntegerField()
    aktif = models.BooleanField(default=True)

    class Meta:
        db_table = "langganan_paket"

    def __str__(self) -> str:
        return f"{self.kode} - {self.nama}"

    def daftar_mapel(self):
        pass


class PaketMapel(models.Model):
    """Tabel 13: langganan_paketmapel."""

    paket = models.ForeignKey(Paket, on_delete=models.CASCADE, related_name="paket_mapel")
    mapel = models.ForeignKey("pembelajaran.Mapel", on_delete=models.PROTECT)

    class Meta:
        db_table = "langganan_paketmapel"


class Tagihan(models.Model):
    """Tabel 14: langganan_tagihan (PENJUALAN)."""

    nomor_invoice = models.CharField(max_length=100, unique=True)
    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.PROTECT, related_name="tagihan")
    subtotal = models.IntegerField()
    diskon_nominal = models.IntegerField(default=0)
    total = models.IntegerField()
    nominal_bayar = models.IntegerField(null=True, blank=True)
    kembalian = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="menunggu")
    token = models.CharField(max_length=64, unique=True)
    token_berlaku_sampai = models.DateTimeField()
    persetujuan_ortu_pada = models.DateTimeField(null=True, blank=True)
    file_invoice = models.CharField(max_length=255, null=True, blank=True)
    dibuat_pada = models.DateTimeField(default=timezone.now)
    dibayar_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "langganan_tagihan"

    def apakah_token_valid(self) -> bool:
        pass


class TagihanDetail(models.Model):
    """Tabel 15: langganan_tagihandetail (PENJUALANDetail)."""

    tagihan = models.ForeignKey(Tagihan, on_delete=models.CASCADE, related_name="detail")
    paket = models.ForeignKey(Paket, on_delete=models.PROTECT)
    durasi_bulan = models.SmallIntegerField()
    harga_per_bulan = models.IntegerField()
    subtotal = models.IntegerField()
    diskon_persen = models.IntegerField(default=0)
    diskon_nominal = models.IntegerField(default=0)
    total = models.IntegerField()

    class Meta:
        db_table = "langganan_tagihandetail"


class Langganan(models.Model):
    """Tabel 16: langganan_langganan."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.PROTECT, related_name="langganan")
    paket = models.ForeignKey(Paket, on_delete=models.PROTECT)
    tagihan_detail = models.OneToOneField(TagihanDetail, on_delete=models.PROTECT)
    mulai = models.DateField()
    berakhir = models.DateField()

    class Meta:
        db_table = "langganan_langganan"

    def masih_aktif(self) -> bool:
        pass