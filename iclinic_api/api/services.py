import requests
from django.conf import settings
from django.core.cache import cache


class ServiceBase:
    @classmethod
    def build_uri(cls, uri_dict):
        uri = cls.uri
        for key, value in uri_dict.items():
            uri = uri.replace(f"%%{key}%%", f"{value}")
        return uri

    @classmethod
    def make_request(cls, uri_dict={}, body_dict=None):
        uri = cls.build_uri(uri_dict)
        response = cache.get(uri)
        if response:
            return True, response

        headers = {"Authorization": f"Bearer {cls.token}"}
        response = None
        for _ in range(cls.retries):
            try:
                response = getattr(requests, cls.method)(
                    uri, headers=headers, json=body_dict, timeout=cls.timeout
                )
            except requests.exceptions.ReadTimeout:
                pass

        success = False
        if response:
            if cls.cache_time:
                cache.set(uri, response, timeout=cls.cache_time)
            success = True
        return success, response


class ServicePhysicians(ServiceBase):
    uri = settings.PHYSICIANS_URL + "/physicians/%%id%%/"
    token = settings.PHYSICIANS_TOKEN
    timeout = settings.PHYSICIANS_TIMEOUT_SECONDS
    retries = settings.PHYSICIANS_RETRIES
    cache_time = settings.PHYSICIANS_CACHE_TTL_HOURS * 3600
    method = "get"


class ServiceClinics(ServiceBase):
    uri = settings.CLINICS_URL + "/clinics/%%id%%/"
    token = settings.CLINICS_TOKEN
    timeout = settings.CLINICS_TIMEOUT_SECONDS
    retries = settings.CLINICS_RETRIES
    cache_time = settings.CLINICS_CACHE_TTL_HOURS * 3600
    method = "get"


class ServicePatients(ServiceBase):
    uri = settings.PATIENTS_URL + "/patients/%%id%%/"
    token = settings.PATIENTS_TOKEN
    timeout = settings.PATIENTS_TIMEOUT_SECONDS
    retries = settings.PATIENTS_RETRIES
    cache_time = settings.PATIENTS_CACHE_TTL_HOURS * 3600
    method = "get"


class ServiceMetrics(ServiceBase):
    uri = settings.METRICS_URL + "/metrics/"
    token = settings.METRICS_TOKEN
    timeout = settings.METRICS_TIMEOUT_SECONDS
    retries = settings.METRICS_RETRIES
    cache_time = settings.METRICS_CACHE_TTL_HOURS * 3600
    method = "post"
