from django.contrib import admin
from django.urls import path
from Laptop import views

app_name = "Laptop"


urlpatterns = [
    path("", views.listProduct,name='startpage'),
    path('load-more-products/', views.load_more_products, name='load_more_products'),
    path("filter_data",views.filter_data,name='filteration'),
    path("detail_product/<int:product_id>",views.product_detail,name='detail_view'),
    path("update/<int:product_id>",views.update_view,name='update_view')
]
