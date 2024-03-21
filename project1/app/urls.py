from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('take-notes/', views.take_notes, name='take_notes'),
    path('view-notes/', views.view_notes, name='view_notes'),
    path('logout/', views.logout_view, name='logout'),
]