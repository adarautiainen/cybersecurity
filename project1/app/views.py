from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Note
from django import forms

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def home(request):
    return render(request, 'app/home.html')

def take_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('view_notes')
    else:
        form = NoteForm()
    return render(request, 'app/take_notes.html', {'form': form})

def view_notes(request):
    # jos poistaa tän ???
    notes = None
    not_authenticated = False
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
    else:
        not_authenticated = True
    return render(request, 'app/view_notes.html', {'notes': notes, 'not_authenticated': not_authenticated})
