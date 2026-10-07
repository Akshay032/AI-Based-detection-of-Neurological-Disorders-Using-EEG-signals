from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   # 🔥 VERY IMPORTANT
            user.save()

            # update profile
            profile = user.profile
            profile.bio = form.cleaned_data.get('bio')

            if request.FILES.get('photo'):
                profile.photo = request.FILES.get('photo')

            profile.save()

            return render(request, 'accounts/waiting_approval.html')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})





from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your account is waiting for admin approval.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
