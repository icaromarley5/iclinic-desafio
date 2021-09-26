from django.urls import path
from .views import create_prescription
from django.views.generic import TemplateView

urlpatterns = [
    path("prescriptions/", create_prescription),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="swagger.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
]
