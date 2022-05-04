from django.shortcuts import render

# Create your views here.
def notes_view(request):
    return render(request,'notes/notes.html')
