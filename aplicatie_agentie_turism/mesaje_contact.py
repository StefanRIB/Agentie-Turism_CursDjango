"""
Prelucrarea si stocarea mesajelor primite prin pagina de contact (Laborator 5).

Mesajele nu se salveaza in baza de date, ci in fisiere JSON:
    aplicatie_agentie_turism/Mesaje_nerezolvate/<departament>/mesaj_<timestamp>[_urgent].json
"""
import html
import json
import os
import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path

from .models import Departament
from .validatori import text_varsta

RADACINA = Path(__file__).resolve().parent / 'Mesaje_nerezolvate'
EXTENSII_IMAGINI = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
RE_NUME_IMAGINE = re.compile(r'^mesaj_\d+(?:_urgent)?_img[1-3]\.(?:jpg|jpeg|png|gif|webp)$')

# Foldere
def nume_folder(nume_departament):
    """'Relații clienți' -> 'Relatii_clienti' (nume formatat pentru un folder)."""
    ascii_ = unicodedata.normalize('NFKD', nume_departament).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', ascii_).strip('_') or 'departament'

def asigura_folder(cale):
    """Verifica prezenta folderului si il creeaza daca nu exista."""
    try:
        os.listdir(cale)
    except FileNotFoundError:
        os.makedirs(cale)
    return Path(cale)

def asigura_foldere_departamente():
    """Mesaje_nerezolvate + cate un subfolder pentru fiecare departament din baza de date."""
    asigura_folder(RADACINA)
    for nume in Departament.objects.values_list('nume_departament', flat=True):
        asigura_folder(RADACINA / nume_folder(nume))

# Preprocesari
def majuscule_dupa_terminatori(text):
    """Litera de dupa '.', '?', '!', '...' devine majuscula."""
    return re.sub(
        r'([.!?]+)(\s+)([^\W\d_])',
        lambda m: m.group(1) + m.group(2) + m.group(3).upper(),
        text,
    )

def mesaj_in_html(text):
    """Spatiile succesive devin unul singur; fiecare paragraf (linie noua) intra in <p></p>."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+', ' ', text)
    text = majuscule_dupa_terminatori(text)
    paragrafe = [p.strip() for p in text.split('\n') if p.strip()]
    return ''.join(f'<p>{html.escape(p)}</p>' for p in paragrafe)

def pregateste_date(date_curate, tip, ip):
    """Intoarce dictionarul care se salveaza in format JSON."""
    date = dict(date_curate)
    imagini = [date.pop(f'imagine_{i}', None) for i in (1, 2, 3)]
    date.pop('confirmare_email', None)

    data_nasterii = date.pop('data_nasterii')
    date['varsta'] = text_varsta(data_nasterii)       
    date['mesaj'] = mesaj_in_html(date['mesaj'])
    date['urgent'] = date['zile_asteptare'] == tip.zile_minime
    date['ip'] = ip
    acum = datetime.now()
    date['data_sosire'] = acum.isoformat(timespec='seconds')
    date['timestamp'] = int(acum.timestamp())
    return date, [i for i in imagini if i]

# Salvare
def salveaza_mesaj(date, imagini):
    """Scrie fisierul JSON in folderul departamentului."""
    asigura_foldere_departamente()
    folder = asigura_folder(RADACINA / nume_folder(date['departament']))
    sufix = '_urgent' if date['urgent'] else ''
    timestamp = date['timestamp']
    while (folder / f'mesaj_{timestamp}{sufix}.json').exists():   
        timestamp += 1
    baza = f'mesaj_{timestamp}{sufix}'

    nume_imagini = []
    for i, fisier in enumerate(imagini, start=1):
        extensie = os.path.splitext(fisier.name)[1].lower()
        if extensie not in EXTENSII_IMAGINI:
            extensie = '.jpg'
        nume = f'{baza}_img{i}{extensie}'
        with open(folder / nume, 'wb') as f:
            for bucata in fisier.chunks():
                f.write(bucata)
        nume_imagini.append(nume)
    date['imagini'] = nume_imagini

    cale = folder / f'{baza}.json'
    with open(cale, 'w', encoding='utf-8') as f:
        json.dump(date, f, ensure_ascii=False, indent=2)
    return cale

# Citire (pagina /mesaje)
def departament_dupa_folder(folder):
    for dep in Departament.objects.all():
        if nume_folder(dep.nume_departament) == folder:
            return dep
    return None

def incarca_mesaje(dep, an=None, luna=None, zi=None):
    """Mesajele unui departament, filtrate dupa an / an+luna / an+luna+zi (data sosirii)."""
    folder = asigura_folder(RADACINA / nume_folder(dep.nume_departament))
    rezultat = []
    for cale in sorted(folder.glob('mesaj_*.json'), reverse=True):
        try:
            with open(cale, encoding='utf-8') as f:
                mesaj = json.load(f)
            data = datetime.fromisoformat(mesaj['data_sosire'])
        except (OSError, ValueError, KeyError):
            continue   
        if an is not None and data.year != an:
            continue
        if luna is not None and data.month != luna:
            continue
        if zi is not None and data.day != zi:
            continue
        mesaj['_fisier'] = cale.name
        rezultat.append(mesaj)
    return rezultat
