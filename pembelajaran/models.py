from django.db import models
from django.utils import timezone


class Mapel(models.Model):
    """Tabel 3: pembelajaran_mapel."""

    kode = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=255)

    class Meta:
        db_table = "pembelajaran_mapel"

    def __str__(self) -> str:
        return f"{self.kode} - {self.nama}"


class Modul(models.Model):
    """Tabel 5: pembelajaran_modul."""

    mapel = models.ForeignKey(Mapel, on_delete=models.PROTECT, related_name="modul")
    judul = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    urutan = models.SmallIntegerField()

    class Meta:
        db_table = "pembelajaran_modul"

    def apakah_terkunci(self, siswa) -> bool:
        pass


class Materi(models.Model):
    """Tabel 6: pembelajaran_materi."""

    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, related_name="materi")
    judul = models.CharField(max_length=255)
    tipe = models.CharField(max_length=50)
    konten_teks = models.TextField(null=True, blank=True)
    file_pdf = models.CharField(max_length=255, null=True, blank=True)
    gambar = models.CharField(max_length=255, null=True, blank=True)
    urutan = models.SmallIntegerField()

    class Meta:
        db_table = "pembelajaran_materi"


class Kuis(models.Model):
    """Tabel 7: pembelajaran_kuis."""

    mapel = models.ForeignKey(Mapel, on_delete=models.PROTECT, related_name="kuis")
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, null=True, blank=True, related_name="kuis")
    judul = models.CharField(max_length=255)
    jenis = models.CharField(max_length=50)

    class Meta:
        db_table = "pembelajaran_kuis"


class Soal(models.Model):
    """Tabel 8: pembelajaran_soal."""

    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name="soal")
    tipe = models.CharField(max_length=50)
    pertanyaan = models.TextField()
    kunci_isian = models.TextField(null=True, blank=True)
    bobot = models.SmallIntegerField()
    urutan = models.SmallIntegerField()

    class Meta:
        db_table = "pembelajaran_soal"


class PilihanJawaban(models.Model):
    """Tabel 9: pembelajaran_pilihanjawaban."""

    soal = models.ForeignKey(Soal, on_delete=models.CASCADE, related_name="pilihan")
    teks = models.CharField(max_length=255)
    benar = models.BooleanField()

    class Meta:
        db_table = "pembelajaran_pilihanjawaban"


class Achievement(models.Model):
    """Tabel 10: pembelajaran_achievement."""

    kode = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()

    class Meta:
        db_table = "pembelajaran_achievement"


class Tugas(models.Model):
    """Tabel 11: pembelajaran_tugas."""

    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, related_name="tugas")
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    tenggat = models.DateTimeField()

    class Meta:
        db_table = "pembelajaran_tugas"


class ProgresMateri(models.Model):
    """Tabel 17: pembelajaran_progresmateri."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="progres_materi")
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)
    selesai_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "pembelajaran_progresmateri"


class PercobaanKuis(models.Model):
    """Tabel 18: pembelajaran_percobaankuis."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="percobaan_kuis")
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE)
    skor_otomatis = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skor_akhir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50)
    dikumpulkan_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "pembelajaran_percobaankuis"


class JawabanSiswa(models.Model):
    """Tabel 19: pembelajaran_jawabansiswa."""

    percobaan = models.ForeignKey(PercobaanKuis, on_delete=models.CASCADE, related_name="jawaban")
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE)
    pilihan = models.ForeignKey(PilihanJawaban, on_delete=models.SET_NULL, null=True, blank=True)
    jawaban_teks = models.TextField(null=True, blank=True)
    poin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    catatan_guru = models.TextField(null=True, blank=True)
    dinilai_oleh = models.ForeignKey("akun.Pengguna", on_delete=models.SET_NULL, null=True, blank=True)
    dinilai_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pembelajaran_jawabansiswa"


class PengumpulanTugas(models.Model):
    """Tabel 20: pembelajaran_pengumpulantugas."""

    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE, related_name="pengumpulan")
    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="pengumpulan_tugas")
    file = models.CharField(max_length=255)
    dikumpulkan_pada = models.DateTimeField(default=timezone.now)
    terlambat = models.BooleanField(default=False)
    nilai = models.SmallIntegerField(null=True, blank=True)
    catatan = models.TextField(null=True, blank=True)
    dinilai_oleh = models.ForeignKey("akun.Pengguna", on_delete=models.SET_NULL, null=True, blank=True)
    dinilai_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pembelajaran_pengumpulantugas"


class AksesModul(models.Model):
    """Tabel 21: pembelajaran_aksesmodul."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="akses_modul")
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    sumber = models.CharField(max_length=50)
    dibuka_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "pembelajaran_aksesmodul"


class AchievementSiswa(models.Model):
    """Tabel 22: pembelajaran_achievementsiswa."""

    siswa = models.ForeignKey("akun.Pengguna", on_delete=models.CASCADE, related_name="achievement_diraih")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    diraih_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "pembelajaran_achievementsiswa"