from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [

    # USER
    path('login/', LoginView.as_view(), name='api_login'),
    path('user/register/', RegisterUserView.as_view()),
    path('user/me/', UserMeView.as_view()),
    path('user/list/', UserListView.as_view()),
    path('user/list/dosen/', UserDosenListView.as_view()),
    path('user/list/mahasiswa/', UserMahasiswaListView.as_view()),
    path('user/delete/<int:pk>/', DeleteUserView.as_view()),
    path('user/delete/all/', DeleteAllUserView.as_view()),

    # JENIS SOP
    path('jenis-sop/create/', CreateJenisSOPView.as_view()),
    path('jenis-sop/list/', ListJenisSOPView.as_view()),
    
    # SOAL SOP
    path('soal-sop/create/', CreateSoalSOPView.as_view()),
    path('soal-sop/list/', ListSoalSOPView.as_view()),
    path('soal-sop/list/<str:nama_sop>/', ListSoalSOPByNamaView.as_view(), name='list-soal-sop-by-nama'),
    path('soal-sop/update/<int:pk>/', UpdateSoalSOPView.as_view()),
    path('soal-sop/delete/<int:pk>/', DeleteSoalSOPView.as_view()),

    # DETAIL SOP
    path('detail-sop/create/', CreateDetailSOPView.as_view()),
    path('detail-sop/list/', ListDetailSOPView.as_view()),
    path('detail-sop/<int:id_sop>/', ListDetailSOPBySopView.as_view()),
    path('detail-sop/update/<int:pk>/', UpdateDetailSOPView.as_view()),
    path('detail-sop/delete/<int:pk>/', DeleteDetailSOPView.as_view()),

    # SESI TEST
    path('sesi/create/', CreateSesiTestView.as_view()),
    path('sesi/update/<int:id>/', UpdateSesiUjianView.as_view()),
    path('sesi/list/', ListSesiUjianView.as_view()),
    path('sesi/delete/all/', DeleteAllSesiView.as_view()),

    # TEST
    path('test/create/', CreateTestView.as_view()),
    path('test/list/', ListTestView.as_view()),
    path('test/list/<int:sesi_id>/', ListTestByIdView.as_view()),
    path('test/sesi/<int:sesi_id>/sop/<str:sop>/', ListTestBySesiAndSOPView.as_view()),
    path('test/list/user/<int:user_id>/', ListTestByUserView.as_view()),
    path('test/list/last/', ListLatestTestView.as_view()),
    path('test/update/<int:pk>/', UpdateTestView.as_view()),
    path('test/delete/<int:pk>/', DeleteTestView.as_view()),
    path('test/delete/all/', DeleteAllTestView.as_view()),

    # DETAIL TEST
    path('detail-test/create/', CreateDetailTestView.as_view()),
    path('detail-test/list/', ListDetailTestView.as_view()),
    path('detail-test/list/<int:test_id>/', ListDeatilTestByIdView.as_view()),
    path('detail-test/update/', UpdateDetailTestView.as_view()),
    path('detail-test/delete/<int:pk>/', DeleteDetailTestView.as_view()),
]