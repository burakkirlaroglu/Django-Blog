from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("username")

        newUser = User(username=username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request, "Kayıt başarılı...")
        return redirect("index")
    contextForm = {
        "form" : form
    }
    return render(request, "User/register.html",contextForm)

# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("username")

#             newUser = User(username=username)
#             newUser.set_password(password)
#             newUser.save()
#             login(request, newUser)
#             return redirect("index")
#         contextForm = {
#         "form":form
#         }
#         return render(request, "User/register.html",contextForm)
#     else:
#         form = RegisterForm()
#         contextForm = {
#             "form":form
#         }
#         return render(request, "User/register.html",contextForm)

    # def register(request):
    #     form = RegisterForm()
    #     contextForm = {
    #     "form":form
    #     }
    #     return render(request, template_name="User/register.html", context=contextForm)

    

def loginUser(request):
    form = LoginForm(request.POST or None)

    contextForm = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
    
        user = authenticate(username=username,password=password)

        if user is None:
            messages.info(request, "Kullanıcı adı veya parola hatalı")
            return render(request, "User/login.html")
        messages.success(request, "Giriş başarılı hoşgeldin "+username)
        login(request, user)
        return redirect("index")
    return render(request, template_name="User/login.html", context=contextForm)

def logoutUser(request):
    logout(request)
    messages.warning(request, "Çıkış başarılı")
    return redirect("index")