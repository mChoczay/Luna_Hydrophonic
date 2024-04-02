from django.db import models


class Customer(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class HydroponicSystem(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ph = models.FloatField()
    water_temperature = models.FloatField()
    TDS = models.FloatField()

    def __str__(self):
        return self.name + " " + str(self.customer)