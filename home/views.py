from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from django.utils import timezone
from datetime import datetime
import uuid
from . import models
from django.shortcuts import get_object_or_404
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.
def get_user_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = models.Usuario.objects.select_related('perfil').get(id=user_id)
            return {
                'user_id': user.id,
                'user_name': user.nome,
                'user_role': user.perfil.nome,
                'is_authenticated': True
            }
        except models.Usuario.DoesNotExist:
            return {'user_name': '', 'is_authenticated': False}
    return {'user_name': '', 'is_authenticated': False}

def login(request):
    if request.method == 'GET':
        return render(request, "login/login.html")

    if request.method == 'POST':
        login_user = request.POST.get("login")
        password = request.POST.get("password")
        
        if not all([login_user, password]):
            messages.info(request, "Não pode mandar campos vazio.")
            return redirect('login')
            
        try:
            if models.Usuario.objects.filter(email=login_user).first() or models.Usuario.objects.filter(cpf=login_user).first():
                user = models.Usuario.objects.filter(email=login_user).first() or models.Usuario.objects.filter(cpf=login_user).first()
                if check_password(password, user.senha):
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.nome
                    request.session['user_role'] = user.perfil.nome
                    
                    messages.success(request, f"Bem vindo {user.nome} ao music hall")
                    if user.perfil.nome == "Totem":
                        return redirect("totem")
                    return redirect("home")
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return redirect('login')
        
def view_logout(request):
    logout(request)
    messages.success(request, "Você saiu do sistema")
    return redirect('login') 
       
def home(request):
    context = get_user_profile(request)
    context['events'] = models.Evento.objects.all()
    return render(request, "home/home.html", context)

def list_user(request):
    context = get_user_profile(request)
    context['users'] = models.Usuario.objects.all()
    
    return render(request, "users/list_user.html", context)

def register_user(request):
    context = get_user_profile(request)
    context['profiles'] = models.Perfil.objects.all()
    
    if request.method == "POST":
        name_user = request.POST.get("name")
        email_user = request.POST.get("email")
        cpf_user = request.POST.get("cpf")
        profile_user = request.POST.get("profile")
        password_user = request.POST.get("password")
        password_confirmation = request.POST.get("password2")
        
        if not all([name_user, email_user, cpf_user, profile_user, password_user, password_confirmation]):
            messages.info(request, "Todos os campos são obrigatórios.")
            return redirect("register_user")
                    
        if models.Usuario.objects.filter(cpf=cpf_user).exists():
            messages.info(request, "CPF já cadastrado.")
            return redirect("register_user")
            
        if models.Usuario.objects.filter(email=email_user).exists():
            messages.info(request, "Email já cadastrado.")
            return redirect("register_user")
            
        if password_user != password_confirmation:
            messages.info(request, "Senhas não são iguais.")
            return redirect("register_user")
        
        try:
            profile = models.Perfil.objects.get(id=profile_user)
        except models.Perfil.DoesNotExist:
            messages.error(request, "Perfil não encontrado")    
            return redirect("register_user")
        
        try:
            heshers_password = make_password(password_user)
            
            new_user = models.Usuario.objects.create(
                nome=name_user,
                email=email_user,
                cpf=cpf_user,
                senha=heshers_password,
                perfil=profile
            )
            new_user.full_clean()
            new_user.save()
            
            messages.success(request, f"Usuário {new_user.nome} cadastrado com sucesso.")
            return redirect("list_user")
            
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar novo usuario: {str(ve)}")
            return redirect("register_user")
        
    return render(request, "users/register_user.html", context)

