from django.contrib import admin
from django.urls import path
from Laptop import views
from Laptop.views import CreateCheckoutSessionView,SuccessView,stripe_webhook

app_name = "Laptop"


urlpatterns = [
    path("", views.listProduct,name='startpage'),
    path('load-more-products/', views.load_more_products, name='load_more_products'),
    path("filter_data",views.filter_data,name='filteration'),
    path("detail_product/<int:product_id>",views.product_detail,name='detail_view'),
    path("update/<int:product_id>",views.update_view,name='update_view'),
    
    path('create-checkout-session/<int:id>/',CreateCheckoutSessionView.as_view(),name="create-checkout-session"),
    path('success/',SuccessView.as_view(),name='success'),
    path("stripe_webhooks/",stripe_webhook,name='stripe-webhook'),
]
