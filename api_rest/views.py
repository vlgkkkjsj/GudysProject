from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse,HttpResponseForbidden 
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.middleware.csrf import get_token
from django.contrib import messages
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
# from django.views.decorators.csrf import csrf_exempt


#validação pra ver se o maluco é autorizado

def is_admin(user):
    return user.is_authenticated and user.is_admin

def is_superuser(user):
    return user.is_superuser

def is_staff(user):
    return user.is_authenticated and not user.is_superuser and not user.is_admin

# Verificação de redirecionamento de cada usuario com as devidas permissoes

@login_required
@user_passes_test(is_superuser)
def sideSuperUser(request):
    return render(request, 'SuPages/superuser.html')

@login_required
@user_passes_test(is_admin)
def sideAdmin(request):
    return render(request,'admin.html')

@login_required
@user_passes_test(is_staff)
def sideStaff(request):
    return render(request,'userCommon.html')

# views e mais views (desgraça do krlh)

#td essa porra faz validação e assegura q o user ta seguro no login
def home(request):
    users = User.objects.all()
    cookie_value = request.COOKIES.get('user_nickname', 'Visitante')
    return render(request, "login.html", {"users": users, "cookie_value": cookie_value, "csrf_token": get_token(request)})

def homeLogin(request):
    if request.user.is_authenticated:
        return redirect('homeLog')
    else:
        return redirect('login')
    
@login_required
def homeLog(request):
    user = request.user 
    
    if user.is_superuser:
        return redirect('sideSuperUser')
    if user.is_admin:
        return redirect('sideAdmin')
    if user.is_staff:
        return redirect('sideStaff')
    
    return HttpResponse("Acesso negado")  # Retorne uma resposta adequada


@login_required
def home_dashboard(request):
    return redirect('listar')

def logar(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            response = redirect('homeLog')
            response.set_cookie('user_nickname', user.username, max_age=3600)  # Define o cookie com o 
            return response
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

@login_required
def listar(request):
    users = User.objects.all()
    query = request.GET.get('q')

    if query:
        users = users.filter(Q(name__icontains=query))
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'listar.html', context)
# Esse caralho, vai cadastrar os usuarios

#view cadastrar
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_admin) # Apenas super Usuarios e Admins tem acesso
def cadastrar(request):
    users = User.objects.all()
    return render(request, "cadastro.html", {"users": users})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_admin) # Apenas super Usuarios e Admins tem acesso
def salvar(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        username = request.POST.get("username")
        is_active = request.POST.get("is_active") == "on"
        is_staff = request.POST.get("is_staff") == "on"
        is_admin = request.POST.get("is_admin") == "on"
        is_superuser = request.POST.get("is_superuser") == "on"

       
        try:
            user = User.objects.create_user(
                username=username,
                nickname=nickname,
                name=name,
                gender=gender,
                age=age,
                is_active=is_active,
                is_staff=is_staff,
                is_admin=is_admin,
                is_superuser=is_superuser
            )
            user.save()
            messages.success(request, 'Usuário salvo com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar o usuário: {e}')
        
        return redirect('listar') 
    
    return render(request, 'cadastro.html')  


# view para editar
@login_required # Variavel usuario recebe recebe usuario ou retorna erro 404,caso 
@user_passes_test(lambda u: u.is_superuser or u.is_admin)
def editar(request, id):
    user = get_object_or_404(User, id=id)
    if not (request.user.is_superuser or request.is_admin):
        return HttpResponseForbidden("não possui acesso")
    return render(request, "update.html", {"user": user})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_admin)
def update(request, id):
    user = get_object_or_404(id=id)
    if request.method =='POST':
        nickname = request.POST.get("nickname")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        age = request.POST.get("age")

        user = get_object_or_404(User, id=id)
        user.nickname = nickname
        user.name = name
        user.gender = gender
        user.age = age
        user.save()
        return redirect('homeLog')
    return render(request, 'listar.html', {'user':user})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_admin)
def delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('homeLog')


def custom_logout(request):
    response = redirect('home')
    response.delete_cookie('user_nickname')  # Remove o cookie ao fazer logout
    logout(request)
    return response

# 
@login_required
@user_passes_test(lambda u: u.is_superuser)
def redirectList(request):
    return render(request, 'SuPages/cadAdmin.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        
        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'O usuário já existe.')
            return redirect('cadAdmin')

        # Criar novo usuário admin usando o método create_admin
        user = User.objects.create_admin(username=username, password=password, nickname=nickname)
        
        messages.success(request, 'Administrador criado com sucesso!')
        return redirect('listarAdmin')

    return render(request, 'SuPages/cadAdmin.html')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def listarAdmin(request):
    users = User.objects.filter(is_admin=True, is_staff=True)  # Filtrar administradores
    query = request.GET.get('q', '')
    if query:
        users = users.filter(Q(username__icontains=query) | Q(nickname__icontains=query))

    paginator = Paginator(users, 10)  # Exibir 10 administradores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'SuPages/listarAdmin.html', context)



                               



