from django.urls import path
from backend.views import GetImg
from backend.views import UploadCsv

urlpatterns = [
    path('saveimage/', GetImg.as_view({'post': 'save_image'})),
    path('savecsv/', UploadCsv.as_view({'post':'save_csv'})),
]
