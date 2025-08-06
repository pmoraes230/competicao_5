from django.shortcuts import render
from home.views import get_user_profile

# Create your views here.
def validador(request):
    context = get_user_profile(request)
    return render(request, "validador.html", context)