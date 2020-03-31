from users.api import views
from django.urls import path

app_name = 'users'

urlpatterns = [

    # consumer links
    path('con/', views.ConsumerView.as_view()),
    path('<int:id>/', views.api_detail_consumer_view),
    path('con_register/', views.api_consumer_register_view, name='con_register'),
    path('pro_check/', views.api_product_check_view, name='product_check'),

    # retailer links
    path('ret_login/', views.api_retailer_login_view, name='retailer_login'),
]
