from typing import Optional
from decimal import Decimal
from pembelajaran.models import Mapel
from akun.models import Pengguna


class AdaptivePathService:
    """Layanan pembuka kunci (unlock) modul lanjutan secara adaptif (BR-08, BR-09)."""

    def __init__(self):
        self.__ambang_pretest: int = 85
        self.__ambang_kuis_dasar: int = 75

    def cek_unlock(self, siswa: Pengguna, mapel: Mapel) -> None:
        """+ Public: Memeriksa syarat BR-08 dan BR-09 lalu membuka modul lanjutan bila terpenuhi."""
        pass

    def _buka(self, siswa: Pengguna, modul_qs, sumber: str) -> None:
        """# Protected: Mencatat akses modul lanjutan ke tabel pembelajaran_aksesmodul."""
        pass

    def __ambil_skor_diagnostik(self, siswa: Pengguna, mapel: Mapel) -> Optional[Decimal]:
        """- Private: Mengambil skor tes diagnostik siswa pada mapel terkait."""
        pass