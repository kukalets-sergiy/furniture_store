from django.contrib.auth.decorators import login_required
from carts.models import Cart
from django.shortcuts import render




@login_required
def payment_selection(request):
    return render(request, "payment/payment_selection.html", {})
