from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from registerLogin.models import RegisterLogin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from registerLogin.forms import RegisLogForm


def register(request):
    form = RegisLogForm()

    if request.method == "POST":
        form = RegisLogForm(request.POST)
        if form.is_valid():
            
            data_register_login = RegisterLogin.objects.all()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_type = request.POST.get('user_type')
            provinsi = request.POST.get('provinsi')
            if user_type == "PEMDA" or user_type == "pemda":
                for user in data_register_login:
                    print(user.provinsi)
                    if user.user_type == "PEMDA" or user.user_type == "pemda":
                        if user.provinsi == provinsi:
                            print("gagal")
                            return redirect('registerLogin:register')
            form.save()
            new_user = RegisterLogin(username = username, password = password,user_type = user_type,provinsi = provinsi)
            new_user.save()
            messages.success(request, 'Akun telah berhasil dibuat!')    
            user = authenticate(request, user_type=user_type, provinsi=provinsi)
            print("berhasil")
            return redirect('registerLogin:login')
    

    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("/"))
            #response = HttpResponseRedirect('registerLogin:login')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    
        else:
            messages.info(request, 'Username atau Password salah!')

    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='/regsiterLogin/login/')
def show_registerlogin(request):
    data_register_login = RegisterLogin.objects.all()
    context = {
    'list_registerlogin': data_register_login,
    'last_login': request.COOKIES['last_login'],
}
    return render(request, "login.html")
