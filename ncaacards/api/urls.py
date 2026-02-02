from django.urls import re_path
from ncaacards.api import views

urlpatterns = [
    re_path(r'^make_market$', views.make_market),
    re_path(r'^positions$', views.positions),
    re_path(r'^executions$', views.executions),
    re_path(r'^open_orders$', views.open_orders),
    re_path(r'^cancel_order$', views.cancel_order),
    re_path(r'^place_order$', views.place_order),
    re_path(r'^my_markets$', views.my_markets),
    re_path(r'^market_data$', views.market_data),
    re_path(r'^get_book$', views.get_book),
]
