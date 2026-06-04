from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = form.cleaned_data['email']
            user.voter_id = form.cleaned_data['voter_id']
            user.role = form.cleaned_data['role']

            user.save()

            messages.success(request, "Account created successfully")

            return redirect('login')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # SUPERUSER → ADMIN DASHBOARD
            if user.is_superuser:
                return redirect("admin_dashboard")

            # VOTER
            elif user.role == "voter":
                return redirect("voter_dashboard")

            # CANDIDATE
            elif user.role == "candidate":
                return redirect("candidate_dashboard")

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")




def logout_view(request):
    logout(request)
    return redirect('login')





