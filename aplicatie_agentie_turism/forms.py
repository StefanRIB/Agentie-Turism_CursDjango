import re
from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import (
    CategorieServiciu, Departament, Furnizor, Profil, ServiciuIndividual, TipMesaj, Utilizator,
)
from .validatori import (
    VALOARE_NESELECTAT, cuvinte, data_din_cnp, genereaza_cod_cerere, valideaza_cnp,
    valideaza_cod_cerere, valideaza_dimensiune_imagine, valideaza_email_permanent,
    valideaza_fara_linkuri, valideaza_major, valideaza_majuscule_dupa_separator,
    valideaza_nume_propriu, valideaza_prima_litera_mare,
)

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

TEXT_ZILE = (
    "Pentru review-uri/cereri minimul de zile de așteptare trebuie setat de la 4 încolo, "
    "iar pentru reclamații/întrebări/programări de la 2 încolo. Maximul e 30."
)

# LABORATOR 5 - TASK 3: FORMULAR DE CONTACT
class ContactForm(forms.Form):
    nume = forms.CharField(
        max_length=10, label='Nume',
        validators=[valideaza_nume_propriu, valideaza_majuscule_dupa_separator],
        error_messages={'required': 'Numele este obligatoriu.',
                        'max_length': 'Numele poate avea cel mult 10 caractere.'},
    )
    prenume = forms.CharField(
        required=False, max_length=30, label='Prenume',
        help_text='Prenumele pot fi separate prin spațiu sau liniuță (ex: Ana Maria sau Ana-Maria).',
        validators=[valideaza_nume_propriu, valideaza_majuscule_dupa_separator],
        error_messages={'max_length': 'Prenumele poate avea cel mult 30 de caractere.'},
    )
    cnp = forms.CharField(
        required=False, min_length=13, max_length=13, label='CNP',
        widget=forms.TextInput(attrs={'inputmode': 'numeric', 'autocomplete': 'off'}),
        error_messages={'min_length': 'CNP-ul trebuie să aibă exact 13 caractere.',
                        'max_length': 'CNP-ul trebuie să aibă exact 13 caractere.'},
    )
    data_nasterii = forms.DateField(
        label='Data nașterii', widget=WIDGET_DATA,
        error_messages={'required': 'Data nașterii este obligatorie.',
                        'invalid': 'Introduceți o dată validă.'},
    )
    email = forms.EmailField(
        label='E-mail', validators=[valideaza_email_permanent],
        error_messages={'required': 'Adresa de e-mail este obligatorie.',
                        'invalid': 'Introduceți o adresă de e-mail validă.'},
    )
    confirmare_email = forms.EmailField(
        label='Confirmare e-mail', validators=[valideaza_email_permanent],
        error_messages={'required': 'Confirmați adresa de e-mail.',
                        'invalid': 'Introduceți o adresă de e-mail validă.'},
    )
    telefon = forms.CharField(
        required=False, max_length=20, label='Telefon',
        help_text='Format: 0712345678 sau, cu prefixul țării, +40712345678.',
    )
    tip_mesaj = forms.ChoiceField(
        label='Tip mesaj', initial=VALOARE_NESELECTAT, choices=[],
        error_messages={'required': 'Alegeți tipul mesajului.',
                        'invalid_choice': 'Tipul de mesaj selectat nu este unul dintre cele permise.'},
    )
    departament = forms.ChoiceField(
        label='Departament destinație', initial=VALOARE_NESELECTAT, choices=[],
        error_messages={'required': 'Alegeți departamentul.',
                        'invalid_choice': 'Departamentul selectat nu este unul dintre cele permise.'},
    )
    subiect = forms.CharField(
        max_length=100, label='Subiect',
        validators=[valideaza_fara_linkuri, valideaza_nume_propriu],
        error_messages={'required': 'Subiectul este obligatoriu.',
                        'max_length': 'Subiectul poate avea cel mult 100 de caractere.'},
    )
    zile_asteptare = forms.IntegerField(
        label='Minim zile așteptare', min_value=1, max_value=30, help_text=TEXT_ZILE,
        error_messages={'required': 'Precizați câte zile sunteți dispus să așteptați.',
                        'invalid': 'Introduceți un număr natural.',
                        'min_value': 'Numărul de zile trebuie să fie cel puțin 1.',
                        'max_value': 'Numărul de zile poate fi cel mult 30.'},
    )
    mesaj = forms.CharField(
        label='Mesaj (semnați-vă la final cu numele dumneavoastră)',
        widget=forms.Textarea(attrs={'rows': 7}),
        error_messages={'required': 'Mesajul este obligatoriu.'},
    )
    imagine_1 = forms.ImageField(
        required=False, label='Imagine 1', validators=[valideaza_dimensiune_imagine],
        error_messages={'invalid_image': 'Fișierul încărcat nu este o imagine validă.'})
    imagine_2 = forms.ImageField(
        required=False, label='Imagine 2', validators=[valideaza_dimensiune_imagine],
        error_messages={'invalid_image': 'Fișierul încărcat nu este o imagine validă.'})
    imagine_3 = forms.ImageField(
        required=False, label='Imagine 3', validators=[valideaza_dimensiune_imagine],
        error_messages={'invalid_image': 'Fișierul încărcat nu este o imagine validă.'})
    gdpr = forms.BooleanField(
        label='Sunt de acord cu prelucrarea datelor mele personale (GDPR)', initial=False,
        error_messages={'required': 'Trebuie să vă dați acordul pentru prelucrarea datelor.'},
    )
    cod_cerere = forms.CharField(widget=forms.HiddenInput, error_messages={
        'required': 'Lipsește codul cererii.'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tipurile si departamentele vin din baza de date
        self.tipuri = {t.cod: t for t in TipMesaj.objects.prefetch_related('departamente')}
        self.fields['tip_mesaj'].choices = (
            [(VALOARE_NESELECTAT, 'neselectat')] + [(cod, t.nume) for cod, t in self.tipuri.items()]
        )
        nume_departamente = Departament.objects.filter(
            tipuri_mesaje__isnull=False).distinct().order_by('nume_departament')
        self.fields['departament'].choices = (
            [(VALOARE_NESELECTAT, 'neselectat')]
            + [(d.nume_departament, d.nume_departament) for d in nume_departamente]
        )
        if not self.is_bound:
            self.initial['cod_cerere'] = genereaza_cod_cerere()

    def mapare_departamente(self):
        """{tip: {zile_minime, departamente}} pentru actualizarea dinamica a dropdown-ului."""
        return {
            cod: {
                'zile_minime': t.zile_minime,
                'departamente': sorted(d.nume_departament for d in t.departamente.all()),
            }
            for cod, t in self.tipuri.items()
        }

    def tip_ales(self):
        return self.tipuri[self.cleaned_data['tip_mesaj']]

    # validari campuri 
    def clean_cnp(self):
        cnp = self.cleaned_data['cnp']
        valideaza_cnp(cnp)
        return cnp

    def clean_data_nasterii(self):
        data = self.cleaned_data['data_nasterii']
        valideaza_major(data)
        return data

    def clean_email(self):
        email = self.cleaned_data['email']
        valideaza_email_permanent(email)
        return email

    def clean_tip_mesaj(self):
        tip = self.cleaned_data['tip_mesaj']
        if tip == VALOARE_NESELECTAT:
            raise forms.ValidationError('Alegeți un tip de mesaj (nu lăsați „neselectat”).')
        if tip not in self.tipuri:
            raise forms.ValidationError('Tipul de mesaj nu există în baza de date.')
        return tip

    def clean_departament(self):
        departament = self.cleaned_data['departament']
        if departament == VALOARE_NESELECTAT:
            raise forms.ValidationError('Alegeți un departament (nu lăsați „neselectat”).')
        if not Departament.objects.filter(nume_departament=departament).exists():
            raise forms.ValidationError('Departamentul nu există în baza de date.')
        return departament

    def clean_mesaj(self):
        mesaj = self.cleaned_data['mesaj']
        valideaza_fara_linkuri(mesaj)
        lista = cuvinte(mesaj)
        if not 5 <= len(lista) <= 100:
            raise forms.ValidationError(
                f'Mesajul trebuie să aibă între 5 și 100 de cuvinte (acum are {len(lista)}).')
        lungi = [c for c in lista if len(c) > 15]
        if lungi:
            raise forms.ValidationError(
                f'Un cuvânt nu poate avea mai mult de 15 caractere (ex: „{lungi[0]}”).')
        return mesaj

    def clean_gdpr(self):
        if not self.cleaned_data['gdpr']:
            raise forms.ValidationError('Trebuie să vă dați acordul pentru prelucrarea datelor.')
        return True

    def clean_cod_cerere(self):
        cod = self.cleaned_data['cod_cerere']
        valideaza_cod_cerere(cod)
        return cod

    # validari pe mai multe campuri 
    def clean(self):
        date_curate = super().clean()
        email, confirmare = date_curate.get('email'), date_curate.get('confirmare_email')
        if email and confirmare and email.lower() != confirmare.lower():
            self.add_error('confirmare_email', 'Adresa de e-mail și confirmarea ei nu coincid.')

        mesaj, nume = date_curate.get('mesaj'), date_curate.get('nume')
        if mesaj and nume:
            ultimul = mesaj.split()[-1].strip('.,;:!?…"\'()')
            if ultimul.casefold() != nume.casefold():
                self.add_error('mesaj', f'Mesajul trebuie să se încheie cu semnătura dumneavoastră: „{nume}”.')

        tip = self.tipuri.get(date_curate.get('tip_mesaj'))
        zile = date_curate.get('zile_asteptare')
        if tip and zile is not None and zile < tip.zile_minime:
            self.add_error(
                'zile_asteptare',
                f'Pentru „{tip.nume}” numărul minim de zile de așteptare este {tip.zile_minime}.')

        cnp, data_nasterii = date_curate.get('cnp'), date_curate.get('data_nasterii')
        if cnp and data_nasterii:
            if data_din_cnp(cnp) != data_nasterii:
                self.add_error('cnp', 'CNP-ul nu corespunde cu data nașterii introduse.')

        departament = date_curate.get('departament')
        if tip and departament:
            permise = {d.nume_departament for d in tip.departamente.all()}
            if departament not in permise:
                self.add_error(
                    'departament',
                    f'Departamentul „{departament}” nu poate primi mesaje de tip „{tip.nume}”. '
                    'Datele formularului au fost modificate.')
        return date_curate

# LABORATOR 5 - TASK 2: FORMULAR DE FILTRARE A PRODUSELOR
PRODUSE_PE_PAGINA = [(6, '6'), (12, '12'), (18, '18'), (24, '24')] # divizibile cu 1, 2 si 3
COLOANE_GRID = [(1, '1 coloană'), (2, '2 coloane'), (3, '3 coloane')]
COLOANE_SORTARE = [('nume', 'Nume serviciu'), ('pret', 'Preț'), ('rating', 'Rating')]
DIRECTII_SORTARE = [('a', 'Ascendent (a)'), ('d', 'Descendent (d)')]
IMPLICIT_PE_PAGINA = 6
IMPLICIT_COLOANE = 3

class FiltrareProduseForm(forms.Form):
    nume = forms.CharField(
        required=False, label='Nume serviciu conține',
        widget=forms.TextInput(attrs={'placeholder': 'ex: City Break'}))
    facilitati = forms.CharField(required=False, label='Facilități conțin')
    pret_min = forms.DecimalField(
        required=False, min_value=0, max_digits=8, decimal_places=2, label='Preț minim (EUR)',
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        error_messages={'min_value': 'Prețul minim nu poate fi negativ.',
                        'invalid': 'Introduceți un preț valid.',
                        'max_digits': 'Prețul introdus este prea mare.',
                        'max_decimal_places': 'Prețul poate avea cel mult 2 zecimale.'})
    pret_max = forms.DecimalField(
        required=False, min_value=0, max_digits=8, decimal_places=2, label='Preț maxim (EUR)',
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        error_messages={'min_value': 'Prețul maxim nu poate fi negativ.',
                        'invalid': 'Introduceți un preț valid.',
                        'max_digits': 'Prețul introdus este prea mare.',
                        'max_decimal_places': 'Prețul poate avea cel mult 2 zecimale.'})
    rating_min = forms.FloatField(
        required=False, min_value=0, max_value=5, label='Rating minim',
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        error_messages={'min_value': 'Ratingul minim este 0.', 'max_value': 'Ratingul maxim este 5.',
                        'invalid': 'Introduceți un rating valid.'})
    rating_max = forms.FloatField(
        required=False, min_value=0, max_value=5, label='Rating maxim',
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        error_messages={'min_value': 'Ratingul minim este 0.', 'max_value': 'Ratingul maxim este 5.',
                        'invalid': 'Introduceți un rating valid.'})
    stoc_min = forms.IntegerField(
        required=False, min_value=0, label='Locuri disponibile (minim)',
        error_messages={'min_value': 'Numărul de locuri nu poate fi negativ.',
                        'invalid': 'Introduceți un număr întreg.'})
    stoc_max = forms.IntegerField(
        required=False, min_value=0, label='Locuri disponibile (maxim)',
        error_messages={'min_value': 'Numărul de locuri nu poate fi negativ.',
                        'invalid': 'Introduceți un număr întreg.'})
    activ = forms.ChoiceField(
        required=False, label='Disponibilitate',
        choices=[('', 'Toate'), ('da', 'Doar active'), ('nu', 'Doar inactive')])
    prestat_de_la = forms.DateField(
        required=False, label='Data prestării – de la', widget=WIDGET_DATA,
        error_messages={'invalid': 'Introduceți o dată validă.'})
    prestat_pana_la = forms.DateField(
        required=False, label='Data prestării – până la', widget=WIDGET_DATA,
        error_messages={'invalid': 'Introduceți o dată validă.'})
    adaugat_de_la = forms.DateField(
        required=False, label='Adăugat în catalog – de la', widget=WIDGET_DATA,
        error_messages={'invalid': 'Introduceți o dată validă.'})
    adaugat_pana_la = forms.DateField(
        required=False, label='Adăugat în catalog – până la', widget=WIDGET_DATA,
        error_messages={'invalid': 'Introduceți o dată validă.'})
    categorie = forms.ModelChoiceField(
        required=False, queryset=CategorieServiciu.objects.all(), to_field_name='nume',
        empty_label='Toate categoriile', label='Categorie',
        error_messages={'invalid_choice': 'Categoria selectată nu există.'})
    furnizor = forms.ModelChoiceField(
        required=False, queryset=Furnizor.objects.all(),
        empty_label='Toți furnizorii', label='Furnizor',
        error_messages={'invalid_choice': 'Furnizorul selectat nu există.'})
    taguri = forms.CharField(
        required=False, label='Taguri (separate prin virgulă)',
        widget=forms.TextInput(attrs={'placeholder': 'ex: familie, mare'}))
    nr_pe_pagina = forms.TypedChoiceField(
        required=False, choices=PRODUSE_PE_PAGINA, coerce=int, empty_value=IMPLICIT_PE_PAGINA,
        initial=IMPLICIT_PE_PAGINA, label='Produse pe pagină',
        error_messages={'invalid_choice': 'Număr de produse pe pagină invalid.'})
    nr_coloane = forms.TypedChoiceField(
        required=False, choices=COLOANE_GRID, coerce=int, empty_value=IMPLICIT_COLOANE,
        initial=IMPLICIT_COLOANE, label='Afișare pe',
        error_messages={'invalid_choice': 'Număr de coloane invalid.'})
    col = forms.ChoiceField(
        required=False, choices=COLOANE_SORTARE, initial='nume', label='Sortează după',
        error_messages={'invalid_choice': 'Coloană de sortare invalidă.'})
    sort = forms.ChoiceField(
        required=False, choices=DIRECTII_SORTARE, initial='a', label='Direcție',
        error_messages={'invalid_choice': 'Direcție de sortare invalidă.'})

    def __init__(self, *args, categorie_curenta=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.categorie_curenta = categorie_curenta
        if categorie_curenta:
            # pe paginile categoriilor campul este setat, ascuns si readonly
            camp = self.fields['categorie']
            camp.initial = categorie_curenta.nume
            camp.widget = forms.HiddenInput(attrs={'readonly': 'readonly'})

    # validari pe un singur camp 
    def clean_nume(self):
        nume = self.cleaned_data['nume'].strip()
        if nume and len(nume) < 2:
            raise forms.ValidationError('Introduceți cel puțin 2 caractere pentru nume.')
        if nume and not re.fullmatch(r"[\w\s\-'.]+", nume):
            raise forms.ValidationError('Numele conține caractere nepermise.')
        return nume

    def clean_taguri(self):
        taguri = [t.strip() for t in self.cleaned_data['taguri'].split(',') if t.strip()]
        for tag in taguri:
            if not re.fullmatch(r'[\w\-]{2,50}', tag):
                raise forms.ValidationError(
                    f'Tagul „{tag}” este invalid (2–50 de caractere: litere, cifre sau cratimă).')
        return taguri

    def clean_adaugat_pana_la(self):
        data = self.cleaned_data['adaugat_pana_la']
        if data and data > date.today():
            raise forms.ValidationError('Data „până la” nu poate fi în viitor.')
        return data

    # validari pe mai multe campuri 
    def clean(self):
        d = super().clean()
        perechi = [
            ('pret_min', 'pret_max', 'Prețul minim nu poate depăși prețul maxim.'),
            ('rating_min', 'rating_max', 'Ratingul minim nu poate depăși ratingul maxim.'),
            ('stoc_min', 'stoc_max', 'Numărul minim de locuri nu poate depăși maximul.'),
            ('prestat_de_la', 'prestat_pana_la', 'Data „de la” nu poate fi după data „până la”.'),
            ('adaugat_de_la', 'adaugat_pana_la', 'Data „de la” nu poate fi după data „până la”.'),
        ]
        for mic, mare, mesaj in perechi:
            if d.get(mic) is not None and d.get(mare) is not None and d[mic] > d[mare]:
                self.add_error(mare, mesaj)
        return d

# LABORATOR 5 - TASK 4: FORMULAR (ModelForm) PENTRU ADAUGAREA PRODUSELOR
class ProdusForm(forms.ModelForm):
    # inputuri aditionale: din ele se calculeaza coloana pret_serviciu
    pret_achizitie = forms.DecimalField(
        min_value=0.01, max_digits=8, decimal_places=2, label='Preț de achiziție de la furnizor (EUR)',
        help_text='Prețul plătit furnizorului pentru acest serviciu.',
        error_messages={'required': 'Introduceți prețul de achiziție.',
                        'min_value': 'Prețul de achiziție trebuie să fie pozitiv.',
                        'invalid': 'Introduceți un preț valid.'})
    adaos_comercial = forms.DecimalField(
        min_value=0, max_value=300, max_digits=5, decimal_places=2, label='Adaos comercial (%)',
        help_text='Procentul adăugat la prețul de achiziție (0–300). Din el rezultă prețul final.',
        error_messages={'required': 'Introduceți adaosul comercial.',
                        'min_value': 'Adaosul nu poate fi negativ.',
                        'max_value': 'Adaosul poate fi cel mult 300%%.',
                        'invalid': 'Introduceți un procent valid.'})
    # doua validatoare externe
    nume_serviciu = forms.CharField(
        max_length=200, label='Denumirea serviciului',
        validators=[valideaza_fara_linkuri, valideaza_prima_litera_mare],
        help_text='Începe cu literă mare; fără linkuri.',
        error_messages={'required': 'Denumirea serviciului este obligatorie.',
                        'max_length': 'Denumirea poate avea cel mult 200 de caractere.'})

    class Meta:
        model = ServiciuIndividual
        fields = ['nume_serviciu', 'facilitati_incluse', 'id_categorie', 'id_furnizor',
                  'stoc_locuri', 'taguri']
        labels = {
            'facilitati_incluse': 'Ce include serviciul',
            'id_categorie': 'Categoria serviciului',
            'id_furnizor': 'Furnizor (prestator)',
            'stoc_locuri': 'Număr de locuri disponibile',
        }
        help_texts = {
            'taguri': 'Taguri separate prin virgulă (maxim 6), ex: familie, mare.',
            'stoc_locuri': 'Între 1 și 500 de locuri.',
        }
        error_messages = {
            'id_categorie': {'required': 'Alegeți categoria.'},
            'id_furnizor': {'required': 'Alegeți furnizorul.'},
            'stoc_locuri': {'required': 'Introduceți numărul de locuri.',
                            'invalid': 'Introduceți un număr întreg.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facilitati_incluse'].validators.append(valideaza_fara_linkuri)
        self.fields['facilitati_incluse'].widget.attrs['rows'] = 3

    # validari campuri
    def clean_nume_serviciu(self):
        nume = self.cleaned_data['nume_serviciu'].strip()
        if len(nume) < 5:
            raise forms.ValidationError('Denumirea trebuie să aibă cel puțin 5 caractere.')
        return nume

    def clean_stoc_locuri(self):
        stoc = self.cleaned_data['stoc_locuri']
        if not 1 <= stoc <= 500:
            raise forms.ValidationError('Numărul de locuri trebuie să fie între 1 și 500.')
        return stoc

    def clean_taguri(self):
        taguri = self.cleaned_data['taguri']
        if len(taguri) > 6:
            raise forms.ValidationError('Puteți adăuga cel mult 6 taguri.')
        return taguri

    # validare pe mai multe campuri 
    def clean(self):
        d = super().clean()
        stoc, adaos = d.get('stoc_locuri'), d.get('adaos_comercial')
        achizitie = d.get('pret_achizitie')
        if stoc is not None and adaos is not None and stoc >= 100 and adaos > 50:
            self.add_error(
                'adaos_comercial',
                'Pentru servicii cu 100 sau mai multe locuri adaosul comercial poate fi cel mult 50%.')
        if achizitie is not None and adaos is not None:
            if achizitie * (1 + adaos / 100) >= 1_000_000:
                self.add_error('pret_achizitie', 'Prețul final rezultat este prea mare (maximum 999999.99 EUR).')
        return d
