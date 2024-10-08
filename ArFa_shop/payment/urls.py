from django.urls import path
from . import views

from django.contrib import admin
from azbankgateways.urls import az_bank_gateways_urls
from .views import go_to_gateway_view, callback_gateway_view

urlpatterns = [
    path("bankgateways/", az_bank_gateways_urls()),
    path('go_to_gateway/', go_to_gateway_view, name='goToGateway'),
    path('callback-gateway/', callback_gateway_view, name='callback-gateway'),
]