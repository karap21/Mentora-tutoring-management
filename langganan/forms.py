from django import forms


PAKET_AKTIF_KATALOG = {
    "BDL-FULL": ("Paket Bundling Semua Mapel", 450000),
    "BDL-SAINS": ("Paket Bundling Sains (MTK, FIS, KIM, BIO)", 350000),
    "BDL-BHS": ("Paket Bundling Bahasa (BIN, BIG)", 200000),
    "MAP-MTK": ("Paket Matematika SMA", 120000),
    "MAP-FIS": ("Paket Fisika SMA", 120000),
    "MAP-KIM": ("Paket Kimia SMA", 120000),
    "MAP-BIO": ("Paket Biologi SMA", 120000),
    "MAP-BIN": ("Paket Bahasa Indonesia", 100000),
    "MAP-BIG": ("Paket Bahasa Inggris", 100000),
    "MAP-PPK": ("Paket Pendidikan Pancasila", 90000),
}

PAKET_NONAKTIF_KATALOG = {
    "PKT-LAMA-2024": "Paket Kurikulum Lama 2024",
    "BDL-ARSIP": "Paket Bundling Arsip",
}


class PemesananPaketForm(forms.Form):
    """Form Pemesanan / Keranjang Paket Belajar."""

    kode_paket = forms.CharField(
        label="Kode Paket",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "contoh: BDL-SAINS atau MAP-MTK",
            }
        ),
    )
    durasi_bulan = forms.CharField(
        label="Durasi Berlangganan (Bulan)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "1 - 12 bulan",
            }
        ),
    )
    kode_paket_tambahan = forms.CharField(
        label="Kode Paket Tambahan (Opsional)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Kosongkan jika hanya 1 paket",
            }
        ),
    )
    kode_diskon = forms.CharField(
        label="Kode Promo (Opsional)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukkan kode promo bila ada",
            }
        ),
    )

    def clean_kode_paket_tambahan(self):
        kode = (self.cleaned_data.get("kode_paket_tambahan") or "").strip().upper()
        if not kode:
            return ""  # opsional, boleh kosong
        if any(s in kode for s in ["' OR ", "OR 1=1", "DROP TABLE", "UNION SELECT", "--", ";", "<SCRIPT"]):
            raise forms.ValidationError("Format kode paket tambahan tidak valid.")
        if kode in PAKET_NONAKTIF_KATALOG:
            raise forms.ValidationError("Paket tambahan yang dipilih sudah tidak aktif.")
        if kode not in PAKET_AKTIF_KATALOG:
            raise forms.ValidationError("Kode paket tambahan tidak ditemukan.")
        return kode
    
    def clean_kode_paket(self):
        kode = (self.cleaned_data.get("kode_paket") or "").strip()
        if not kode:
            raise forms.ValidationError("Kode paket wajib diisi.")
        upper_kode = kode.upper()
        if any(sqli in upper_kode for sqli in ["' OR ", "OR 1=1", "DROP TABLE", "UNION SELECT", "--", ";", "<script"]):
            raise forms.ValidationError("Format kode paket tidak valid.")
        if upper_kode in PAKET_NONAKTIF_KATALOG:
            raise forms.ValidationError("Paket yang dipilih sudah tidak aktif.")
        if upper_kode not in PAKET_AKTIF_KATALOG:
            raise forms.ValidationError("Kode paket tidak ditemukan.")
        return upper_kode

    def clean_durasi_bulan(self):
        raw_durasi = (self.cleaned_data.get("durasi_bulan") or "").strip()
        if not raw_durasi:
            raise forms.ValidationError("Durasi berlangganan wajib diisi.")

        try:
            if "." in raw_durasi or "," in raw_durasi:
                raise forms.ValidationError("Durasi harus berupa angka bulat.")
            durasi = int(raw_durasi)
        except forms.ValidationError:
            raise
        except ValueError:
            raise forms.ValidationError("Durasi harus berupa angka bulat antara 1 sampai 12.")

        if durasi < 0:
            raise forms.ValidationError("Durasi berlangganan tidak boleh bernilai negatif.")
        if durasi == 0:
            raise forms.ValidationError("Durasi berlangganan minimal 1 bulan.")
        if durasi > 12:
            raise forms.ValidationError("Durasi berlangganan maksimal 12 bulan.")
        return durasi

    def clean_kode_diskon(self):
        kupon = (self.cleaned_data.get("kode_diskon") or "").strip()
        if not kupon:
            return ""
        upper_kupon = kupon.upper()
        if any(sqli in upper_kupon for sqli in ["'", "OR ", "1=1", "--", ";", "DROP"]):
            raise forms.ValidationError("Format kode promo tidak valid.")
        if upper_kupon not in ("HEMAT12", "MENTORA20"):
            raise forms.ValidationError("Kode promo tidak ditemukan atau sudah tidak berlaku.")
        return upper_kupon

    def clean(self):
        cleaned = super().clean()
        utama = (self.data.get("kode_paket") or "").strip().upper()
        tambahan = (self.data.get("kode_paket_tambahan") or "").strip().upper()
        if utama and tambahan and utama == tambahan:
            self.add_error(
                "kode_paket_tambahan",
                "Paket yang sama tidak dapat dipilih dua kali dalam satu transaksi.",
            )
        return cleaned


