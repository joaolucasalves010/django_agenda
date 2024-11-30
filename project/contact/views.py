from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator
from contact.forms import ContactForm
from django.urls import reverse

# Create your views here.
def index(request):
  contacts = Contact.objects.filter(show=True).order_by("-id") # Pegando todos os contacts da tabela e ordenando contatos da tabela e ordenando com ID decrescente
  paginator = Paginator(contacts, 10)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  
  context = {
    "page_obj": page_obj,
  }
  return render(request, "contact/index.html", context)

def search(request):
  search_value = request.GET.get('q', '').strip()
  print(search_value)

  if search_value == "":
    return redirect("contact:index")

  contacts = Contact.objects.filter(show=True).filter(Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) | Q(phone__icontains=search_value) | Q(email__icontains=search_value)).order_by('-id')
  context = {
    "page_obj": contacts,
    "search_value": search_value,
  }

  return render(request, "contact/index.html", context)

def contact(request, id):
  try:
    contact = Contact.objects.get(id=id)
    site_title = f"{contact.first_name} {contact.last_name} "
    context= {
    "page_obj": contact,
    "site_title": site_title,
    }
    return render(request, "contact/contact.html", context)
  except Exception as exc:
    print(exc)
    raise Http404("Contato não existe")
  
def create(request):
  
  form_action = reverse("contact:create")
  
  if request.method == 'POST':
    form = ContactForm(request.POST)
    
    context = {
      'form': form,
      'form_action': form_action,
    }
    
    if form.is_valid():
      print("Formulario válido")
      contact = form.save()
      return redirect('contact:update', id=contact.pk)
    else:
      print("Formulário não é válido")

    return render(request, 'contact/create.html', context)
  else:
    context = {
      'form': ContactForm(),
      'form_action': form_action,
    }
    return render(request, 'contact/create.html', context)

def update(request, id):
  contact = get_object_or_404(Contact, pk=id, show=True)
  form_action = reverse("contact:update", args=(id,))
  
  if request.method == 'POST':
    form = ContactForm(request.POST, instance=contact)
    
    context = {
      'form': form,
      'form_action': form_action,
    }
    
    if form.is_valid():
      print("Formulario válido")
      contact = form.save()
      return redirect('contact:contact', id=contact.pk)
    else:
      print("Formulário não é válido")

    return render(request, 'contact/create.html', context)
  else:
    context = {
      'form': ContactForm(instance=contact),
      'form_action': form_action,
    }
    return render(request, 'contact/create.html', context)