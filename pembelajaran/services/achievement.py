from typing import Optional
from pembelajaran.models import Achievement, AchievementSiswa
from akun.models import Pengguna


class AchievementService:
    """Layanan pemeriksa dan pemberi penghargaan belajar siswa (FR-23, UC-15)."""

    def periksa(self, siswa: Pengguna) -> list[Achievement]:
        """+ Public: Memeriksa keempat syarat achievement dan memberikan yang belum diraih."""
        pass

    def _beri_achievement(self, siswa: Pengguna, kode: str) -> Optional[AchievementSiswa]:
        """# Protected: Menyimpan pencapaian baru ke tabel pembelajaran_achievementsiswa."""
        pass