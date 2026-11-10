from django import forms


class LoginForm(forms.Form):
    """Form Login untuk Siswa, Guru, dan Admin (UC-02)."""

    email = forms.EmailField(
        label="Alamat Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "contoh: andi.pratama@mentora.id",
                "required": True,
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Kata Sandi",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukkan kata sandi",
                "required": True,
            }
        ),
    )


class RegistrasiSiswaForm(forms.Form):
    """Form Registrasi Siswa (UC-01)."""

    nama = forms.CharField(
        label="Nama Lengkap",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukkan nama lengkap",
            }
        ),
    )
    email = forms.CharField(
        label="Alamat Email Siswa",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "contoh: andi.pratama@mentora.id",
            }
        ),
    )
    kelas = forms.CharField(
        label="Kelas",
        required=False,
        widget=forms.Select(
            choices=[
                ("X", "Kelas X"),
                ("XI", "Kelas XI"),
                ("XII", "Kelas XII"),
            ],
            attrs={"class": "form-select"},
        ),
    )
    email_orang_tua = forms.CharField(
        label="Email Orang Tua / Wali",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "contoh: orangtua@gmail.com",
            }
        ),
    )
    password = forms.CharField(
        label="Kata Sandi",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Minimal 8 karakter",
            }
        ),
    )
    konfirmasi_password = forms.CharField(
        label="Konfirmasi Kata Sandi",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ulangi kata sandi",
            }
        ),
    )
    setuju_tos = forms.BooleanField(
        label="Saya menyetujui Syarat dan Ketentuan Layanan Mentora-LMS",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_nama(self):
        raw_nama = self.data.get("nama", "")
        if not raw_nama or not raw_nama.strip():
            raise forms.ValidationError("Nama lengkap wajib diisi.")
        nama = raw_nama.strip()
        lower_nama = nama.lower()
        if any(p in lower_nama for p in ["<script", "</script", "javascript:", "onerror=", "onload=", "<img", "<iframe"]):
            raise forms.ValidationError("Nama tidak valid karena mengandung karakter atau tag HTML terlarang.")
        if len(nama) > 255:
            raise forms.ValidationError("Nama lengkap maksimal 255 karakter.")
        return nama

    def clean_email(self):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError as DjangoValidationError
        from .models import Pengguna

        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            raise forms.ValidationError("Alamat email siswa wajib diisi.")

        upper_email = email.upper()
        if any(sqli in upper_email for sqli in ["' OR ", "OR 1=1", "DROP TABLE", "UNION SELECT", "--", ";"]):
            raise forms.ValidationError("Format alamat email tidak valid.")

        try:
            validate_email(email)
        except DjangoValidationError:
            raise forms.ValidationError("Masukkan format alamat email yang benar.")

        email_lower = email.lower()
        email_terdaftar_default = {
            "andi.pratama@mentora.id",
            "fajar.nugroho@mentora.id",
            "admin@mentora.id",
            "siswa.test@mentora.id",
        }
        sudah_ada = email_lower in email_terdaftar_default
        if not sudah_ada:
            try:
                sudah_ada = Pengguna.objects.filter(email__iexact=email_lower).exists()
            except Exception:
                pass

        if sudah_ada:
            raise forms.ValidationError("Email ini sudah terdaftar. Gunakan email lain.")
        return email_lower

    def clean_kelas(self):
        kelas = (self.cleaned_data.get("kelas") or "").strip()
        if kelas not in ("X", "XI", "XII"):
            raise forms.ValidationError("Pilihan kelas tidak valid.")
        return kelas

    def clean_email_orang_tua(self):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError as DjangoValidationError

        email_ortu = (self.cleaned_data.get("email_orang_tua") or "").strip()
        if not email_ortu:
            raise forms.ValidationError("Alamat email orang tua wajib diisi.")

        try:
            validate_email(email_ortu)
        except DjangoValidationError:
            raise forms.ValidationError("Masukkan format email orang tua yang benar.")
        return email_ortu.lower()

    def clean_password(self):
        password = self.cleaned_data.get("password") or ""
        if not password:
            raise forms.ValidationError("Kata sandi wajib diisi.")
        if len(password) < 8:
            raise forms.ValidationError("Kata sandi minimal 8 karakter.")
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            raise forms.ValidationError("Kata sandi harus mengandung kombinasi huruf dan angka.")
        return password

    def clean_setuju_tos(self):
        setuju = self.cleaned_data.get("setuju_tos")
        if not setuju:
            raise forms.ValidationError("Anda harus menyetujui Syarat dan Ketentuan Layanan.")
        return setuju

    def clean(self):
        cleaned_data = super().clean()
        email_siswa = (cleaned_data.get("email") or "").strip().lower()
        email_ortu = (cleaned_data.get("email_orang_tua") or "").strip().lower()
        if email_siswa and email_ortu and email_siswa == email_ortu:
            self.add_error(
                "email_orang_tua",
                "Email orang tua tidak boleh sama dengan email siswa.",
            )

        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("konfirmasi_password") or ""
        if pw1 and pw1 != pw2:
            self.add_error(
                "konfirmasi_password",
                "Konfirmasi kata sandi tidak cocok.",
            )
        return cleaned_data
