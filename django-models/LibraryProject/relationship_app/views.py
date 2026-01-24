from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# View to register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, f'Welcome {user.username}!')
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})
