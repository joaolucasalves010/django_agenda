from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator
from contact.forms import ContactForm
from django.urls import reverse
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
    contact = Contact.objects.get(id=id)
    site_title = f"{contact.first_name} {contact.last_name} "
    context= {
    "contact": contact,
    "site_title": site_title,
    }
    return render(request, "contact/contact.html", context)

@login_required(login_url='contact:login')
def create(request):
  
  form_action = reverse("contact:create")
  
  if request.method == 'POST':
    form = ContactForm(request.POST, request.FILES)
    
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

@login_required(login_url='contact:login')
def update(request, id):
  contact = get_object_or_404(Contact, pk=id, show=True)
  form_action = reverse("contact:update", args=(id,))
  
  if request.method == 'POST':
    form = ContactForm(request.POST, request.FILES, instance=contact)
    
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
      'form': ContactForm(instance=contact),
      'form_action': form_action,
    }
    return render(request, 'contact/create.html', context)

@login_required(login_url='contact:login')
def delete(request, id):
  contact = get_object_or_404(
    Contact, pk=id, show=True
  )

  confirmation = request.POST.get("confirmation", "no")
  print("confirmation", confirmation)

  if confirmation == "yes":
    contact.delete()
    return redirect('contact:index')

  context = {
    "contact": contact,
    "confirmation": confirmation,
  }

  return render(request, 'contact/contact.html', context)

def register(request):
  form = RegisterForm()

  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth.login(request, user)
      return redirect('contact:login')

  context = {
    'form': form,
  }

  return render(request, 'contact/register.html', context)

def login_view(request):
  form = AuthenticationForm()

  if request.method == "POST":
    form = AuthenticationForm(request, request.POST)
    

    if form.is_valid():
      user = form.get_user()
      auth.login(request, user)
      print(user)

  context = {
    'form': form,
  }

  return render(request, 'contact/login.html', context)

@login_required(login_url='contact:login')
def logout_view(request):
  auth.logout(request)
  return redirect('contact:login')

@login_required(login_url='contact:login')
def user_update(request):
  form = RegisterUpdateForm(instance=request.user)

  if request.method == "POST":
    form = RegisterUpdateForm(data=request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('contact:user_update')
      # return redirect('contact:user_update')

  context = {
    'form': form,
  }

  return render(request, 'contact/register.html', context)