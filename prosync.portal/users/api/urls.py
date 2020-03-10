from users.api.views import api_detail_consumer_view, api_consumer_register_view, api_product_check_view, ConsumerView

from django.urls import path

app_name = 'users'

urlpatterns = [

    # consumer links
    path('con/', ConsumerView.as_view()),
    path('<int:id>/', api_detail_consumer_view),
    path('con_register/', api_consumer_register_view, name='con_register'),
    path('pro_check/', api_product_check_view, name='product_check'),
]
