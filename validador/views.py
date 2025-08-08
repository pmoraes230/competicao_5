from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models

# Create your views here.
def validador(request):
    context = get_user_profile(request)
    if request.method == 'POST':
        code_input = request.POST.get("code")
        if not code_input:
            messages.info(request, "Insira um código no campo.")
            return redirect("totem")
        
        try:
            id_ticket = models.Ingresso.objects.get(id_ingresso=code_input)
            if id_ticket.status == "validado":
                messages.info(request, "Ingresso já validado, tente outro ingresso.")
                return redirect("totem")
            elif id_ticket.status == "cancelado":
                messages.info(request, "Ingresso ingresso cancelado.")
                return redirect("totem")
            elif id_ticket.status == "emitido":
                id_ticket.status = "validado"
                id_ticket.save()
                messages.success(request, "Ingresso válidado com sucesso.")
                return redirect("totem")
            else:
                messages.error(request, "Ingresso inválido.")
                return redirect("totem")
                
        except models.Ingresso.DoesNotExist:
            messages.error(request, "Ingresso não encontrado")
            return redirect("totem")
        
    return render(request, "validador.html", context)