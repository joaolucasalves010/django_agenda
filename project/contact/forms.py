# type ignore
from django import forms
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

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
    required=False
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
  email = forms.EmailField(required=True)

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
  
class RegisterUpdateForm(forms.ModelForm):

  first_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text='Required.',
    error_messages={
      'min_length': 'Please, add more than 2 letters.'
    }
  )

  last_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text='Required.'
  )
  
  password1 = forms.CharField(
    label="Password",
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    help_text=password_validation.password_validators_help_text_html(),
    required=False,
  )

  password2 = forms.CharField(
    label="Password 2",
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    help_text='Use the same password as before.',
    required=False,
  )

  class Meta:
      model = User
      fields = ('first_name', 'last_name', 'email', 'username')


  def save(self, commit=True):
    cleaned_data = self.cleaned_data
    user = super().save(commit=False)

    password = cleaned_data.get('password1')

    if password:
      user.set_password(password)

    if commit:
      user.save()
    
    return user


  def clean(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')

    if password1 or password2: 
      if password1 != password2:
        self.add_error('password1', ValidationError("As senhas não coincidem", code="invalid"))
        self.add_error('password2', ValidationError("As senhas não coincidem", code="invalid"))

    return super().clean()


  def clean_email(self):
    email = self.cleaned_data.get('email')
    current_email = self.instance.email

    if current_email  != email:
      if User.objects.filter(email=email).exists():
        self.add_error('email', ValidationError("ja existe esse email", code='invalid'))

    return email
  
  def clean_password1(self):
    password1 = self.cleaned_data.get('password1')

    if password1:
      try:
        password_validation.validate_password(password1)
      except ValidationError as exc:
        print(exc)
        self.add_error('password1', ValidationError(exc))

    return password1