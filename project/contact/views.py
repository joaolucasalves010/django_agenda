from django.shortcuts import render, redirect
from contact.models import Contact
from django.db.models import Q
from django.http import Http404

# Create your views here.
def index(request):
  contacts = Contact.objects.filter(show=True).order_by("-id")[10:20] # Pegando todos os contacts da tabela e ordenando contatos da tabela e ordenando com ID decrescente
  context = {
    "contacts": contacts,
  }
  return render(request, "contact/index.html", context)

def search(request):
  search_value = request.GET.get('q', '').strip()
  print(search_value)

  if search_value == "":
    return redirect("contact:index")

  contacts = Contact.objects.filter(show=True).filter(Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) | Q(phone__icontains=search_value) | Q(email__icontains=search_value)).order_by('-id')
  context = {
    "contacts": contacts,
    "search_value": search_value,
  }

  return render(request, "contact/index.html", context)

def contact(request, id):
  try:
    contact = Contact.objects.get(id=id)
    site_title = f"{contact.first_name} {contact.last_name} "
    context= {
    "contact": contact,
    "site_title": site_title,
    }
    return render(request, "contact/contact.html", context)
  except Exception as exc:
    print(exc)
    raise Http404("Contato não existe")