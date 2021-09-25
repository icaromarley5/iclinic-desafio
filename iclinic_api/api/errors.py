from rest_framework import status


class MessageError:
    @classmethod
    def create_response(cls):
        body = {
            "error": {
                "message": cls.message,
                "code": cls.code,
            }
        }
        status = cls.status_code
        return body, status


class MalformedRequestMessageError(MessageError):
    message = "malformed request"
    code = "01"
    status_code = status.HTTP_400_BAD_REQUEST


class PatientNotFoundMessageError(MessageError):
    message = "patient not found"
    code = "02"
    status_code = status.HTTP_404_NOT_FOUND


class PhysicianNotFoundMessageError(MessageError):
    message = "physician not found"
    code = "03"
    status_code = status.HTTP_404_NOT_FOUND


class MetricsNotAvailableMessageError(MessageError):
    message = "metrics service not available"
    code = "04"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class PhysiciansNotAvailableMessageError(MessageError):
    message = "physicians service not available"
    code = "05"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class PatientsNotAvailableMessageError(MessageError):
    message = "patients service not available"
    code = "06"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
