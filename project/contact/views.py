from django.shortcuts import render
from contact.models import Contact
from django.http import Http404

# Create your views here.
def index(request):
 
  contacts = Contact.objects.filter(show=True).order_by("-id") # Pegando todos os contacts da tabela e ordenando contatos da tabela e ordenando com ID decrescente
  context = {
    "contacts": contacts,
  }

  return render(request, "contact/index.html", context)

def contact(request, id):
  try:
    contact = Contact.objects.get(id=id)
    context= {
    "contact": contact,
    }
    return render(request, "contact/contact.html", context)
  except Exception as exc:
    print(exc)
    raise Http404("Contato não existe")