def update_user(request, id_user):
    context = get_user_profile(request)
    try:
        user = models.Usuario.objects.get(id=id_user)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado")
        return redirect("upadate_user", id_user=id_user)
    
    if request.method == "POST":
        name_user = request.POST.get("name")
        email_user = request.POST.get("email")
        cpf_user = request.POST.get("cpf")
        profile_user = request.POST.get("profile")
        
        if not all([name_user, email_user, cpf_user, profile_user]):
            messages.info(request, "Todos os campos são obrigatórios.")
            return redirect("upadate_user", id_user=id_user)
                    
        if models.Usuario.objects.filter(cpf=cpf_user).exclude(id=id_user).exists():
            messages.info(request, "CPF já cadastrado.")
            return redirect("upadate_user", id_user=id_user)
            
        if models.Usuario.objects.filter(email=email_user).exclude(id=id_user).exists():
            messages.info(request, "Email já cadastrado.")
            return redirect("upadate_user", id_user=id_user)
        
        try:
            profile = models.Perfil.objects.get(id=profile_user)
        except models.Perfil.DoesNotExist:
            messages.error(request, "Perfil não encontrado")    
            return redirect("upadate_user", id_user=id_user)
        
        try:
            user.nome = name_user
            user.email = email_user
            user.cpf = cpf_user
            user.perfil = profile
            
            user.full_clean()
            user.save()
            
            messages.success(request, f"Cadastro de {user.nome} atualizado com sucesso.")
            return redirect("list_user")
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar o cadastro de {user.nome}: {str(ve)}")
    
    context.update({
        'user': user,
        'profiles': models.Perfil.objects.all()
    })
    return render(request, "users/update_user.html", context)

def delete_user(request, id_user):
    try:
        user = models.Usuario.objects.get(id=id_user)
        if request.method == "POST":
            user.delete()
            messages.success(request, "Usuário deletado com sucesso.")
            return redirect("list_user")
        context = {
            'user': user,
            **get_user_profile(request)
        }
        return render(request, "users/delete_user.html", context)
    except models.Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado")
        return redirect("list_user")
    
def deteils_event(request, id_event):
    context = get_user_profile(request)
    try:
        event = models.Evento.objects.get(id=id_event)
        setor = models.Setor.objects.filter(evento=event)
        client = None
        client_search = []
        
        if request.method == "POST" and "search_names" in request.POST:
            search = request.POST.get("search_name", "").strip()
            if search:
                client_search = models.Cliente.objects.filter(
                    Q(nome__icontains=search)
                )[:10]
                if not client_search:
                    messages.info(request, f"Nenhum cliente encontrado para o nome {search}")
                else:
                    messages.success(request, f"{client_search.count()} cliente(s) encontrado(s).")
            else: 
                messages.error(request, "Digite um nome para pesquisa")

        if request.method == "POST" and "client_select" in request.POST:
            client_id = request.POST.get("client_id")
            request.session['client'] = client_id
            try:
                client = models.Cliente.objects.get(id=client_id)
                messages.success(request, f"Cliente {client.nome} selecionado")
            except models.Cliente.DoesNotExist:
                messages.error(request, "Cliente não encontrado")

        # Atualizar o contexto com as variáveis necessárias
        context.update({
            'events': event,
            'client_search': client_search,
            'client': client,
            'setors': setor,
        })
        
        return render(request, "events/deteils_event.html", context)
        
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado.")
        return redirect("home")
    
def buy_ticket(request, id_event):
    context = get_user_profile(request)
    try:
        event = models.Evento.objects.get(id=id_event)
        setor = models.Setor.objects.filter(evento=event)
        client = None
        
        if request.method == "POST" and "buy_ticket" in request.POST:
            client_id = request.session.get("client")
            if not client_id:
                messages.info(request, "Por favor, selecione um cliente")
                return redirect("deteils_event", id_event=id_event)
            try:
                client = models.Cliente.objects.get(id=client_id)
            except models.Cliente.DoesNotExist:
                messages.error(request, "Cliente não encontrado")
                return redirect("deteils_event", id_event=id_event)
            
            setor_form = request.POST.get("setor")
            amount = int(request.POST.get("amount", 0))
            
            if not setor_form:
                messages.info(request, "Por favor, escolha um setor")
                return redirect("deteils_event", id_event=id_event)
            
            try:
                setor_event = models.Setor.objects.get(id=setor_form)
            except models.Setor.DoesNotExist:
                messages.error(request, "Setor não encontrado")
                return redirect("deteils_event", id_event=id_event)
            
            if amount == 0:
                messages.info(request, "Por favor, Escolha a quantidade de ingressos")
            elif amount > 10:
                messages.info(request, "O máximo de ingresso é 10 por cada cliente")
            else:
                tickets = []
                for _ in range(amount):
                    ticket = models.Ingresso.objects.create(
                        cliente=client,
                        evento=event,
                        setor=setor_event,
                        id_ingresso=str(uuid.uuid4()),
                        data_emissao=timezone.now(),
                        status="emitido"
                    )
                    tickets.append(ticket)
                    setor_event.quantidade_ingresso -= 1
                    setor_event.save()
                    
                    del request.session['client']
                    messages.success(request, "Ingressos gerado")
                    return redirect("deteils_event", id_event=id_event)
                
        context.update({
            'events': event,
            'client': client,
            'setor': setor,
        })
        
        return render(request, "events/deteils_event.html", context)
        
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado.")
        return redirect("home")
    
