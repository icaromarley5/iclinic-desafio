from rest_framework import serializers


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class CreatePrescriptionSerializer(serializers.Serializer):
    clinic = IdSerializer()
    physician = IdSerializer()
    patient = IdSerializer()
    text = serializers.CharField()
