from django.contrib import admin
from Laptop.models import product_line,Laptop,Product_image
from django.contrib import admin
from django.forms import Media

class YourModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',),  # Path to your custom CSS file
        }

class image_Admin(admin.ModelAdmin):
    list_display = ('id','image_tag','product')
    
 
  
admin.site.register(product_line,YourModelAdmin)
admin.site.register(Laptop)
admin.site.register(Product_image,image_Admin)

admin.site.site_header = "Dell Technologies"