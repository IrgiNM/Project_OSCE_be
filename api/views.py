from rest_framework import generics
from .models import *
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token



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
        )

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

class ListDetailSOPView(generics.ListAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

class UpdateDetailSOPView(generics.UpdateAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer

class DeleteDetailSOPView(generics.DestroyAPIView):
    queryset = DetailSoalSOP.objects.all()
    serializer_class = DetailSoalSOPSerializer


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

class ListTestByIdView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        sesi_id = self.kwargs.get('sesi_id')
        return Test.objects.filter(
            sesi=sesi_id,
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

class UpdateDetailTestView(generics.UpdateAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer

class DeleteDetailTestView(generics.DestroyAPIView):
    queryset = DetailTest.objects.all()
    serializer_class = DetailTestSerializer