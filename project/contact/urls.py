from django.contrib import admin
from django.urls import path
from contact import views

app_name = "contact"

urlpatterns = [
  path('', views.index, name="index"),
  path('contact/<int:id>', views.contact, name="contact"),
  # Urls padrão de CRUD (Create, Read, Update, Delete)
  path('search/', views.search, name='search'),
  path('contact/create', views.create, name='create'),
  path('contact/<int:id>/update', views.update, name='update'),
  path('contact/<int:id>/delete', views.delete, name="delete")
]