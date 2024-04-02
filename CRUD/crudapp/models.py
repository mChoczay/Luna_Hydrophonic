from django.db import models


class HydroponicSystem(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    ph = models.FloatField()
    water_temperature = models.FloatField()
    TDS = models.FloatField()

    def __str__(self):
        return str(self.name)