from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Note
from django import forms
import sqlite3
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

# Identification and authentication flaw, do not use Django's validators
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if is_weak_password(password):
                #print(f"Warning: User {username} used a weak password!")
                return HttpResponse("Your password is too weak. Please choose a stronger one.") # fix for the flaw
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def is_weak_password(password):
    weak_passwords = ["password", "admin"]
    return password in weak_passwords

"""
# Alternative fix for identification and authentication flaw use this and in settings.py Django's validators
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})
"""

def home(request):
    return render(request, 'app/home.html')

# SQL injection flaw
def take_notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user_id = request.user.id
        created_at = timezone.now()

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        query = "INSERT INTO app_note (title, content, user_id,  created_at) VALUES (?, ?, ?, ?)" # unsafe query
        cursor.execute(query, (title, content, user_id,  created_at))
        conn.commit()
        conn.close()

        return redirect('view_notes')
    else:
        return render(request, 'app/take_notes.html')

"""
# Fix for SQL injection
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
"""

# Broken Access Control flaw, users can access other users notes, user should only see own notes
def view_notes(request):
    notes = Note.objects.all()
    return render(request, 'app/view_notes.html', {'notes': notes})

"""
# Fix for Broken Access Control flaw
def view_notes(request):
    notes = None
    not_authenticated = False
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
    else:
        not_authenticated = True
    return render(request, 'app/view_notes.html', {'notes': notes, 'not_authenticated': not_authenticated})
"""