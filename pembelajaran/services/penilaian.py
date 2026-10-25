from decimal import Decimal
from pembelajaran.models import PercobaanKuis, JawabanSiswa, PengumpulanTugas
from akun.models import Pengguna


class PenilaianService:
    """Layanan penilaian otomatis pilihan ganda/isian serta penilaian esai/tugas oleh guru."""

    def nilai_otomatis(self, percobaan: PercobaanKuis) -> None:
        """+ Public: Menghitung skor otomatis dari soal PG dan isian (BR-15)."""
        pass

    def perbarui_skor_akhir(self, percobaan: PercobaanKuis) -> None:
        """+ Public: Menghitung skor akhir kuis setelah semua soal esai dinilai (BR-16)."""
        pass

    def simpan_nilai_esai(
        self, jawaban: JawabanSiswa, guru: Pengguna, poin: Decimal, catatan: str
    ) -> None:
        """+ Public: Menyimpan nilai esai dari guru dan memperbarui skor akhir."""
        pass

    def simpan_nilai_tugas(
        self, pengumpulan: PengumpulanTugas, guru: Pengguna, nilai: int, catatan: str
    ) -> None:
        """+ Public: Menyimpan nilai tugas (0-100) dari guru (UC-14)."""
        pass