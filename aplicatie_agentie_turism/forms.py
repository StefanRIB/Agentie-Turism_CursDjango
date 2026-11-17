import re
from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profil, Utilizator

CAMPURI_PROFIL = ['judet', 'strada', 'cod_postal', 'tara']
WIDGET_DATA = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')


class ValidariUtilizator:
    """Validari comune pentru inregistrare si editare date (campurile suplimentare)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # campuri obligatorii in formular
        for nume in ('first_name', 'last_name', 'email', 'telefon', 'data_nasterii'):
            self.fields[nume].required = True

    # Validare 1: telefon cu prefix international
    def clean_telefon(self):
        telefon = re.sub(r'[\s.\-]', '', self.cleaned_data['telefon'])
        if not re.fullmatch(r'\+\d{8,15}', telefon):
            raise forms.ValidationError(
                "Introduceți numărul cu prefix internațional, de exemplu +40712345678."
            )
        return telefon

    # Validare 2: data nasterii - minim 18 ani
    def clean_data_nasterii(self):
        d = self.cleaned_data['data_nasterii']
        azi = date.today()
        if d > azi:
            raise forms.ValidationError("Data nașterii nu poate fi în viitor.")
        varsta = azi.year - d.year - ((azi.month, azi.day) < (d.month, d.day))
        if varsta < 18:
            raise forms.ValidationError("Trebuie să aveți cel puțin 18 ani.")
        return d

    # Validare: e-mail unic
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Utilizator.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Există deja un cont cu această adresă de e-mail.")
        return email


class ProfilFieldsForm(forms.Form):
    """Campurile din Profil (toate optionale) + salvarea conditionata."""
    judet = forms.CharField(required=False, max_length=100, label='Județ')
    strada = forms.CharField(required=False, max_length=150, label='Strada')
    cod_postal = forms.CharField(required=False, max_length=10, label='Cod poștal')
    tara = forms.CharField(required=False, max_length=100, label='Țara')

    # Validare 3: cod postal (6 cifre)
    def clean_cod_postal(self):
        cod = self.cleaned_data['cod_postal'].strip()
        if cod and not re.fullmatch(r'\d{6}', cod):
            raise forms.ValidationError("Codul poștal trebuie să aibă exact 6 cifre.")
        return cod

    # Validare 4: tara - doar litere
    def clean_tara(self):
        tara = self.cleaned_data['tara'].strip()
        if tara and not all(c.isalpha() or c in " -'." for c in tara):
            raise forms.ValidationError("Țara poate conține doar litere.")
        return tara

    def salveaza_profil(self, utilizator):
        """Creeaza/actualizeaza Profil doar daca s-a completat macar un camp."""
        date_profil = {c: self.cleaned_data.get(c, '').strip() for c in CAMPURI_PROFIL}
        if any(date_profil.values()):
            Profil.objects.update_or_create(utilizator=utilizator, defaults=date_profil)


class InregistrareForm(ValidariUtilizator, ProfilFieldsForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilizator
        fields = ('username', 'first_name', 'last_name', 'email',
                  'telefon', 'data_nasterii', 'gen')
        widgets = {'data_nasterii': WIDGET_DATA}


class LoginForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False, label='Păstrează-mă logat timp de o zi'
    )


class EditareDateForm(ValidariUtilizator, ProfilFieldsForm, forms.ModelForm):
    class Meta:
        model = Utilizator
        fields = ('first_name', 'last_name', 'email', 'telefon', 'data_nasterii', 'gen')
        widgets = {'data_nasterii': WIDGET_DATA}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profil = Profil.objects.filter(utilizator=self.instance).first()
        if profil and not self.is_bound:
            for camp in CAMPURI_PROFIL:
                self.fields[camp].initial = getattr(profil, camp)