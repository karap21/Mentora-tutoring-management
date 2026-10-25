from langganan.models import Tagihan
from akun.models import Pengguna


class PembayaranService:
    """Layanan pembuatan tagihan, verifikasi pembayaran orang tua, dan aktivasi langganan."""

    def __init__(self):
        self.__masa_berlaku_jam: int = 72

    def buat_tagihan(self, siswa: Pengguna, keranjang: list) -> Tagihan:
        """+ Public: Menyimpan header Tagihan, TagihanDetail, dan mengirim email ke orang tua."""
        pass

    def proses_pembayaran(self, token: str, nominal_bayar: int, setuju: bool) -> Tagihan:
        """+ Public: Memvalidasi pembayaran orang tua, menghitung kembalian, dan melunasi tagihan."""
        pass

    def _aktifkan_langganan(self, tagihan: Tagihan) -> None:
        """# Protected: Membuat baris Langganan aktif untuk setiap detail tagihan & cek unlock."""
        pass

    def __buat_nomor_invoice(self) -> str:
        """- Private: Menghasilkan nomor invoice dengan format INV-YYYYMMDD-NNNN (BR-17)."""
        pass

    def __kirim_email_tagihan(self, tagihan: Tagihan) -> None:
        """- Private: Mengirim link pembayaran bertoken ke email orang tua."""
        pass

    def __kirim_email_invoice(self, tagihan: Tagihan) -> None:
        """- Private: Mengirim file invoice PDF ke email orang tua."""
        pass