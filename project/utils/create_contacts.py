import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice
import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent

print(str(DJANGO_BASE_DIR)) # >> C:\Workspace\Python\django_agenda\project

NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
settings.USE_TZ = False

django.setup()

if __name__ == "__main__":
  import faker

  from contact.models import Category, Contact

  Category.objects.all().delete()
  Contact.objects.all().delete()

  fake = faker.Faker('pt_BR')
  categories = ['Amigos', 'Familia', 'Conhecidos']

  django_categories = [Category(name=name) for name in categories]

  for category in django_categories:
    category.save()

  django_contacts = []

  """
  first_name
  last_name
  phone
  email
  created_date
  category
  description
  """

  for _ in range(NUMBER_OF_OBJECTS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number()
    email = fake.email()
    created_date: datetime = fake.date_this_year()
    category = choice(django_categories)
    description = fake.text(max_nb_chars=100)
    
    django_contacts.append(
      Contact(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        created_date=created_date,
        category=category,
        description=description
      )
    )

  if len(django_contacts) > 0:
    Contact.objects.bulk_create(django_contacts)