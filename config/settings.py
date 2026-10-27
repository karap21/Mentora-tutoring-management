from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-mentora-lms-tubes-impal-2026-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 5 App Mentora-LMS
    "akun",
    "langganan",
    "pembelajaran",
    "rekomendasi",
    "notifikasi",
    "django_browser_reload",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Konfigurasi Database PostgreSQL 16 (mentora_tubes)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "mentora_tubes"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "admin"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Custom User Model (akun_pengguna)
AUTH_USER_MODEL = "akun.Pengguna"

# Hashing Kata Sandi dengan bcrypt sesuai NFR-01 & 02_insert_data.sql
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/akun/masuk/"
LOGIN_REDIRECT_URL = "/siswa/"
LOGOUT_REDIRECT_URL = "/akun/masuk/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Konstanta Aturan Bisnis (DPPL Bab 4.1)
DURASI_MIN, DURASI_MAX = 1, 12          # BR-03
DURASI_DISKON, PERSEN_DISKON = 12, 20   # BR-04
MASA_BERLAKU_TOKEN_JAM = 72             # BR-07
AMBANG_PRETEST = 85                     # BR-08
AMBANG_KUIS_DASAR = 75                  # BR-09
INTERVAL_LAPORAN_HARI = 14              # BR-12