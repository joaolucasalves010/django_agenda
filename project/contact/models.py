from django.db import models
from django.utils import timezone

"""
id (primary key - Auto integer) >> Gerado automaticamente com o django (INTEGER AUTO INCREMENT)
first_name - last_name (string) 
phone (string)
created_data (date)
description (text)

Depois
category (foreign key)
show(boolean)
owner(foreign key)
picture (image)
"""



class Contact(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone = models.CharField(max_length=50)
  email = models.EmailField(max_length=254, blank=True) # Blank true deixa o dado opcional 
  created_date = models.DateTimeField(default=timezone.now)
  description = models.TextField(blank=True)
