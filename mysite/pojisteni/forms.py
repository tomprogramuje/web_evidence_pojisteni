from django import forms
from .models import Pojistenec, Pojisteni, Uzivatel


class PojistenecForm(forms.ModelForm):
    jaka_pojisteni = forms.ModelMultipleChoiceField(queryset=Pojisteni.objects.all(), required=False)

    class Meta:
        model = Pojistenec
        fields = ["jmeno", "prijmeni", "ulice", "mesto", "psc", "telefon", "email", "jaka_pojisteni"]


class PojisteniForm(forms.ModelForm):

    class Meta:
        model = Pojisteni
        fields = ["typ", "castka", "predmet", "platnost_od", "platnost_do"]

class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ["email", "password"]


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']
