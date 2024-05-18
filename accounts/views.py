from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError
from django.db.models import Q  
from .models import Usuario


def register_municipe(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            if User.objects.filter(username=email).exists():
                raise ValidationError("Este e-mail já está em uso.")
            else:
                User.objects.create_user(username=email, password=password)
        except ValidationError as e:
            context['error'] = str(e)
    return render(request, 'register_municipe.html', context)


def login_municipe_view(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']
        user = authenticate(request, username=email, password=password) 
        if user is not None:
            login(request, user)
            return redirect('painel_solicitacoes_municipe')  # Redireciona para a página 'painel_solicitacoes_municipe'
    return render(request, 'login_municipe.html')

def painel_solicitacoes_municipe(request):
    return render(request, 'painel_solicitacoes_municipe.html')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



def login_prefeitura(request):
    return render(request, 'login_prefeitura.html')

def login_prefeitura(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.username == 'prefeitura1':
                login(request, user)
                return redirect('painel_solicitacoes_prefeitura')
            else:
                return render(request, 'login_prefeitura.html', {'error': 'Senha ou usuário incorretos'})
        else:
            return render(request, 'login_prefeitura.html', {'error': 'Senha ou usuário incorretos'})
    return render(request, 'login_prefeitura.html')

def painel_solicitacoes_prefeitura(request):
    return render(request, 'painel_solicitacoes_prefeitura.html')