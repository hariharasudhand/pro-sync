from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.index, name='index'),
    path('', views.success, name='success'),

    # add product links
    path('product/', views.product, name='product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('product/<int:id>/delete/', views.cancel_product, name='delete_product'),

    # batch links
    path('batch/', views.batch, name='batch'),
]

