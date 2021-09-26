from .serializers import CreatePrescriptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import errors
from . import services
from .models import Prescription
from django.db import transaction


@api_view(["POST"])
def create_prescription(request):
    serializer = CreatePrescriptionSerializer(data=request.data)
    if not serializer.is_valid():
        body, status_code = errors.MalformedRequestMessageError.create_response()
        return Response(body, status=status_code)

    request_json = serializer.validated_data
    # physician
    success, response = services.ServicePhysicians.make_request(
        uri_dict=request_json["physician"]
    )

    if not success:
        (
            body,
            status_code,
        ) = errors.PhysiciansNotAvailableMessageError.create_response()
        return Response(body, status=status_code)
    if response.status_code != 200:
        if response.status_code == 404:
            body, status_code = errors.PhysicianNotFoundMessageError.create_response()
        else:
            (
                body,
                status_code,
            ) = errors.PhysiciansNotAvailableMessageError.create_response()
        return Response(body, status=status_code)

    physician_json = response.json()
    # clinic
    success, response = services.ServiceClinics.make_request(
        uri_dict=request_json["clinic"]
    )
    clinic_json = {}
    if success and response.status_code == 200:
        clinic_json = response.json()
    # patient
    success, response = services.ServicePatients.make_request(
        uri_dict=request_json["patient"]
    )
    if not success:
        (
            body,
            status_code,
        ) = errors.PatientsNotAvailableMessageError.create_response()
        return Response(body, status=status_code)

    if response.status_code != 200:
        if response.status_code == 404:
            body, status_code = errors.PatientNotFoundMessageError.create_response()
        else:
            (
                body,
                status_code,
            ) = errors.PatientsNotAvailableMessageError.create_response()
        return Response(body, status=status_code)
    patient_json = response.json()

    try:
        with transaction.atomic():
            prescription = Prescription.objects.create(
                clinic_id=clinic_json.get("id"),
                physician_id=physician_json["id"],
                patient_id=physician_json["id"],
                text=request_json["text"],
            )
            # metric
            metric_json = {
                "physician_id": physician_json["id"],
                "physician_name": physician_json["name"],
                "physician_crm": physician_json["crm"],
                "patient_id": patient_json["id"],
                "patient_name": patient_json["name"],
                "patient_email": patient_json["email"],
                "patient_phone": patient_json["phone"],
                "prescription_id": prescription.id,
            }
            if clinic_json:
                metric_json["clinic_id"] = clinic_json["id"]
                metric_json["clinic_name"] = clinic_json["name"]

            success, response = services.ServiceMetrics.make_request(
                body_dict=metric_json
            )
            if not success or response.status_code != 201:
                raise Exception("Metrics service unavailable")
            prescription.metric_id = response.json()["id"]
            prescription.save(update_fields=["metric_id"])
    except:
        body, status_code = errors.MetricsNotAvailableMessageError.create_response()
        return Response(body, status=status_code)
    response_json = {
        "data": {
            "id": prescription.id,
            "clinic": {"id": prescription.clinic_id},
            "physician": {"id": prescription.physician_id},
            "patient": {"id": prescription.patient_id},
            "text": prescription.text,
            "metric": {"id": prescription.metric_id},
        }
    }
    return Response(
        response_json,
        status=status.HTTP_201_CREATED,
    )
