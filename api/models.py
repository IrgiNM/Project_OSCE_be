from django.db import models
from django.contrib.auth.models import AbstractUser


# USER
class User(AbstractUser):
    nim = models.CharField(max_length=50, unique=True, null=True, blank=True)
    nama_lengkap = models.CharField(max_length=100, null=True, blank=True)
    kelas = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.nama_lengkap


# JENIS SOP
class JenisSOP(models.Model):
    judul = models.TextField()

    def __str__(self):
        return self.judul[:50]


# SOAL SOP
class SoalSOP(models.Model):
    soal = models.TextField()
    category = models.CharField(blank=True, null=True)
    nama_sop = models.CharField(blank=True, null=True)
    bobot = models.IntegerField(default=0)

    def __str__(self):
        return self.soal[:50] + " - " + self.nama_sop[:50]


# DETAIL SOAL SOP
class DetailSoalSOP(models.Model):
    sop = models.ForeignKey(
        SoalSOP,
        on_delete=models.CASCADE,
        related_name='jenis_soal'
    )
    bobot = models.IntegerField(default=0)
    deskripsi_soal = models.TextField()

    def __str__(self):
        return self.sop.soal[:50] + " - " + self.deskripsi_soal[:50]


# TEST SESI UJIAN
class SesiUjian(models.Model):
    nama_sesi = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_sesi
    
    
# TEST SISWA
class Test(models.Model):
    sesi = models.ForeignKey(
        SesiUjian,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='test_siswa'
    )
    sop = models.CharField(blank=True, null=True)
    total_nilai = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test {self.id} - {self.user.nama_lengkap}"


# DETAIL NILAI PER SOAL
class DetailTest(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='detail_test'
    )
    soal_sop = models.ForeignKey(
        SoalSOP,
        on_delete=models.CASCADE
    )
    nilai = models.IntegerField()

    def __str__(self):
        return f"{self.test.id} - {self.soal_sop.id}"