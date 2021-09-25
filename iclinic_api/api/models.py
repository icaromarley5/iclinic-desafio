from django.db import models

# Create your models here.


class Prescription(models.Model):
    id = models.BigAutoField(primary_key=True)
    clinic_id = models.PositiveIntegerField(db_column="clinic_id", null=True)
    physician_id = models.PositiveIntegerField(db_column="physician_id")
    patient_id = models.PositiveIntegerField(db_column="patient_id")
    text = models.TextField()
    metric_id = models.UUIDField(null=True)

    class Meta:
        db_table = "tb_prescription"
