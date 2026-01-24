from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

# View to register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, f'Welcome {user.username}!')
            next_url = request.GET.get('next', 'home')  # Redirect to the 'next' page if provided, otherwise default to 'home'
            return redirect(next_url)
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})
