from langganan.models import Paket


class PricingService:
    """Layanan perhitungan harga, diskon, dan subtotal keranjang (BR-02 s.d. BR-05, BR-18)."""

    def __init__(self):
        self.__durasi_min: int = 1
        self.__durasi_max: int = 12
        self.__durasi_diskon: int = 12
        self.__persen_diskon: int = 20

    def cari_paket(self, kode: str) -> Paket:
        """+ Public: Mencari paket aktif berdasarkan kode (case-insensitive)."""
        pass

    def hitung_item(self, paket: Paket, durasi: int) -> dict:
        """+ Public: Menghitung subtotal, diskon, dan total untuk satu baris detail."""
        pass

    def hitung_tagihan(self, keranjang: list[tuple[Paket, int]]) -> dict:
        """+ Public: Menghitung keseluruhan tagihan dari daftar item di keranjang."""
        pass

    def __validasi_duplikasi_keranjang(self, keranjang: list[tuple[Paket, int]]) -> None:
        """- Private: Memastikan tidak ada paket yang sama dua kali dalam satu tagihan (BR-18)."""
        pass