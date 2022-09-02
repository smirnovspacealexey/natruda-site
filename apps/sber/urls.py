from django.urls import path

from . import backend
from . import views

urlpatterns = [
    path('test-pay/', views.test, name='test'),
    path('successful-payment/', views.successful_payment, name='successful_payment'),
    path('failed-payment/', views.failed_payment, name='failed_payment'),
]

