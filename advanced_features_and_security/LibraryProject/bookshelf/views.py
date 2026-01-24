from django.shortcuts import render, redirect
from .forms import ExampleForm  # Make sure to import ExampleForm here

# View to handle the form for creating a new book
def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new book instance
            return redirect('book_list')  # Redirect to the book list page after saving
    else:
        form = ExampleForm()  # Create an empty form for GET request

    return render(request, 'create_book.html', {'form': form})
