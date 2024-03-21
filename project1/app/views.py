from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Note
from django import forms
import sqlite3
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
import requests
import re


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'url']

# Identification and authentication flaw, do not use Django's validators in settings.py
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if is_weak_password(password):
                pass
                # return HttpResponse("Your password is too weak. Please choose a stronger one.") # fix for the Identification and authentication flaw
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def is_weak_password(password):
    weak_passwords = ["password", "admin"]
    return password in weak_passwords

def logout_view(request):
    logout(request)
    return redirect('home')

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

# SQL injection flaw and Server-Side Request Forgery flaw
@login_required
def take_notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url') # getting url from user and not validating it
        user_id = request.user.id
        created_at = timezone.now()

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        query = "INSERT INTO app_note (title, url, user_id,  created_at) VALUES (?, ?, ?, ?)" # unsafe query
        cursor.execute(query, (title, url, user_id,  created_at))
        conn.commit()

        #try:
            #response = requests.get(url)
            #content = response.text
        #except Exception as e:
           # content = f"Error fetching URL: {e}"
        
        conn.close()

        return redirect('view_notes')
    else:

        return render(request, 'app/take_notes.html')

"""
# Fix for Server-Side Request Forgery

def take_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            url = note.url
            if not is_safe_url(url):  # validate URL
                return HttpResponseBadRequest("Invalid URL")

            try:
                response = requests.get(url)
                content = response.text
            except Exception as e:
                content = f"Error fetching URL: {e}"

        return redirect('view_notes')
    else:
        form = NoteForm()
        return render(request, 'app/take_notes.html', {'form': form})

def is_safe_url(url):
    # list of trusted domains
    trusted_domains = ['google.com', 'cybersecuritybase.mooc.fi']

    # Check if the URL starts with 'http://' or 'https://'
    if not (url.startswith('http://') or url.startswith('https://')):
        return False

    # Extract the domain from the URL
    domain = re.match(r'^https?://([^/]+)', url).group(1)

    # Check if the extracted domain is in the list of trusted domains
    if domain not in trusted_domains:
        return False

    return True
"""

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
@login_required
def view_notes(request):
    if request.user.is_authenticated:
        notes = Note.objects.all()
    else:
        notes = None
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