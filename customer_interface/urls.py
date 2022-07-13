from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('meat/<str:category_slug>/', views.meat, name='meat'),
    path('basket', views.basket, name='basket'),
    path('content/<int:macroproduct_content_id>/', views.char, name='char'),
    path('content/char/', views.char_base, name='char_base'),
    path('contacts', views.contacts, name='contacts'),
    path('about', views.about, name='about'),
    path('confirm_order', views.create_order, name='confirm_order'),
    path('check_order', views.check_order, name='check_order'),
    path('check_order_ajax', views.check_order_ajax, name='check_order_ajax'),
    path('update_menu', views.update_menu, name='update_menu'),
]

