from langganan.models import Tagihan


class InvoiceGenerator:
    """Layanan pembuat dokumen Invoice PDF menggunakan ReportLab (FR-11)."""

    def __init__(self):
        self.__direktori_output: str = "invoice/"

    def buat_pdf(self, tagihan: Tagihan) -> str:
        """+ Public: Menghasilkan file PDF untuk tagihan lunas dan mengembalikan path relatifnya."""
        pass

    def __render_tabel_item(self, canvas: object, tagihan: Tagihan) -> None:
        """- Private: Menggambar rincian tabel paket pada kanvas PDF."""
        pass