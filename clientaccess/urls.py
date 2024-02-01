from django.urls import re_path

from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('add_item', views.add_item),
    re_path('all_items', views.all_items),
    re_path('see_item', views.see_item),
    re_path('add_to_cart', views.add_to_cart),
    re_path('my_cart', views.my_cart),
    re_path('remove_from_cart', views.remove_from_cart),
    re_path('order', views.order)
]