import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


class Command(BaseCommand):
    help = "Seeder user mahasiswa dari file JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="users_angkatan_2024.json",
            help="Path file JSON user"
        )

        parser.add_argument(
            "--password",
            type=str,
            default="12345678",
            help="Password default jika data JSON tidak punya password"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = Path(options["file"])
        default_password = options["password"]

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR(f"File tidak ditemukan: {file_path}")
            )
            return

        with open(file_path, "r", encoding="utf-8") as file:
            users_data = json.load(file)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for data in users_data:
            nim = str(data.get("nim", "")).strip()
            nama_lengkap = data.get("nama_lengkap", "").strip()
            kelas = data.get("kelas", "").strip()
            email = data.get("email", "").strip()
            password = data.get("password") or default_password
            is_staff = data.get("is_staff", False)

            if not nim or not nama_lengkap or not email:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Data dilewati karena tidak lengkap: {data}")
                )
                continue

            user = User.objects.filter(nim=nim).first()

            if user:
                user.nama_lengkap = nama_lengkap
                user.kelas = kelas
                user.email = email
                user.username = email
                user.is_staff = is_staff
                user.set_password(password)
                user.save()

                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated: {nama_lengkap}")
                )

            else:
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    nim=nim,
                    nama_lengkap=nama_lengkap,
                    kelas=kelas,
                    is_staff=is_staff,
                )

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {nama_lengkap}")
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seeder selesai"))
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
        self.stdout.write(self.style.WARNING(f"Updated: {updated_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped: {skipped_count}"))