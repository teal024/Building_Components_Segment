from django.urls import path
from backend.views import GetImg

urlpatterns = [
    path('saveimage/', GetImg.as_view({'post': 'save_image'})),
]
