from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


# USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nim',
            'nama_lengkap',
            'kelas',
            'email',
            'status',
            'password',
            'is_staff',
        ]

    def validate(self, data):
        nim = data.get('nim')
        nama_lengkap = data.get('nama_lengkap')
        email = data.get('email')

        if nim and User.objects.filter(nim=nim).exists():
            raise serializers.ValidationError({
                'nim': 'NIM sudah digunakan'
            })

        if nama_lengkap and User.objects.filter(nama_lengkap=nama_lengkap).exists():
            raise serializers.ValidationError({
                'nama_lengkap': 'Nama lengkap sudah digunakan'
            })

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Email sudah digunakan'
            })

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            username=validated_data.get('email'),
            nim=validated_data.get('nim'),
            nama_lengkap=validated_data.get('nama_lengkap'),
            email=validated_data.get('email'),
            kelas=validated_data.get('kelas'),
            status=validated_data.get('status'),
            is_staff=validated_data.get('is_staff', False),
        )

        user.set_password(password)
        user.save()

        return user

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user_obj = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Email tidak ditemukan'
            )
        user = authenticate(
            username=user_obj.username,
            password=password
        )
        if not user:
            raise serializers.ValidationError(
                'Password salah'
            )
        attrs['user'] = user
        return attrs

# DETAIL SOAL SOP SERIALIZER
class DetailSoalSOPSerializer(serializers.ModelSerializer):
    sop_detail = serializers.SerializerMethodField()
    class Meta:
        model = DetailSoalSOP
        fields = [
            'id',
            'deskripsi_soal',
            'sop',
            'sop_detail',
        ]

    def get_sop_detail(self, obj):
        return {
            'id': obj.sop.id,
            'soal': obj.sop.soal,
            'category': obj.sop.category,
            'nama_sop': obj.sop.nama_sop,
        }

    def validate(self, data):
        deskripsi_soal = data.get('deskripsi_soal')
        sop = data.get('sop')

        if DetailSoalSOP.objects.filter(
            deskripsi_soal=deskripsi_soal,
            sop=sop
        ).exists():
            raise serializers.ValidationError({
                'detail_soal': 'Deskripsi soal dengan SOP ini sudah ada'
            })

        return data


# JENIS SOP SERIALIZER
class JenisSOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisSOP
        fields = '__all__'

# SOAL SOP SERIALIZER
class SoalSOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoalSOP
        fields = '__all__'

# SESI UJIAN SERIALIZER 
class SesiUjianSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesiUjian
        fields = [
            'id',
            'nama_sesi',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

# TEST SERIALIZER
class TestSerializer(serializers.ModelSerializer):
    sesi_detail = SesiUjianSerializer(
        source='sesi',
        read_only=True
    )
    user_detail = UserSerializer(
        source='user',
        read_only=True
    )
    class Meta:
        model = Test
        fields = [
            'id',
            'user',
            'sesi',
            'sop',
            'total_nilai',
            'created_at',
            'sesi_detail',
            'user_detail',
        ]


# DETAIL TEST SERIALIZER
class DetailTestSerializer(serializers.ModelSerializer):
    test_detail = TestSerializer(
        source='test',
        read_only=True
    )
    soal_sop_detail = SoalSOPSerializer(
        source='soal_sop',
        read_only=True
    )
    class Meta:
        model = DetailTest
        fields = [
            'id',
            'test',
            'soal_sop',
            'nilai',
            'test_detail',
            'soal_sop_detail',
        ]