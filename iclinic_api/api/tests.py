from django.test import TestCase
from .models import Prescription
from . import views
from unittest import mock
from rest_framework.test import APIRequestFactory
from .services import ServiceClinics


@mock.patch("api.views.services.ServiceMetrics")
@mock.patch("api.views.services.ServicePatients")
@mock.patch("api.views.services.ServiceClinics")
@mock.patch("api.views.services.ServicePhysicians")
class CreatePrescriptionsTestCase(TestCase):
    def test_success(self, physicians_mock, clinics_mock, patients_mock, metrics_mock):

        physicians_response_dict = {
            "id": 1,
            "name": "Ana Júlia Cardoso",
            "crm": "80385363",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=physicians_response_dict)
        response_mock.status_code = 200
        physicians_mock.make_request = mock.MagicMock(
            return_value=(True, response_mock)
        )

        clinics_response_dict = {"id": 1, "name": "Cardoso"}
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=clinics_response_dict)
        response_mock.status_code = 200
        clinics_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        patients_response_dict = {
            "id": 1,
            "name": "Yuri Porto",
            "email": "pintodavi-lucca@uol.com.br",
            "phone": "+55 (011) 6667 6061",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=patients_response_dict)
        response_mock.status_code = 200
        patients_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        metrics_response_dict = {
            "id": "046c8dbc-a320-4816-9fac-a8bdcdd4ead7",
            "clinic_id": clinics_response_dict["id"],
            "clinic_name": "Clínica A",
            "physician_id": physicians_response_dict["id"],
            "physician_name": "José",
            "physician_crm": "SP293893",
            "patient_id": patients_response_dict["id"],
            "patient_name": "Rodrigo",
            "patient_email": "rodrigo@gmail.com",
            "patient_phone": "(16)998765625",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=metrics_response_dict)
        response_mock.status_code = 201
        metrics_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        request_dict = {
            "clinic": {"id": clinics_response_dict["id"]},
            "physician": {"id": physicians_response_dict["id"]},
            "patient": {"id": patients_response_dict["id"]},
            "text": "Dipirona 1x ao dia",
        }
        factory = APIRequestFactory()
        request = factory.post(
            "/prescriptions",
            request_dict,
            format="json",
        )
        response = views.create_prescription(request)

        self.assertEqual(
            Prescription.objects.filter(pk=response.data["data"]["id"]).count(), 1
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "data": {
                    "id": response.data["data"]["id"],
                    "clinic": {"id": clinics_response_dict["id"]},
                    "physician": {"id": physicians_response_dict["id"]},
                    "patient": {"id": patients_response_dict["id"]},
                    "text": request_dict["text"],
                    "metric": {"id": metrics_response_dict["id"]},
                }
            },
        )

    def test_success_without_clinics(
        self, physicians_mock, clinics_mock, patients_mock, metrics_mock
    ):

        physicians_response_dict = {
            "id": 1,
            "name": "Ana Júlia Cardoso",
            "crm": "80385363",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=physicians_response_dict)
        response_mock.status_code = 200
        physicians_mock.make_request = mock.MagicMock(
            return_value=(True, response_mock)
        )

        patients_response_dict = {
            "id": 1,
            "name": "Yuri Porto",
            "email": "pintodavi-lucca@uol.com.br",
            "phone": "+55 (011) 6667 6061",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=patients_response_dict)
        response_mock.status_code = 200
        patients_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        response_mock = mock.MagicMock()
        response_mock.status_code = 500
        clinics_mock.make_request = mock.MagicMock(return_value=(False, response_mock))

        metrics_response_dict = {
            "id": "046c8dbc-a320-4816-9fac-a8bdcdd4ead7",
            "physician_id": physicians_response_dict["id"],
            "physician_name": "José",
            "physician_crm": "SP293893",
            "patient_id": patients_response_dict["id"],
            "patient_name": "Rodrigo",
            "patient_email": "rodrigo@gmail.com",
            "patient_phone": "(16)998765625",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=metrics_response_dict)
        response_mock.status_code = 201
        metrics_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        request_dict = {
            "clinic": {"id": 1},
            "physician": {"id": physicians_response_dict["id"]},
            "patient": {"id": patients_response_dict["id"]},
            "text": "Dipirona 1x ao dia",
        }
        factory = APIRequestFactory()
        request = factory.post(
            "/prescriptions",
            request_dict,
            format="json",
        )

        response = views.create_prescription(request)

        self.assertEqual(
            Prescription.objects.filter(pk=response.data["data"]["id"]).count(), 1
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsNone(
            Prescription.objects.get(pk=response.data["data"]["id"]).clinic_id
        )
        self.assertEqual(
            response.data,
            {
                "data": {
                    "id": response.data["data"]["id"],
                    "clinic": {"id": None},
                    "physician": {"id": physicians_response_dict["id"]},
                    "patient": {"id": patients_response_dict["id"]},
                    "text": request_dict["text"],
                    "metric": {"id": metrics_response_dict["id"]},
                }
            },
        )

    def test_error_physicians(
        self, physicians_mock, clinics_mock, patients_mock, metrics_mock
    ):
        physicians_mock.make_request = mock.MagicMock(
            return_value=(False, mock.MagicMock())
        )

        patients_response_dict = {
            "id": 1,
            "name": "Yuri Porto",
            "email": "pintodavi-lucca@uol.com.br",
            "phone": "+55 (011) 6667 6061",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=patients_response_dict)
        response_mock.status_code = 200
        patients_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        response_mock = mock.MagicMock()
        response_mock.status_code = 500
        clinics_mock.make_request = mock.MagicMock(return_value=(False, response_mock))

        metrics_response_dict = {
            "id": "046c8dbc-a320-4816-9fac-a8bdcdd4ead7",
            "physician_id": 1,
            "physician_name": "José",
            "physician_crm": "SP293893",
            "patient_id": patients_response_dict["id"],
            "patient_name": "Rodrigo",
            "patient_email": "rodrigo@gmail.com",
            "patient_phone": "(16)998765625",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=metrics_response_dict)
        response_mock.status_code = 201
        metrics_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        request_dict = {
            "clinic": {"id": 1},
            "physician": {"id": 1},
            "patient": {"id": patients_response_dict["id"]},
            "text": "Dipirona 1x ao dia",
        }
        factory = APIRequestFactory()
        request = factory.post(
            "/prescriptions",
            request_dict,
            format="json",
        )

        response = views.create_prescription(request)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.data,
            {"error": {"message": "physicians service not available", "code": "05"}},
        )

    def test_error_patients(
        self, physicians_mock, clinics_mock, patients_mock, metrics_mock
    ):

        physicians_response_dict = {
            "id": 1,
            "name": "Ana Júlia Cardoso",
            "crm": "80385363",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=physicians_response_dict)
        response_mock.status_code = 200
        physicians_mock.make_request = mock.MagicMock(
            return_value=(True, response_mock)
        )

        patients_mock.make_request = mock.MagicMock(
            return_value=(False, mock.MagicMock)
        )

        response_mock = mock.MagicMock()
        response_mock.status_code = 500
        clinics_mock.make_request = mock.MagicMock(return_value=(False, response_mock))

        metrics_response_dict = {
            "id": "046c8dbc-a320-4816-9fac-a8bdcdd4ead7",
            "physician_id": physicians_response_dict["id"],
            "physician_name": "José",
            "physician_crm": "SP293893",
            "patient_id": 1,
            "patient_name": "Rodrigo",
            "patient_email": "rodrigo@gmail.com",
            "patient_phone": "(16)998765625",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=metrics_response_dict)
        response_mock.status_code = 201
        metrics_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        request_dict = {
            "clinic": {"id": 1},
            "physician": {"id": physicians_response_dict["id"]},
            "patient": {"id": 1},
            "text": "Dipirona 1x ao dia",
        }
        factory = APIRequestFactory()
        request = factory.post(
            "/prescriptions",
            request_dict,
            format="json",
        )

        response = views.create_prescription(request)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.data,
            {"error": {"message": "patients service not available", "code": "06"}},
        )

    def test_success_without_clinics(
        self, physicians_mock, clinics_mock, patients_mock, metrics_mock
    ):

        physicians_response_dict = {
            "id": 1,
            "name": "Ana Júlia Cardoso",
            "crm": "80385363",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=physicians_response_dict)
        response_mock.status_code = 200
        physicians_mock.make_request = mock.MagicMock(
            return_value=(True, response_mock)
        )

        patients_response_dict = {
            "id": 1,
            "name": "Yuri Porto",
            "email": "pintodavi-lucca@uol.com.br",
            "phone": "+55 (011) 6667 6061",
        }
        response_mock = mock.MagicMock()
        response_mock.json = mock.MagicMock(return_value=patients_response_dict)
        response_mock.status_code = 200
        patients_mock.make_request = mock.MagicMock(return_value=(True, response_mock))

        response_mock = mock.MagicMock()
        response_mock.status_code = 500
        clinics_mock.make_request = mock.MagicMock(return_value=(False, response_mock))

        metrics_mock.make_request = mock.MagicMock(return_value=(False, mock.MagicMock))

        request_dict = {
            "clinic": {"id": 1},
            "physician": {"id": physicians_response_dict["id"]},
            "patient": {"id": patients_response_dict["id"]},
            "text": "Dipirona 1x ao dia",
        }
        factory = APIRequestFactory()
        request = factory.post(
            "/prescriptions",
            request_dict,
            format="json",
        )

        response = views.create_prescription(request)

        self.assertEqual(Prescription.objects.all().count(), 0)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.data,
            {"error": {"message": "metrics service not available", "code": "04"}},
        )


@mock.patch("api.views.services.requests")
@mock.patch("api.views.services.cache")
class CacheTestCase(TestCase):
    def test_set_cache(self, cache_mock, requests_mock):
        cache_mock.get = mock.MagicMock()

        requests_mock.get = mock.MagicMock()

        key = ServiceClinics.build_uri({"id": 1})
        ServiceClinics.make_request({"id": 1})

        self.assertIsNone(cache_mock.get.assert_called_once_with(key))
        self.assertEqual(requests_mock.get.call_count, 0)

    def test_get_cache(self, cache_mock, requests_mock):
        cache_mock.get = mock.MagicMock(return_value=None)
        cache_mock.set = mock.MagicMock()

        response_test = "teste"
        requests_mock.get = mock.MagicMock(return_value=response_test)
        ServiceClinics.make_request({"id": 1})
        key = ServiceClinics.build_uri({"id": 1})

        self.assertIsNone(cache_mock.get.assert_called_once_with(key))

        self.assertIsNone(
            cache_mock.set.assert_called_once_with(
                key, response_test, timeout=ServiceClinics.cache_time
            )
        )
