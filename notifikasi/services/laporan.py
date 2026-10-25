from datetime import date
from notifikasi.models import Notifikasi
from akun.models import Pengguna


class LaporanProgresService:
    """Layanan pengiriman laporan progres 14 hari ke orang tua dan notifikasi in-app (BR-12)."""

    def __init__(self):
        self.__interval_hari: int = 14

    def kirim_laporan_dua_mingguan(self) -> int:
        """+ Public: Mengirim email progres ke orang tua seluruh siswa berlangganan aktif."""
        pass

    def buat_notifikasi(self, pengguna: Pengguna, judul: str, pesan: str, tautan: str = None) -> Notifikasi:
        """+ Public: Membuat notifikasi in-app baru untuk siswa."""
        pass

    def _susun_ringkasan_siswa(self, siswa: Pengguna, mulai: date, akhir: date) -> dict:
        """# Protected: Mengambil ringkasan materi selesai, nilai kuis/tugas, dan rekomendasi."""
        pass