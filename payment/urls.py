from django.urls import include, path

from . import views

app_name = "payment"

urlpatterns = [
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]
