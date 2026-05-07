from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # hash password before saving
            user.password = make_password(form.cleaned_data['password'])

            user.save()

            messages.success(request, "Account created successfully")
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})





def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # email or voter_id
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "voter":
                return redirect("voter_dashboard")

            elif user.role == "candidate":
                return redirect("candidate_dashboard")

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")




