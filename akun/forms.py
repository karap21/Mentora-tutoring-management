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
    """Kerangka Form Registrasi Siswa (UC-01)."""

    nama = forms.CharField(max_length=255)
    email = forms.EmailField()
    kelas = forms.ChoiceField(choices=[("X", "X"), ("XI", "XI"), ("XII", "XII")])
    email_orang_tua = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    konfirmasi_password = forms.CharField(widget=forms.PasswordInput)
    setuju_tos = forms.BooleanField(required=True)

    def clean(self):
        pass