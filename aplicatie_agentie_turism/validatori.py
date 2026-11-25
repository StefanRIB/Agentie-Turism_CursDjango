"""
Functii de validare si utilitare reutilizabile (Laborator 5).

"""
import random
import re
import string
from datetime import date

from django.core.exceptions import ValidationError

DOMENII_TEMPORARE = ('guerillamail.com', 'yopmail.com')
VALOARE_NESELECTAT = 'neselectat'

# VARSTA
def calculeaza_varsta(data_nasterii, azi=None):
    """Intoarce (ani, luni) impliniti. Daca param. azi nu e specificat, se foloseste data curenta."""
    azi = azi or date.today()
    luni_total = (azi.year - data_nasterii.year) * 12 + (azi.month - data_nasterii.month)
    if azi.day < data_nasterii.day:  # luna curenta nu s-a incheiat inca
        luni_total -= 1
    return divmod(luni_total, 12)

def text_varsta(data_nasterii):
    ani, luni = calculeaza_varsta(data_nasterii)

    def forma(n, singular, plural):
        if n == 1:
            return f'{n} {singular}'
        return f'{n} {plural}' if n < 20 else f'{n} de {plural}'

    return f"{forma(ani, 'an', 'ani')} și {forma(luni, 'lună', 'luni')}"

def valideaza_major(data_nasterii):
    if data_nasterii > date.today():
        raise ValidationError('Data nașterii nu poate fi în viitor.', code='data_viitor')
    ani, _ = calculeaza_varsta(data_nasterii)
    if ani < 18:
        raise ValidationError(
            'Trebuie să aveți cel puțin 18 ani pentru a trimite un mesaj.', code='minor')

# FORMATARE TEXT
def cuvinte(text):
    """Cuvinte = secvente alfanumerice separate prin secvente nealfanumerice."""
    return re.findall(r'[^\W_]+', text)

def valideaza_fara_linkuri(text):
    for token in text.split():
        t = token.lower()
        if t.startswith('http://') or t.startswith('https://'):
            raise ValidationError(
                'Textul nu poate conține linkuri (http:// sau https://).', code='link')
        # mai mult de 2 cuvinte unite prin puncte, fara spatii: cuv1.cuv2.cuv3
        if re.search(r'[^\W_]+(?:\.[^\W_]+){2,}', token):
            raise ValidationError(
                f'Șirul „{token}” seamănă cu o adresă web (prea multe cuvinte unite prin puncte).',
                code='link')

def valideaza_nume_propriu(text):
    """Incepe cu litera mare si contine doar litere, spatii si cratima.
    Valoarea goala este acceptata (prenumele este optional)."""
    if not text:
        return
    if not (text[0].isalpha() and text[0].isupper()):
        raise ValidationError('Textul trebuie să înceapă cu literă mare.', code='majuscula')
    if not all(c.isalpha() or c in ' -' for c in text):
        raise ValidationError(
            'Sunt permise doar litere, spații și cratime.', code='caractere')


def valideaza_majuscule_dupa_separator(text):
    """Dupa spatiu sau cratima trebuie sa urmeze litera mare."""
    for urmator in re.findall(r'[ -](\S)', text or ''):
        if not urmator.isupper():
            raise ValidationError(
                'După spațiu sau cratimă trebuie să urmeze o literă mare.', code='majuscula')


def valideaza_prima_litera_mare(text):
    if text and not text[0].isupper():
        raise ValidationError('Textul trebuie să înceapă cu literă mare.', code='majuscula')

# E-mail, CNP
def valideaza_email_permanent(email):
    domeniu = email.rsplit('@', 1)[-1].lower()
    if domeniu in DOMENII_TEMPORARE:
        raise ValidationError(
            f'Adresele de e-mail temporare ({domeniu}) nu sunt acceptate.', code='email_temporar')

def data_din_cnp(cnp):
    """Data nasterii codificata in CNP (cifrele 2-7: AALLZZ). ValueError daca nu e valida."""
    secol = {'1': 1900, '2': 1900, '5': 2000, '6': 2000}[cnp[0]]
    data = date(secol + int(cnp[1:3]), int(cnp[3:5]), int(cnp[5:7]))
    if data > date.today():
        raise ValueError('data viitoare')
    return data

def valideaza_cnp(cnp):
    if not cnp:  # camp optional
        return
    if not cnp.isdigit():
        raise ValidationError('CNP-ul trebuie să conțină doar cifre.', code='cnp_cifre')
    if cnp[0] not in '1256':
        raise ValidationError('CNP-ul trebuie să înceapă cu 1, 2, 5 sau 6.', code='cnp_prima_cifra')
    try:
        data_din_cnp(cnp)
    except (ValueError, KeyError):
        raise ValidationError(
            'Cifrele 2-7 din CNP nu formează o dată de naștere validă.', code='cnp_data')

# Cod cerere: LLL-NNNNNN-C
#   3 litere mari, 6 cifre, litera de control calculata din primele 9 caractere
_COD_RE = re.compile(r'^([A-Z]{3})-(\d{6})-([A-Z])$')

def _litera_control(litere, cifre):
    suma = sum((i + 1) * ord(c) for i, c in enumerate(litere))
    suma += sum((i + 2) * int(d) for i, d in enumerate(cifre))
    return chr(ord('A') + suma % 26)

def genereaza_cod_cerere():
    litere = ''.join(random.choices(string.ascii_uppercase, k=3))
    cifre = ''.join(random.choices(string.digits, k=6))
    return f'{litere}-{cifre}-{_litera_control(litere, cifre)}'

def valideaza_cod_cerere(cod):
    potrivire = _COD_RE.match(cod or '')
    if not potrivire or potrivire.group(3) != _litera_control(potrivire.group(1), potrivire.group(2)):
        raise ValidationError(
            'Codul cererii nu este valid; cererea nu a fost generată de formularul nostru.',
            code='cod_invalid')

# Imagini
DIMENSIUNE_MAXIMA_IMAGINE = 2 * 1024 * 1024

def valideaza_dimensiune_imagine(fisier):
    if fisier.size > DIMENSIUNE_MAXIMA_IMAGINE:
        raise ValidationError('Imaginea poate avea cel mult 2 MB.', code='imagine_mare')
