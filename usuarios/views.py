from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não conferem')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('/usuarios/cadastro')
        
        try:
            User.objects.create_user(username=username, password=senha)
           # messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return redirect('/usuarios/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor ao criar usuário')
            return redirect('/usuarios/cadastro')
        
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=username, password=senha)

        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado com sucesso!')
            return redirect('/flashcard/novo_flashcard/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return redirect('/usuarios/logar')
        

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/logar')

              