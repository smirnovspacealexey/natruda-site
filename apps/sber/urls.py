from django.urls import path

from . import backend
from . import views

urlpatterns = [
    path('test/', views.test1, name='test1'),  # del me

    path('test-pay/', views.test, name='test'),
    path('successful-payment/', views.successful_payment, name='successful_payment'),
    path('failed-payment/', views.failed_payment, name='failed_payment'),
    path('sber/result', views.sber_result, name='sber-result'),
]

