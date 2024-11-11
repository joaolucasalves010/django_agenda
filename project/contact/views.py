from django.shortcuts import render
from contact.models import Contact

# Create your views here.
def index(request):
 
  contacts = Contact.objects.filter(show=True).order_by("-id") # Pegando todos os contacts da tabela e ordenando contatos da tabela e ordenando com ID decrescente
  context = {
    "contacts": contacts,
  }

  return render(request, "contact/index.html", context)