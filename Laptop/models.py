from django.db import models


#Now I am creating models here
class product_line(models.Model):
    name = models.CharField(max_length=30)

class Laptop(models.Model):
    name = models.CharField(max_length=30)
    model = models.IntegerField()
    price = models.IntegerField()
    short_processor_details = models.CharField(max_length=30)
    full_processor_details = models.CharField(max_length=60)
    graphics = models.CharField(max_length=50)
    os = models.CharField(max_length=20)
    memory = models.CharField(max_length=20)
    display = models.FloatField()
    product_line = models.ForeignKey(product_line,on_delete=models.CASCADE)
    
    
class Images(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Laptop, on_delete=models.CASCADE)