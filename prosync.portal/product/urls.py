from django.urls import path
from . import views

urlpatterns = [

    # add product links
    path('product/', views.product, name='product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('product/<int:id>/delete/', views.cancel_product, name='delete_product'),

    # batch links
    path('batch/', views.batch, name='batch'),
]
