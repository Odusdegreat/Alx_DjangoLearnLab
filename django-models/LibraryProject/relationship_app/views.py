from django.shortcuts import render, get_object_or_404
from .models import Library  # <-- must have this

def library_detail(request, pk):
    library = get_object_or_404(Library, pk=pk)  # <-- context variable must be "library"
    return render(
        request,
        "relationship_app/library_detail.html",  # <-- exact string expected
        {"library": library}  # <-- context key must be "library"
    )