def register_event(request):
    context = get_user_profile(request)
    if request.method == "POST":
        name_event = request.POST.get("name")
        limit_event = request.POST.get("limit_peaple")
        image_event = request.FILES.get("image")
        datetime_event = request.POST.get("datetime")
        describle_event = request.POST.get("describle")
        
        
        if not all([name_event, limit_event, image_event, datetime_event, describle_event]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_event")
        
        native_datetime = datetime.strptime(datetime_event, "%Y-%m-%dT%H:%M")
        aware_datetime = timezone.make_aware(native_datetime)
            
        if models.Evento.objects.filter(data=aware_datetime).exists():
            messages.info(request, "Data e horário já reservado a um outro evento.")
            return redirect("register_event")
        
        user_id = request.session.get("user_id")
        try:
            user = models.Usuario.objects.get(id=user_id)
        except models.Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("register_event")
        
        try:
            new_event = models.Evento.objects.create(
                nome=name_event,
                capacidade_pessoas=limit_event,
                imagem=image_event,
                descricao=describle_event,
                data=aware_datetime,
                usuario=user
            )
            
            new_event.full_clean()
            new_event.save()
            
            messages.success(request, F"Evento {new_event.nome} criado com sucesso.")
            return redirect("home")
        except ValueError as ve:
            messages.error(request, f"Erro ao cadastrar evento: {str(ve)}")
        
    return render(request, "events/register_event.html", context)

def update_event(request, id_event):
    context = get_user_profile(request)
    try:
        event = models.Evento.objects.get(id=id_event)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("home")
    
    if request.method == "POST":
        name_event = request.POST.get("name")
        limit_event = request.POST.get("limit_peaple")
        image_event = request.FILES.get("image")
        datetime_event = request.POST.get("datetime")
        describle_event = request.POST.get("describle")
        
        if not all([name_event, limit_event, datetime_event, describle_event]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("update_event", id_event=id_event)
        
        native_datetime = datetime.strptime(datetime_event, '%Y-%m-%dT%H:%M')
        aware_datetime = timezone.make_aware(native_datetime)
        
        if models.Evento.objects.filter(data=aware_datetime).exclude(id=id_event).exists():
            messages.info(request, "Data e horário já reservado a um outro evento.")
            return redirect("register_event")
        
        try:
            event.nome = name_event
            event.capacidade_pessoas = limit_event
            if image_event:
                event.imagem = image_event
            event.data = datetime_event
            event.descricao = describle_event
            
            event.full_clean()
            event.save()
            
            messages.success(request, f"Evento {event.nome} atualizado com sucesso.")
            return redirect("deteils_event", id_event=id_event)
        except ValueError as ve:
            messages.error(request, f"Erro ao atualizar evento: {str(ve)}")
    
    context['events'] = event
    return render(request, "events/update_event.html", context)

def delete_event(request, id_event):
    try:
        event = models.Evento.objects.get(id=id_event)
        if request.method == "POST":
            event.delete()
            messages.success(request, "Evento apagado do sistema")
            return redirect("home")
        context = {
            "events": event,
            **get_user_profile(request)
        }
        return render(request, "events/delete_event.html", context)
    except models.Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("home")
    
def list_setor(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id=id_event)
    setor = models.Setor.objects.filter(evento=event)
    
    context['setors'] = setor
    return render(request, "setor/list_setor.html", context)

def register_setor(request):
    context = get_user_profile(request)
    context['events'] = models.Evento.objects.all().order_by("-id")
    
    if request.method == "POST":
        name_setor = request.POST.get("name")
        qtd_ticket = request.POST.get("tickets")
        price_event = request.POST.get("price")
        id_event = request.POST.get("profile")
        
        if not all([name_setor, qtd_ticket, price_event, id_event]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("register_setor")
        
        try:
            event = models.Evento.objects.get(id=id_event)
        except models.Evento.DoesNotExist:
            messages.info(request, "Nenhum evento encontrado")
            return redirect("register_setor")

        try:
            new_setor = models.Setor.objects.create(
                nome=name_setor,
                quantidade_ingresso=qtd_ticket,
                preco=price_event,
                evento=event
            )
            
            new_setor.full_clean()
            new_setor.save()
            
            messages.success(request, f"Setor {new_setor.nome} criado com sucesso ao evento {new_setor.evento.nome}.")
            return redirect("list_setores")
        except ValueError as ve:
            messages.error(request, f"Erro ao criar novo setor: {str(ve)}")
            return redirect("register_setor")
    
    return render(request, "setor/register_setor.html", context)

def update_setor(request, id_setor):
    context = get_user_profile(request)
    try:
        setor = models.Setor.objects.get(id=id_setor)
    except models.Setor.DoesNotExist:
        messages.error(request, "Setor não encontrado")
        return redirect("update_setor", id_setor=id_setor)
    
    if request.method == "POST":
        name_setor = request.POST.get("name")
        qtd_ticket = request.POST.get("tickets")
        price_event = request.POST.get("price")
        id_event = request.POST.get("profile")
        
        if not all([name_setor, qtd_ticket, price_event, id_event]):
            messages.info(request, "Todos os campos são obrigatórios")
            return redirect("update_setor", id_setor=id_setor)
        
        try:
            event = models.Evento.objects.get(id=id_event)
        except models.Evento.DoesNotExist:
            messages.info(request, "Nenhum evento encontrado")
            return redirect("update_setor", id_setor=id_setor)
        
        try:
            setor.nome = name_setor
            setor.quantidade_ingresso = qtd_ticket
            setor.preco = price_event
            setor.evento = event
            
            setor.full_clean()
            setor.save()
            
            messages.success(request, f"Setor {setor.nome} atualizado")
            return redirect("home")
        except ValueError as ve:
            messages.error(request, f"Erro ao editar setor: {str(ve)}")
            return redirect("update_setor", id_setor=id_setor)
    
    context.update({
        'setor': setor,
        'events': models.Evento.objects.all().order_by("-id")
    })
    return render(request, "setor/update_setor.html", context)

def delete_setor(request, id_setor):
    try:
        setor = models.Setor.objects.get(id=id_setor)
        if request.method == "POST":
            setor.delete()
            messages.success(request, "Setor apagado do sistema.")
        context = {
            'setor': setor,
            **get_user_profile(request)
        }
        return render(request, "setor/delete_setor.html", context)
    except models.Setor.DoesNotExist:
        messages.error(request, "Setor não encontrado.")
        return redirect("home")
    
def tickets_generate(request, id_event):
    context = get_user_profile(request)
    event = models.Evento.objects.get(id=id_event)
    tickets = models.Ingresso.objects.filter(evento=event)
    
    context.update({
        'events': event,
        'tickets': tickets
    })
    
    return render(request, "events/tickets.html", context)

def export_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(models.Ingresso, id_ingresso=ticket_id)
    
    html = render_to_string('events/ticket_pdf.html', {'ticket': ticket})
    
    configuration = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
    }
    
    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=configuration)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ingresso_{ticket_id}.pdf"'
        response.write(pdf)
        
        return response
    except Exception as e:
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)