class PembayaranTagihanForm(forms.Form):
    """Form Pembayaran Tagihan Langganan."""

    TOTAL_TAGIHAN_SIMULASI = 350000
    NOMINAL_MAKSIMAL = 10_000_000

    token = forms.CharField(
        label="Token Pembayaran",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukkan token dari email tagihan",
            }
        ),
    )
    nominal_bayar = forms.CharField(
        label="Nominal Pembayaran (Rp)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukkan nominal sesuai tagihan",
            }
        ),
    )
    nama_file_bukti = forms.CharField(
        label="Bukti Pembayaran (PDF/JPG/PNG)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "contoh: bukti_transfer.pdf",
            }
        ),
    )
    setuju = forms.BooleanField(
        label="Saya selaku orang tua/wali menyetujui pembayaran tagihan ini",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_token(self):
        token = (self.cleaned_data.get("token") or "").strip()
        if not token:
            raise forms.ValidationError("Token pembayaran wajib diisi.")

        upper_token = token.upper()
        if any(sqli in upper_token for sqli in ["'", "UNION", "SELECT", "DROP", "OR 1=1", "--", ";"]):
            raise forms.ValidationError("Format token pembayaran tidak valid.")
        if upper_token == "TOKEN-KADALUWARSA":
            raise forms.ValidationError("Token pembayaran sudah kedaluwarsa (melebihi 72 jam).")
        if upper_token == "TOKEN-SUDAH-LUNAS":
            raise forms.ValidationError("Tagihan ini sudah lunas dan tidak dapat dibayar ulang.")
        if upper_token != "TOKEN-AKTIF-2026":
            raise forms.ValidationError("Token pembayaran tidak ditemukan.")
        return token

    def clean_nominal_bayar(self):
        raw_nom = (self.cleaned_data.get("nominal_bayar") or "").strip()
        if not raw_nom:
            raise forms.ValidationError("Nominal pembayaran wajib diisi.")

        try:
            nominal = int(raw_nom)
        except ValueError:
            raise forms.ValidationError("Nominal pembayaran harus berupa angka bulat.")

        if nominal < 0:
            raise forms.ValidationError("Nominal pembayaran tidak boleh bernilai negatif.")
        if nominal == 0:
            raise forms.ValidationError("Nominal pembayaran tidak boleh Rp 0.")
        if nominal < self.TOTAL_TAGIHAN_SIMULASI:
            raise forms.ValidationError(
                f"Nominal pembayaran kurang dari total tagihan (Rp {self.TOTAL_TAGIHAN_SIMULASI:,})."
            )
        if nominal > self.NOMINAL_MAKSIMAL:
                raise forms.ValidationError("Nominal pembayaran melebihi batas maksimal.")
        return nominal

    def clean_nama_file_bukti(self):
        nama_file = (self.cleaned_data.get("nama_file_bukti") or "").strip()
        if not nama_file:
            raise forms.ValidationError("Bukti pembayaran wajib diisi.")

        if "../" in nama_file or "..\\" in nama_file or "/etc/" in nama_file.lower():
            raise forms.ValidationError("Nama file tidak valid.")

        lower_file = nama_file.lower()
        ekstensi_valid = (".pdf", ".jpg", ".jpeg", ".png")
        if not lower_file.endswith(ekstensi_valid):
            raise forms.ValidationError("Format file tidak didukung. Gunakan file PDF, JPG, atau PNG.")
        return nama_file

    def clean_setuju(self):
        setuju = self.cleaned_data.get("setuju")
        if not setuju:
            raise forms.ValidationError("Persetujuan orang tua/wali wajib dicentang.")
        return setuju
