from django.shortcuts import render
from .forms import PemesananPaketForm, PembayaranTagihanForm, PAKET_AKTIF_KATALOG


def keranjang_view(request):
    """Halaman Pemesanan / Keranjang Paket Belajar."""
    form = PemesananPaketForm(request.POST or None)
    pesan_sukses = None
    pesan_galat = None

    if request.method == "POST":
        if form.is_valid():
            kode = form.cleaned_data["kode_paket"]
            durasi = form.cleaned_data["durasi_bulan"]
            nama_paket, harga = PAKET_AKTIF_KATALOG[kode]
            total = harga * durasi
            pesan_sukses = f"Tagihan paket {nama_paket} ({durasi} bulan) sebesar Rp {total:,} berhasil dibuat."
        else:
            pesan_galat = "Pesanan tidak dapat diproses. Periksa kembali isian form di bawah."

    return render(
        request,
        "langganan/keranjang.html",
        {
            "form": form,
            "pesan_sukses": pesan_sukses,
            "pesan_galat": pesan_galat,
        },
    )


def bayar_view(request):
    """Halaman Pembayaran Tagihan Langganan."""
    form = PembayaranTagihanForm(request.POST or None)
    pesan_sukses = None
    pesan_galat = None

    if request.method == "POST":
        if form.is_valid():
            nominal = form.cleaned_data["nominal_bayar"]
            kembalian = nominal - PembayaranTagihanForm.TOTAL_TAGIHAN_SIMULASI
            pesan_sukses = f"Pembayaran berhasil diverifikasi. Kembalian: Rp {kembalian:,}."
        else:
            pesan_galat = "Pembayaran gagal diproses. Periksa kembali data pembayaran Anda."

    return render(
        request,
        "langganan/bayar.html",
        {
            "form": form,
            "pesan_sukses": pesan_sukses,
            "pesan_galat": pesan_galat,
        },
    )
