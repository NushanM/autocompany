from django.urls import re_path

from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('list_item', views.list_item),
    re_path('all_items', views.all_items),
    re_path('add_to_cart', views.add_to_cart),
    re_path('all_carts', views.all_carts),
    re_path('my_cart', views.my_cart),
    re_path('remove_item', views.remove_item),
    re_path('order', views.order)
]