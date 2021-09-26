from django.urls import path
from .views import create_prescription

urlpatterns = [
    path("prescriptions/", create_prescription),
]
