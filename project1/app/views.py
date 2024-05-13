from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Note
from django import forms
import sqlite3
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseBadRequest
import requests
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'url']


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'app/home.html')

# SQL injection flaw
@login_required
def take_notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url') # getting url from user and not validating it
        user_id = request.user.id

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        query = "INSERT INTO app_note (title, url, user_id) VALUES ('" + title + "', '" + url + "', " + str(user_id) + ")" # unsafe query
        cursor.execute(query)
        conn.commit()
        conn.close()

        return redirect('view_notes')
    else:

        return render(request, 'app/take_notes.html')

"""

# Fix for SQL injection

def take_notes(request):
    error_message = None
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            url = note.url
            if not is_safe_url(url):  # validate URL
                error_message = "Invalid URL"
            else:
                note.save()
                return redirect('view_notes')

def is_safe_url(url):
    # list of trusted domains
    trusted_domains = ['google.com', 'cybersecuritybase.mooc.fi']

    else:
        form = NoteForm()
    return render(request, 'app/take_notes.html', {'form': form, 'error_message': error_message})
"""

# Server-Side Request Forgery flaw
@login_required
def get_url(request):
    url = request.GET.get('url')
    if url:
        try:
            response = requests.get(url)
            data = response.text
            return render(request, 'app/url.html', {'data': data})
        except requests.RequestException as e:
            error_message = f"Error fetching data from URL: {e}"
            return render(request, 'app/url.html', {'error_message': error_message})
    else:
        return render(request, 'app/url.html')

"""
# Fix for Server-Side Request Forgery

ALLOWED_DOMAINS = ['google.com', 'cybersecuritybase.mooc.fi']

def get_url(request):
    url = request.GET.get('url')
    if url:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ALLOWED_DOMAINS:
            try:
                response = requests.get(url)
                data = response.text
                return render(request, 'app/url.html', {'data': data})
            except requests.RequestException as e:
                error_message = f"Error fetching data from URL: {e}"
                return render(request, 'app/url.html', {'error_message': error_message})
        else:
            error_message = "URL is not allowed."
            return render(request, 'app/url.html', {'error_message': error_message})
    else:
        return render(request, 'app/url.html')
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

# Identification and authentication flaw passwords aren't validated, Django's validators in settings.py are commented out
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                validate_password(password)
            except ValidationError as e:
                error_message = ', '.join(e.messages)
                return render(request, 'app/register.html', {'form': form, 'error_message': error_message})
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

"""
# Fix for identification and authentication flaw use this and take comments off in settings.py Django's validators
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                validate_password(password)
            except ValidationError as e:
                error_message = ', '.join(e.messages)
                return render(request, 'app/register.html', {'form': form, 'error_message': error_message})
            
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})
"""