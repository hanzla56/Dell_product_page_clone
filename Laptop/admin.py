from django.contrib import admin
from Laptop.models import product_line,Laptop,Product_image



class image_Admin(admin.ModelAdmin):
    list_display = ('id','image_tag','product')
    
 
  
admin.site.register(product_line)
admin.site.register(Laptop)
admin.site.register(Product_image,image_Admin)