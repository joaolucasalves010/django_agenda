# type ignore
from django import forms
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):
  first_name = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Primeiro nome"}
    ),
    label="Primeiro nome",
    # help_text="Insira seu primeiro nome acima"
  )

  last_name = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Ultimo nome"}
    ),
    label="Ultimo nome",
    # help_text="Insira seu ultimo nome acima"
  )

  phone = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Insira seu telefone aqui"}
    ),
    label="Telefone",
    # help_text='Insira seu telefone acima'
  )

  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={"placeholder": "Insira seu email aqui"}
    ),
    label="Email"
  )

  image = forms.ImageField(
    widget=forms.FileInput(
      attrs={
        "accept": "image/*",
      }
    ),
    label="Imagem",
  )
 
  class Meta:
    model = Contact
    fields = ('first_name', 'last_name', 'phone', 'email', 'description', 'category', 'image', )
    # widgets = {
    #   'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
    #   'last_name': forms.TextInput(attrs={'placeholder': 'Ultimo nome'}),
    #   'phone': forms.TextInput(attrs={"placeholder": "Insira o número de telefone"})
    # }

  def clean(self):
    cleaned_data = self.cleaned_data
    first_name = cleaned_data.get("first_name")
    last_name = cleaned_data.get("last_name")
    
    if last_name == first_name:
      print("ERROR")
      self.add_error("first_name", ValidationError("O primeiro campo não pode ser igual ao segundo", code='invalid'))
      self.add_error("last_name", ValidationError("O primeiro campo não pode ser igual ao segundo", code='invalid'))

    print(cleaned_data)
    return super().clean()

class RegisterForm(UserCreationForm):
  first_name = forms.CharField(
      required=True,
      min_length=3,
  )
  last_name = forms.CharField(
      required=True,
      min_length=3,
  )
  email = forms.EmailField()

  class Meta:
      model = User
      fields = (
          'first_name', 'last_name', 'email',
          'username', 'password1', 'password2',
      )
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        self.add_error(
          'email',
          ValidationError('Já existe este e-mail', code='invalid')
        )
    return email