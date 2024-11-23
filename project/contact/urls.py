from django.contrib import admin
from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
  path('', views.index, name="index"),
  path('contact/<int:id>', views.contact, name="contact"),
  # Urls padrão de CRUD (Create, Read, Update, Delete)
  path('search/', views.search, name='search'),
  path('contact/create', views.create, name='create')
]