from rest_framework import generics, permissions
from .models import *
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery
from rest_framework.authentication import TokenAuthentication


# USER
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(
            data=request.data,
            many=many
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user

class UserDosenListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(
            is_staff=True
        )

class UserMahasiswaListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(
            is_staff=False
        )

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DeleteAllUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        total = User.objects.count()
        User.objects.all().delete()
        return Response(
            {
                "message": f"{total} user berhasil dihapus"
            },
            status=status.HTTP_200_OK
        )

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_obj = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            return Response({
                'message': 'Email tidak ditemukan'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=user_obj.username,
            password=password
        )
        if not user:
            return Response({
                'message': 'Password salah'
            }, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(
            user=user
        )
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'nim': user.nim,
                'nama_lengkap': user.nama_lengkap,
                'email': user.email,
                'is_staff': user.is_staff,
            }
        })


# JENIS SOP
class CreateJenisSOPView(generics.CreateAPIView):
    queryset = JenisSOP.objects.all()
    serializer_class = JenisSOPSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(
            data=request.data,
            many=many
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class ListJenisSOPView(generics.ListAPIView):
    queryset = JenisSOP.objects.all()
    serializer_class = JenisSOPSerializer
    

# SOAL SOP
class CreateSoalSOPView(generics.CreateAPIView):
    queryset = SoalSOP.objects.all()
    serializer_class = SoalSOPSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(
            data=request.data,
            many=many
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ListSoalSOPView(generics.ListAPIView):
    queryset = SoalSOP.objects.all()
    serializer_class = SoalSOPSerializer

class ListSoalSOPByNamaView(generics.ListAPIView):
    serializer_class = SoalSOPSerializer

    def get_queryset(self):
        nama_sop = self.kwargs['nama_sop']
        return SoalSOP.objects.filter(
            nama_sop=nama_sop
        ).order_by('id')

class UpdateSoalSOPView(generics.UpdateAPIView):
    queryset = SoalSOP.objects.all()
    serializer_class = SoalSOPSerializer

class DeleteSoalSOPView(generics.DestroyAPIView):
    queryset = SoalSOP.objects.all()
    serializer_class = SoalSOPSerializer


# DETAIL SOP
class CreateDetailSOPView(generics.CreateAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(
            data=request.data,
            many=many
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ListDetailSOPView(generics.ListAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

class ListDetailSOPBySopView(generics.ListAPIView):
    serializer_class = DetailSoalSOPSerializer

    def get_queryset(self):
        id_sop = self.kwargs.get("id_sop")
        return DetailSoalSOP.objects.filter(sop=id_sop)

class UpdateDetailSOPView(generics.UpdateAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

class DeleteDetailSOPView(generics.DestroyAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

class DeleteAllDetailSOPView(APIView):
    def delete(self, request):
        total_data = DetailSoalSOP.objects.count()
        DetailSoalSOP.objects.all().delete()
        return Response(
            {
                "message": "Semua data DetailSoalSOP berhasil dihapus",
                "total_deleted": total_data,
            },
            status=status.HTTP_200_OK
        )


# TEST SESI
class CreateSesiTestView(generics.CreateAPIView):
    queryset = SesiUjian.objects.all()
    serializer_class = SesiUjianSerializer

    def create(self, request, *args, **kwargs):
        count = SesiUjian.objects.count() + 1
        nama_sesi = f"Sesi {count}"
        serializer = self.get_serializer(
            data={"nama_sesi": nama_sesi}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
class UpdateSesiUjianView(generics.UpdateAPIView):
    queryset = SesiUjian.objects.all()
    serializer_class = SesiUjianSerializer
    lookup_field = 'id'

class ListSesiUjianView(generics.ListAPIView):
    queryset = SesiUjian.objects.all().order_by('-id')
    serializer_class = SesiUjianSerializer

class DeleteAllSesiView(generics.GenericAPIView):
    queryset = SesiUjian.objects.all()
    serializer_class = SesiUjianSerializer

    def delete(self, request, *args, **kwargs):
        total = SesiUjian.objects.count()
        SesiUjian.objects.all().delete()
        return Response(
            {
                "message": f"{total} Sesi Ujian berhasil dihapus"
            },
            status=status.HTTP_200_OK
        )


# TEST
class CreateTestView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class ListTestView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class ListLatestTestView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        latest_test_per_user_sop = Test.objects.filter(
            user_id=OuterRef('user_id'),
            sop=OuterRef('sop')
        ).order_by('-created_at', '-id')

        return Test.objects.filter(
            id=Subquery(latest_test_per_user_sop.values('id')[:1])
        ).order_by('user_id', 'sop')

class ListTestByUserView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        latest_test_per_sop = Test.objects.filter(
            user_id=user_id,
            sop=OuterRef('sop')
        ).order_by('-created_at', '-id')

        return Test.objects.filter(
            user_id=user_id,
            id=Subquery(latest_test_per_sop.values('id')[:1])
        ).order_by('sop')

class ListTestByIdView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        sesi_id = self.kwargs.get('sesi_id')
        return Test.objects.filter(
            sesi=sesi_id,
            # user__is_staff=False
        )
    
class ListTestBySesiAndSOPView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        sesi_id = self.kwargs.get('sesi_id')
        sop = self.kwargs.get('sop')

        return Test.objects.filter(
            sesi=sesi_id,
            sop=sop,
            user__is_staff=False
        )

class UpdateTestView(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class DeleteTestView(generics.DestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class DeleteAllTestView(generics.GenericAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def delete(self, request, *args, **kwargs):
        total = Test.objects.count()
        Test.objects.all().delete()
        return Response(
            {
                "message": f"{total} Test berhasil dihapus"
            },
            status=status.HTTP_200_OK
        )


# DETAIL TEST
class CreateDetailTestView(generics.CreateAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer

class ListDetailTestView(generics.ListAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer

class ListDeatilTestByIdView(generics.ListAPIView):
    serializer_class = DetailTestSerializer

    def get_queryset(self):
        sesi_id = self.kwargs.get('test_id')
        return DetailTest.objects.filter(
            test=sesi_id,
        ).order_by('soal_sop')

class UpdateDetailTestView(generics.UpdateAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer

    def update(self, request, *args, **kwargs):
        test_id = request.data.get('test')
        soal_sop_id = request.data.get('soal_sop')
        nilai_baru = request.data.get('nilai')

        if not test_id:
            return Response({
                "message": "Field test wajib diisi"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not soal_sop_id:
            return Response({
                "message": "Field soal_sop wajib diisi"
            }, status=status.HTTP_400_BAD_REQUEST)

        if nilai_baru is None:
            return Response({
                "message": "Field nilai wajib diisi"
            }, status=status.HTTP_400_BAD_REQUEST)

        detail_test = get_object_or_404(
            DetailTest,
            test_id=test_id,
            soal_sop_id=soal_sop_id
        )

        detail_test.nilai = nilai_baru
        detail_test.save()

        serializer = self.get_serializer(detail_test)

        return Response({
            "message": "Nilai berhasil diupdate",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class DeleteDetailTestView(generics.DestroyAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer

class DeleteDetailTestBySOPView(APIView):
    def delete(self, request, sop_id):
        detail_tests = DetailTest.objects.filter(soal_sop_id=sop_id)

        if not detail_tests.exists():
            return Response(
                {"message": "Data DetailTest dengan SOP tersebut tidak ditemukan"},
                status=status.HTTP_404_NOT_FOUND
            )

        total_deleted = detail_tests.count()
        detail_tests.delete()

        return Response(
            {
                "message": "Data DetailTest berhasil dihapus",
                "total_deleted": total_deleted,
                "sop_id": sop_id
            },
            status=status.HTTP_200_OK
        )