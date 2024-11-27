# type ignore
from django import forms
from contact.models import Contact

class ContactForm(forms.ModelForm):
  first_name = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Primeiro nome"}
    ),
    label="Primeiro nome",
    help_text="Insira seu primeiro nome acima"
  )

  last_name = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Ultimo nome"}
    ),
    label="Ultimo nome",
    help_text="Insira seu ultimo nome acima"
  )

  phone = forms.CharField(
    widget=forms.TextInput(
      attrs={"placeholder": "Insira seu telefone aqui"}
    ),
    label="Telefone",
    help_text='Insira seu telefone acima'
  )
  
  class Meta:
    model = Contact
    fields = ('first_name', 'last_name', 'phone', )
    # widgets = {
    #   'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
    #   'last_name': forms.TextInput(attrs={'placeholder': 'Ultimo nome'}),
    #   'phone': forms.TextInput(attrs={"placeholder": "Insira o número de telefone"})
    # }

  def clean(self):
    cleaned_data = self.cleaned_data
    print(cleaned_data)
    return super().clean()
      