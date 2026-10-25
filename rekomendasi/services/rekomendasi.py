from rekomendasi.models import KuesionerMinat, Rekomendasi
from akun.models import Pengguna


class RekomendasiService:
    """Layanan prediksi mapel prioritas dengan Decision Tree dan fallback (AI-08, BR-11)."""

    def __init__(self):
        self.__jalur_model: str = "rekomendasi/ml/model_rekomendasi.joblib"
        self._cache_model = None

    def rekomendasikan(self, siswa: Pengguna) -> Rekomendasi:
        """+ Public: Menyusun vektor fitur, memanggil model Decision Tree, dan menyimpan hasil."""
        pass

    def _fallback(self, kuesioner: KuesionerMinat, skor: dict) -> str:
        """# Protected: Menjalankan aturan fallback BR-11 bila model gagal dimuat/memprediksi."""
        pass

    def __muat_model(self) -> object:
        """- Private: Memuat artefak joblib sekali ke dalam memori."""
        pass