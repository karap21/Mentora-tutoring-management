from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from akun.models import Pengguna, ProfilSiswa, GuruMapel
from pembelajaran.models import Mapel, Modul, Achievement, AchievementSiswa
from langganan.models import Paket, PaketMapel, Tagihan, TagihanDetail, Langganan
from rekomendasi.models import Rekomendasi, KuesionerMinat


class Command(BaseCommand):
    help = "Mengisi database dengan akun pengujian (Siswa, Guru, Admin) dan data master resmi SKPL BR-01 Mentora-LMS"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Memulai seeding data resmi SKPL Mentora-LMS..."))

        # Bersihkan data paket/mapel lama jika bukan kode BR-01
        Langganan.objects.all().delete()
        TagihanDetail.objects.all().delete()
        Tagihan.objects.all().delete()
        PaketMapel.objects.all().delete()
        Paket.objects.exclude(
            kode__in=[
                "MAP-BIN", "MAP-BIG", "MAP-MTK", "MAP-FIS", "MAP-KIM", "MAP-BIO", "MAP-PPK",
                "BDL-BHS", "BDL-SAINS", "BDL-FULL"
            ]
        ).delete()
        Rekomendasi.objects.all().delete()
        KuesionerMinat.objects.all().delete()
        GuruMapel.objects.all().delete()
        Modul.objects.all().delete()
        Mapel.objects.exclude(kode__in=["BIN", "BIG", "MTK", "FIS", "KIM", "BIO", "PPK"]).delete()

        # 1. Buat Pengguna Uji (Password: Mentora123!)
        siswa, _ = Pengguna.objects.get_or_create(
            email="andi.pratama@mentora.id",
            defaults={
                "nama": "Andi Pratama",
                "peran": "siswa",
                "is_active": True,
            },
        )
        siswa.set_password("Mentora123!")
        siswa.save()

        ProfilSiswa.objects.get_or_create(
            pengguna=siswa,
            defaults={
                "kelas": "XII",
                "email_orang_tua": "orangtua.andi@gmail.com",
                "persetujuan_siswa_pada": timezone.now(),
            },
        )

        guru, _ = Pengguna.objects.get_or_create(
            email="fajar.nugroho@mentora.id",
            defaults={
                "nama": "Fajar Nugroho, S.Pd.",
                "peran": "guru",
                "is_active": True,
            },
        )
        guru.set_password("Mentora123!")
        guru.save()

        admin, _ = Pengguna.objects.get_or_create(
            email="admin@mentora.id",
            defaults={
                "nama": "Administrator Mentora",
                "peran": "admin",
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("Mentora123!")
        admin.save()

        self.stdout.write(self.style.SUCCESS("[OK] Akun Siswa, Guru, dan Admin berhasil dibuat."))

        # 2. Buat 7 Mata Pelajaran Resmi SKPL (AI-03 & BR-01)
        mapel_data = [
            ("MTK", "Matematika"),
            ("FIS", "Fisika"),
            ("KIM", "Kimia"),
            ("BIO", "Biologi"),
            ("BIN", "Bahasa Indonesia"),
            ("BIG", "Bahasa Inggris"),
            ("PPK", "Pendidikan Pancasila"),
        ]

        mapel_objs = {}
        for kode, nama in mapel_data:
            m, _ = Mapel.objects.update_or_create(kode=kode, defaults={"nama": nama})
            mapel_objs[kode] = m

            Modul.objects.get_or_create(
                mapel=m, urutan=1,
                defaults={"judul": f"Modul Level Dasar {nama}", "level": "dasar"}
            )
            Modul.objects.get_or_create(
                mapel=m, urutan=2,
                defaults={"judul": f"Modul Level Lanjutan {nama}", "level": "lanjutan"}
            )

        GuruMapel.objects.get_or_create(guru=guru, mapel=mapel_objs["MTK"])
        GuruMapel.objects.get_or_create(guru=guru, mapel=mapel_objs["FIS"])

        self.stdout.write(self.style.SUCCESS("[OK] 7 Mata pelajaran resmi SKPL (AI-03) & modul berhasil dibuat."))

        # 3. Buat 10 Paket Langganan Resmi SKPL (BR-01)
        paket_satuan_specs = [
            ("MAP-MTK", "Matematika", ["MTK"], 50000),
            ("MAP-FIS", "Fisika", ["FIS"], 50000),
            ("MAP-KIM", "Kimia", ["KIM"], 50000),
            ("MAP-BIO", "Biologi", ["BIO"], 50000),
            ("MAP-BIN", "Bahasa Indonesia", ["BIN"], 50000),
            ("MAP-BIG", "Bahasa Inggris", ["BIG"], 50000),
            ("MAP-PPK", "Pendidikan Pancasila", ["PPK"], 50000),
        ]

        bundel_specs = [
            ("BDL-SAINS", "Bundel Sains", ["MTK", "FIS", "KIM", "BIO"], 150000),
            ("BDL-BHS", "Bundel Bahasa", ["BIN", "BIG"], 80000),
            ("BDL-FULL", "Bundel Lengkap", ["BIN", "BIG", "MTK", "FIS", "KIM", "BIO", "PPK"], 250000),
        ]

        paket_objs = {}
        for kode, nama, mapel_kodes, harga in paket_satuan_specs:
            p, _ = Paket.objects.update_or_create(
                kode=kode,
                defaults={"nama": nama, "jenis": "mapel", "harga_per_bulan": harga, "aktif": True},
            )
            paket_objs[kode] = p
            for mk in mapel_kodes:
                PaketMapel.objects.get_or_create(paket=p, mapel=mapel_objs[mk])

        for kode, nama, mapel_kodes, harga in bundel_specs:
            p, _ = Paket.objects.update_or_create(
                kode=kode,
                defaults={"nama": nama, "jenis": "bundel", "harga_per_bulan": harga, "aktif": True},
            )
            paket_objs[kode] = p
            for mk in mapel_kodes:
                PaketMapel.objects.get_or_create(paket=p, mapel=mapel_objs[mk])

        self.stdout.write(self.style.SUCCESS("[OK] 10 Paket langganan resmi SKPL (BR-01) berhasil dibuat."))

        # 4. Buat 4 Lencana Achievement
        achievements_data = [
            ("ACH-01", "Langkah Pertama", "Menyelesaikan kuesioner minat dan tes diagnostik pertama."),
            ("ACH-02", "Penakluk Pretest", "Meraih skor tes diagnostik >= 85 dan membuka modul Level Lanjutan."),
            ("ACH-03", "Tuntas Modul", "Menuntaskan seluruh materi dan lulus kuis dasar dengan skor minimal 75."),
            ("ACH-04", "Disiplin Tepat Waktu", "Mengumpulkan tugas mandiri sebelum tenggat waktu dengan evaluasi baik."),
        ]
        for kode, nama, desc in achievements_data:
            ach, _ = Achievement.objects.update_or_create(kode=kode, defaults={"nama": nama, "deskripsi": desc})
            if kode in ["ACH-01", "ACH-02"]:
                AchievementSiswa.objects.get_or_create(siswa=siswa, achievement=ach)

        # 5. Rekomendasi & Kuesioner Minat untuk Siswa Andi
        KuesionerMinat.objects.get_or_create(
            siswa=siswa,
            defaults={"mapel_diminati": mapel_objs["MTK"], "tujuan_belajar": "utbk"},
        )
        Rekomendasi.objects.get_or_create(
            siswa=siswa,
            defaults={"mapel": mapel_objs["MTK"], "sumber": "model"},
        )

        # 6. Tagihan & Langganan Aktif untuk Andi (Contoh SKPL BR-18: BDL-SAINS 12 Bulan)
        paket_sains = paket_objs["BDL-SAINS"]
        tagihan, _ = Tagihan.objects.get_or_create(
            nomor_invoice="INV-20261026-0001",
            defaults={
                "siswa": siswa,
                "subtotal": 1800000,
                "diskon_nominal": 360000,
                "total": 1440000,
                "nominal_bayar": 1500000,
                "kembalian": 60000,
                "status": "lunas",
                "token": "token-demo-andi-2026",
                "token_berlaku_sampai": timezone.now() + timedelta(hours=72),
                "persetujuan_ortu_pada": timezone.now(),
                "dibayar_pada": timezone.now(),
            },
        )
        tagihan_detail, _ = TagihanDetail.objects.get_or_create(
            tagihan=tagihan,
            paket=paket_sains,
            defaults={
                "durasi_bulan": 12,
                "harga_per_bulan": 150000,
                "subtotal": 1800000,
                "diskon_persen": 20,
                "diskon_nominal": 360000,
                "total": 1440000,
            },
        )
        Langganan.objects.get_or_create(
            siswa=siswa,
            paket=paket_sains,
            defaults={
                "tagihan_detail": tagihan_detail,
                "mulai": timezone.now().date(),
                "berakhir": timezone.now().date() + timedelta(days=365),
            },
        )

        self.stdout.write(self.style.SUCCESS("[OK] Data dummy langganan BDL-SAINS & rekomendasi berhasil disiapkan."))
        self.stdout.write(self.style.SUCCESS("Seeding selesai sempurna! Silakan jalankan 'python manage.py runserver'."))
