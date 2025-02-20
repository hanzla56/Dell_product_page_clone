from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location=settings.MEDIA_ROOT)
from django.utils.safestring import mark_safe
from io import BytesIO
from PIL import Image

from secondapp.models import User_Data


#Now I am creating models here
    
class product_line(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Laptop(models.Model):
    name = models.CharField(max_length=30)
    model = models.IntegerField()
    price = models.IntegerField()
    short_processor_details = models.CharField(max_length=30)
    full_processor_details = models.CharField(max_length=100)
    graphics = models.CharField(max_length=50)
    os = models.CharField(max_length=40)
    memory = models.CharField(max_length=20)
    display = models.FloatField()
    product_line = models.ForeignKey(product_line,on_delete=models.CASCADE)
    main_img = models.ImageField()
    
    def __str__(self):
        return self.name
    
    
class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Laptop, null=True,blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, null=True,blank=True, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.product.name
    
    
    
class Product_image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='p_image')
    
      
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'
    
#This is my comment for checking if any change occurs in main branch 