from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request , "Logged out successfully!")
    return redirect('home')

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user_obj = User.objects.filter(email=email).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request , "Logged in successfully!")
                    return redirect('UploadHome', username=request.user.username)
                else:
                    messages.error(request, "Invalid Email or Password")
            else:
                messages.error(request, "No Email Found")
    else:
        form = LoginForm()

    return render(request, 'login.html', {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists.")
                return render(request, "signup.html", {"form": form})

            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome.")
            return redirect("UploadHome", username=request.user.username)
        else:
            # Form invalid on POST
            messages.warning(request, form.errors)
    else:
        # GET request
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

