from django.urls import path
from .views import create_prescription

urlpatterns = [
    path("v1/prescriptions", create_prescription),
]
