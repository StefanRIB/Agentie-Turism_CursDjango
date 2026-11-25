from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from decimal import Decimal

from django.contrib.auth.decorators import user_passes_test
from django.http import FileResponse, Http404, JsonResponse
from django.template.loader import render_to_string
from django.utils.cache import add_never_cache_headers, patch_vary_headers
from django.utils.safestring import mark_safe

from .forms import (
    InregistrareForm, LoginForm, EditareDateForm, ContactForm, FiltrareProduseForm, ProdusForm,
    IMPLICIT_COLOANE, IMPLICIT_PE_PAGINA,
)
from .mesaje_contact import (
    RE_NUME_IMAGINE, RADACINA, asigura_foldere_departamente, departament_dupa_folder,
    incarca_mesaje, nume_folder, pregateste_date, salveaza_mesaj,
)
from .models import Profil, Utilizator, Departament

def trimite_email():
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
        from_email='cursdjango70@gmail.com',
        recipient_list=['cursdjango70@gmail.com'],
        fail_silently=False,
    )

def get_ip(request):
    req_headers = request.META
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')

class Accesare:
    id_curent = 0
    istoric_accesari = []

    def __init__(self, ip_client, url, parametri=None):
        Accesare.id_curent += 1
        self.id = Accesare.id_curent
        self.ip_client = ip_client
        self.url = url
        if parametri is None:
            self.parametri = {}
        else:
            self.parametri = parametri
        self.data = datetime.datetime.now() 
        Accesare.istoric_accesari.append(self)

    def lista_parametri(self):
        lista_rezultata = []
        for cheie, valoare in self.parametri.items():
            if valoare == "" or valoare is None:
                valoare_finala = None
            else:
                valoare_finala = valoare
            lista_rezultata.append((cheie, valoare_finala))
        return lista_rezultata 

    def string_url(self):
         return self.url   
    
    def pagina(self):
        return self.url.split('?')[0]
    
    def calculeaza_data(self, valoare_parametru=""):
        zile_saptamana = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        luni_an = [
            "", "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", 
            "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"
        ]

        nume_zi = zile_saptamana[self.data.weekday()]
        zi_luna = self.data.day
        nume_luna = luni_an[self.data.month]
        an = self.data.year
        
        data_formatata = f"{nume_zi}, {zi_luna} {nume_luna} {an}"
        ora_curenta = self.data.strftime("%H:%M:%S")

        if valoare_parametru == "zi":
            text_afisat = f"Data: {data_formatata}"
        elif valoare_parametru == "timp":
            text_afisat = f"ora {ora_curenta}"
        else:
            text_afisat = f"Data: {data_formatata}, ora {ora_curenta}"

        html_sectiune = f"""
        <section>
            <h2>Data și ora</h2>
            <p>{text_afisat}</p>
        </section>
        """
        return html_sectiune
    
    def __str__(self):
        rezultat = (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data()}\n"
            f"lista_parametri: {self.lista_parametri()}\n"
            "------------------------------------------------"
        )
        return rezultat

def index(request):
    trimite_email()
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    print(accesare_curenta)
    messages.info(request, "Bine ai venit pe Zbor & Dor! Explorează cele mai noi oferte de vacanță.")
    messages.debug(request, f"[Sistem] Sesiune inițializată pentru IP-ul: {accesare_curenta.ip_client}")
    return render(request, 'aplicatie_agentie_turism/index.html')

def info(request):
    
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    
    print(accesare_curenta)

    valoare_parametru_data = request.GET.get("data", "")
    sectiune_html_generata = accesare_curenta.calculeaza_data(valoare_parametru_data)
    return render(request, 'aplicatie_agentie_turism/info.html', {'sectiune_html': sectiune_html_generata})

def log_accesari(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )

    istoric = Accesare.istoric_accesari

    continut_html = "<h1>Log Accesări</h1>"
   
    parametri_primiti = request.GET.keys()
    continut_html += f"<section><h2>Parametri primiți ({len(parametri_primiti)})</h2><ul>"
    for p in parametri_primiti:
        continut_html += f"<li>{p}</li>"
    continut_html += "</ul></section>"

    lista_iduri_brut = request.GET.getlist('iduri')
    if lista_iduri_brut:
        iduri_procesate = []
        for grup in lista_iduri_brut:
            iduri_procesate.extend(grup.split(','))
        
        dubluri = request.GET.get('dubluri', 'false').lower() == 'true'
        
        istoric_filtrat = []
        iduri_vazute = set()
        
        for id_str in iduri_procesate:
            if id_str.isdigit():
                id_cautat = int(id_str)
                if not dubluri and id_cautat in iduri_vazute:
                    continue
                
                for acc in istoric:
                    if acc.id == id_cautat:
                        istoric_filtrat.append(acc)
                        iduri_vazute.add(id_cautat)
                        break
        istoric = istoric_filtrat 

    ultimele = request.GET.get('ultimele')
    if ultimele:
        if ultimele.isdigit():
            n = int(ultimele)
            if n > len(istoric):
                continut_html += f"<p style='color:red;'>Exista doar {len(istoric)} accesari fata de {n} accesari cerute.</p>"
                messages.warning(request, f"Ai solicitat {n} accesări, dar există doar {len(istoric)} în sistem. Le-am afișat pe toate.")
            else:
                istoric = istoric[-n:]
        else:
            continut_html += "<p style='color:red;'>Eroare: Parametrul 'ultimele' trebuie să fie un număr întreg.</p>"

    accesari_param = request.GET.get('accesari')
    if accesari_param == 'nr':
        continut_html += f"<section><h2>Total accesări de la pornirea serverului: {len(Accesare.istoric_accesari)}</h2></section>"
    elif accesari_param == 'detalii':
        continut_html += "<section><h2>Detalii Accesări (Data și Ora)</h2><ul>"
        for acc in istoric:
            continut_html += f"<li>Momentul accesarii cu ID-ul {acc.id}: {acc.data.strftime('%d/%m/%Y %H:%M:%S')}</li>"
        continut_html += "</ul></section>"

    tabel_param = request.GET.get('tabel')
    if tabel_param:
        continut_html += "<section><h2>Tabel Accesări</h2><table border='1'><tr>"
        coloane = ['id', 'ip_client', 'url', 'data'] if tabel_param == 'tot' else tabel_param.split(',')
        
        for col in coloane:
            continut_html += f"<th>{col}</th>"
        continut_html += "</tr>"
        
        for acc in istoric:
            continut_html += "<tr>"
            for col in coloane:
                if col == 'id': 
                    continut_html += f"<td>{acc.id}</td>"
                elif col == 'ip_client': 
                    continut_html += f"<td>{acc.ip_client}</td>"
                elif col == 'url': 
                    continut_html += f"<td>{acc.string_url()}</td>"
                elif col == 'data': 
                    continut_html += f"<td>{acc.data.strftime('%d/%m/%Y %H:%M')}</td>"
                else: 
                    continut_html += "<td>N/A</td>"
            continut_html += "</tr>"
        continut_html += "</table></section>"
    else:
        continut_html += "<section><h2>Lista Accesări</h2><ul>"
        for acc in istoric:
            continut_html += f"<li>ID: {acc.id}, Pagina: {acc.pagina()}, IP: {acc.ip_client}</li>"
        continut_html += "</ul></section>"

    frecvente = {}
    for acc in Accesare.istoric_accesari:
        pag = acc.pagina()
        frecvente[pag] = frecvente.get(pag, 0) + 1
        
    if frecvente:
        pag_max = max(frecvente, key=frecvente.get)
        pag_min = min(frecvente, key=frecvente.get)
        continut_html += f"<section><h3>Statistici Pagină</h3>"
        continut_html += f"<p>Cea mai accesată pagină: <b>{pag_max}</b> ({frecvente[pag_max]} accesări)</p>"
        continut_html += f"<p>Cea mai puțin accesată pagină: <b>{pag_min}</b> ({frecvente[pag_min]} accesări)</p></section>"

    messages.debug(request, f"[Sistem] Am generat log-ul pentru {len(istoric)} înregistrări.")

    return render(request, 'aplicatie_agentie_turism/log.html', {'continut_log': continut_html})

def istoric_site(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    return render(request, 'aplicatie_agentie_turism/istoric.html')

def despre(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    messages.info(request, "Suntem o echipă de pasionați gata să îți planifice următoarea aventură.")
    return render(request, 'aplicatie_agentie_turism/despre.html')

def detalii_accesare(request, id):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    for acc in Accesare.istoric_accesari:
        if str(acc.id) == id:
            html = f"<h1>Detalii Accesare ID: {acc.id}</h1>"
            html += f"<p>IP Client: {acc.ip_client}</p><p>URL: {acc.string_url()}</p>"
            html += f"<p>{acc.calculeaza_data()}</p><p>Parametri: {acc.lista_parametri()}</p>"
            messages.success(request, f"Detaliile pentru accesarea cu ID-ul {id} au fost încărcate corect din memorie.")
            return render(request, 'aplicatie_agentie_turism/detalii_accesare.html', {'continut_detalii': html})
            
    messages.error(request, f"Eroare critică: Accesarea cu ID-ul {id} nu există în baza noastră de date temporară!")
    return render(request, 'aplicatie_agentie_turism/index.html')

def in_lucru(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    messages.warning(request, "Atenție! Această pagină este încă în construcție! Reveniți mai târziu pentru a descoperi conținutul complet.")
    return render(request, 'aplicatie_agentie_turism/in_lucru.html')

from .models import ServiciuIndividual, CategorieServiciu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def servicii_turism(request):
    nrPagina=request.GET.get("pagina", 1)
    produse=ServiciuIndividual.objects.all()
    paginator = Paginator(produse, 5)
    try:
        obPagina = paginator.page(nrPagina)
        messages.success(request, f"Catalogul de servicii a fost actualizat. Vizualizezi pagina {nrPagina}.")
    except EmptyPage:
        obPagina=None
        messages.error(request, "Nu mai există produse pe această pagină. Ai depășit limita catalogului.")
    except PageNotAnInteger:
        obPagina=None
        messages.error(request, "Numărul de pagină introdus în URL este invalid. Te rugăm să folosești butoanele de navigare.")
    return render(request, 'aplicatie_agentie_turism/servicii_turism.html', {'pagina': obPagina})

def _filtreaza_produse(produse, d, taguri_url):
    """Aplica pe QuerySet filtrele din formular"""
    if d.get('nume'):
        produse = produse.filter(nume_serviciu__icontains=d['nume'])
    if d.get('facilitati'):
        produse = produse.filter(facilitati_incluse__icontains=d['facilitati'])
    if d.get('pret_min') is not None:
        produse = produse.filter(pret_serviciu__gte=d['pret_min'])
    if d.get('pret_max') is not None:
        produse = produse.filter(pret_serviciu__lte=d['pret_max'])
    if d.get('rating_min') is not None:
        produse = produse.filter(rating__gte=d['rating_min'])
    if d.get('rating_max') is not None:
        produse = produse.filter(rating__lte=d['rating_max'])
    if d.get('stoc_min') is not None:
        produse = produse.filter(stoc_locuri__gte=d['stoc_min'])
    if d.get('stoc_max') is not None:
        produse = produse.filter(stoc_locuri__lte=d['stoc_max'])
    if d.get('activ') == 'da':
        produse = produse.filter(este_activ=True)
    elif d.get('activ') == 'nu':
        produse = produse.filter(este_activ=False)
    if d.get('prestat_de_la'):
        produse = produse.filter(data_prestare__gte=d['prestat_de_la'])
    if d.get('prestat_pana_la'):
        produse = produse.filter(data_prestare__lte=d['prestat_pana_la'])
    if d.get('adaugat_de_la'):
        produse = produse.filter(data_adaugare__date__gte=d['adaugat_de_la'])
    if d.get('adaugat_pana_la'):
        produse = produse.filter(data_adaugare__date__lte=d['adaugat_pana_la'])
    if d.get('categorie'):
        produse = produse.filter(id_categorie=d['categorie'])
    if d.get('furnizor'):
        produse = produse.filter(id_furnizor=d['furnizor'])
    taguri = list(dict.fromkeys(list(d.get('taguri') or []) + taguri_url))
    if taguri:
        produse = produse.filter(taguri__contains=taguri)
    return produse


def lista_produse(request, nume_categorie=None):
    # Pagina unei categorii sau pagina tuturor produselor
    if nume_categorie:
        categorie_curenta = get_object_or_404(CategorieServiciu, nume=nume_categorie)
    else:
        categorie_curenta = None
    produse = ServiciuIndividual.objects.select_related('id_categorie')
    if categorie_curenta:
        produse = produse.filter(id_categorie=categorie_curenta)

    # Formularul se considera trimis daca in URL apare vreunul din campurile lui
    campuri_form = set(FiltrareProduseForm.base_fields)
    trimis = any(k in request.GET for k in campuri_form)
    date_form = request.GET.copy()
    if categorie_curenta and 'categorie' not in date_form:
        date_form['categorie'] = categorie_curenta.nume     
    form = FiltrareProduseForm(date_form if trimis else None, categorie_curenta=categorie_curenta)

    valid = True
    if trimis:
        valid = form.is_valid()
        # verificare server: categoria de pe pagina nu poate fi schimbata din browser
        if categorie_curenta and 'categorie' in form.cleaned_data:
            ales = form.cleaned_data['categorie']
            if ales != categorie_curenta:
                valid = False
                form.add_error('categorie', 'Categoria nu poate fi modificată pe această pagină.')
                messages.error(
                    request, 'Valoarea categoriei a fost modificată manual. '
                             'Se afișează produsele categoriei curente, fără filtre.')
        if not valid:
            messages.error(request, 'Filtrele conțin erori. Corectați-le și încercați din nou.')

    date = form.cleaned_data if (trimis and valid) else {}
    col_param = date.get('col') or request.GET.get('col') or 'nume'
    sort_param = date.get('sort') or request.GET.get('sort') or 'a'
    coloane_permise = {'nume': 'nume_serviciu', 'pret': 'pret_serviciu', 'rating': 'rating'}
    camp_sortare = coloane_permise.get(col_param, 'nume_serviciu')
    if sort_param == 'd':
        camp_sortare = f"-{camp_sortare}"

    taguri_active = list(dict.fromkeys(request.GET.getlist('tag')))
    produse = _filtreaza_produse(produse, date, taguri_active).order_by(camp_sortare)

    taguri_active_info = []
    for tag in taguri_active:
        params_fara_tag = request.GET.copy()
        taguri_ramase = [t for t in taguri_active if t != tag]
        params_fara_tag.setlist('tag', taguri_ramase)
        url_eliminare = f"?{params_fara_tag.urlencode()}" if params_fara_tag else request.path
        taguri_active_info.append({'nume': tag, 'url_eliminare': url_eliminare})

    query_curent = request.GET.urlencode()

    # Paginare: numarul de produse pe pagina (din formular)
    nr_pe_pagina = date.get('nr_pe_pagina') or IMPLICIT_PE_PAGINA
    nr_coloane = date.get('nr_coloane') or IMPLICIT_COLOANE
    if valid:   
        anterior = request.session.get('nr_pe_pagina', IMPLICIT_PE_PAGINA)
        if anterior != nr_pe_pagina:
            messages.warning(
                request, 'Ați schimbat numărul de produse pe pagină. În urma repaginării este posibil '
                         'să fi sărit peste unele produse sau să le revedeți pe cele deja vizualizate.')
        request.session['nr_pe_pagina'] = nr_pe_pagina
    paginator = Paginator(produse, nr_pe_pagina)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    query_fara_page = params.urlencode()

    context = {
        'form': form,
        'filtrat': trimis and valid,
        'page_obj': page_obj,
        'nr_coloane': nr_coloane,
        'col_curent': col_param,
        'sort_curent': sort_param,
        'stoc_min': settings.STOC_MIN,
        'taguri_active': taguri_active,
        'taguri_active_info': taguri_active_info,
        'query_curent': query_curent,
        'query_fara_page': query_fara_page,
        'categorie_curenta': categorie_curenta,
        'url_baza': request.path,
    }

    # Bonus: cererile trimise cu fetch primesc doar partile care se schimba (JSON)
    if request.headers.get('X-Requested-With') == 'fetch':
        raspuns = JsonResponse({
            'formular': render_to_string(
                'aplicatie_agentie_turism/_filtrare_form.html', context, request=request),
            'continut': render_to_string(
                'aplicatie_agentie_turism/_produse_continut.html', context, request=request),
            'mesaje': [{'text': str(m), 'tip': m.tags} for m in messages.get_messages(request)],
        })
        patch_vary_headers(raspuns, ('X-Requested-With',))   
        add_never_cache_headers(raspuns)
        return raspuns
    return render(request, 'aplicatie_agentie_turism/lista_produse.html', context)


def detalii_produs(request, pk):
    # Tratez cazul în care se accesează un produs inexistent
    try:
        produs = ServiciuIndividual.objects.select_related('id_categorie', 'id_furnizor').get(pk=pk)
    except ServiciuIndividual.DoesNotExist:
        # Se returneaza o pagina de eroare cu status 404
        return render(request, 'aplicatie_agentie_turism/eroare_produs.html', {'id_cautat': pk}, status=404)

    # Selectez aleator 3 produse din aceeasi categorie 
    K = 3
    produse_similare = (
        ServiciuIndividual.objects
        .filter(id_categorie=produs.id_categorie)
        .exclude(pk=produs.pk)
        .order_by('?')[:K]
    )

    context = {
        'produs': produs,
        'produse_similare': produse_similare,
        'stoc_min': settings.STOC_MIN,
    }
    return render(request, 'aplicatie_agentie_turism/detalii_produs.html', context)


O_ZI = 24 * 60 * 60  # secunde


def _log_accesare(request):
    """Inregistreaza accesarea in istoric"""
    return Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )


def _salveaza_in_sesiune(request, utilizator):
    """Memoreaza in sesiune datele utilizatorului si ale profilului"""
    profil = Profil.objects.filter(utilizator=utilizator).first()
    request.session['date_utilizator'] = {
        'username': utilizator.username,
        'first_name': utilizator.first_name,
        'last_name': utilizator.last_name,
        'email': utilizator.email,
        'telefon': utilizator.telefon,
        'data_nasterii': utilizator.data_nasterii.strftime('%d.%m.%Y') if utilizator.data_nasterii else '',
        'gen': utilizator.get_gen_display(),
        'data_inregistrarii': utilizator.date_joined.strftime('%d.%m.%Y %H:%M'),
    }
    request.session['date_profil'] = (
        {
            'judet': profil.judet,
            'strada': profil.strada,
            'cod_postal': profil.cod_postal,
            'tara': profil.tara,
        }
        if profil else None
    )


def inregistrare_view(request):
    _log_accesare(request)
    if request.user.is_authenticated:
        return redirect('profil')
    form = InregistrareForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        utilizator = form.save()
        form.salveaza_profil(utilizator)  # Profil se creeaza doar daca s-a completat ceva
        messages.success(request, "Cont creat cu succes. Vă puteți autentifica.")
        return redirect('login')
    return render(request, 'aplicatie_agentie_turism/formular.html', {
        'titlu': 'Înregistrare', 'form': form, 'buton': 'Creează cont',
    })


def login_view(request):
    _log_accesare(request)
    if request.user.is_authenticated:
        return redirect('profil')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        utilizator = form.get_user()
        login(request, utilizator)
        # bifat -> sesiune de o zi; nebifat -> expira la inchiderea browserului
        request.session.set_expiry(O_ZI if form.cleaned_data['ramane_logat'] else 0)
        _salveaza_in_sesiune(request, utilizator)
        next_url = request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('profil')
    return render(request, 'aplicatie_agentie_turism/formular.html', {
        'titlu': 'Autentificare', 'form': form, 'buton': 'Login',
    })


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Ați fost deconectat.")
    return redirect('login')


@login_required
def profil_view(request):
    _log_accesare(request)
    if 'date_utilizator' not in request.session:
        _salveaza_in_sesiune(request, request.user)
    return render(request, 'aplicatie_agentie_turism/profil.html', {
        'date_utilizator': request.session['date_utilizator'],
        'date_profil': request.session.get('date_profil'),
    })


@login_required
def editare_date_view(request):
    _log_accesare(request)
    utilizator = Utilizator.objects.get(pk=request.user.pk)
    form = EditareDateForm(request.POST or None, instance=utilizator)
    if request.method == 'POST' and form.is_valid():
        utilizator = form.save()
        form.salveaza_profil(utilizator)  # creeaza sau actualizeaza Profil
        _salveaza_in_sesiune(request, utilizator)
        messages.success(request, "Datele au fost actualizate.")
        return redirect('profil')
    return render(request, 'aplicatie_agentie_turism/formular.html', {
        'titlu': 'Modifică datele', 'form': form, 'buton': 'Salvează',
    })


@login_required
def schimba_parola_view(request):
    _log_accesare(request)
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        utilizator = form.save()
        update_session_auth_hash(request, utilizator)  # ramane logat dupa schimbare
        messages.success(request, "Parola a fost schimbată.")
        return redirect('profil')
    return render(request, 'aplicatie_agentie_turism/formular.html', {
        'titlu': 'Schimbă parola', 'form': form, 'buton': 'Schimbă parola',
    })




# Task 3 / lab. 5: pagina de contact 
def contact(request):
    _log_accesare(request)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            date_mesaj, imagini = pregateste_date(form.cleaned_data, form.tip_ales(), get_ip(request))
            salveaza_mesaj(date_mesaj, imagini)
            messages.success(
                request, 'Mesajul a fost trimis. Veți primi un răspuns în numărul de zile precizat.')
            if date_mesaj['urgent']:
                messages.info(request, 'Mesajul a fost marcat ca urgent.')
            return redirect('contact')
        messages.error(request, 'Mesajul nu a fost trimis: formularul conține erori.')
    else:
        form = ContactForm()
    return render(request, 'aplicatie_agentie_turism/contact.html', {
        'form': form,
        'mapare': form.mapare_departamente(),
    })


def _este_personal(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(_este_personal, login_url='login')
def mesaje(request, departament=None, an=None, luna=None, zi=None):
    """/mesaje/<departament>/<an>/<luna>/<zi>/ - luna si ziua sunt optionale."""
    _log_accesare(request)
    asigura_foldere_departamente()
    if departament is None:
        return render(request, 'aplicatie_agentie_turism/mesaje.html', {
            'departamente': [(d.nume_departament, nume_folder(d.nume_departament))
                             for d in Departament.objects.filter(
                                 tipuri_mesaje__isnull=False).distinct().order_by('nume_departament')],
        })
    dep = departament_dupa_folder(departament)
    if dep is None:
        raise Http404('Departament inexistent.')
    if luna is not None and not 1 <= luna <= 12:
        raise Http404('Lună invalidă.')
    if zi is not None and not 1 <= zi <= 31:
        raise Http404('Zi invalidă.')

    lista = []
    for m in incarca_mesaje(dep, an, luna, zi):
        # afisare independenta de numarul si numele campurilor din JSON
        campuri = []
        for cheie, valoare in m.items():
            if cheie.startswith('_'):
                continue
            if cheie == 'mesaj':
                valoare = mark_safe(valoare)          # HTML generat (si escapat) la salvare
            elif cheie == 'imagini':
                pass                                  # lista de fisiere: sablonul afiseaza miniaturi
            elif isinstance(valoare, bool):
                valoare = 'Da' if valoare else 'Nu'
            elif isinstance(valoare, list):
                valoare = ', '.join(str(x) for x in valoare) or '–'
            elif valoare in (None, ''):
                valoare = '–'
            campuri.append((cheie.replace('_', ' ').capitalize(), cheie, valoare))
        lista.append({'campuri': campuri, 'urgent': m.get('urgent'), 'tip': m.get('tip_mesaj', '')})
    perioada = '/'.join(str(x) for x in (an, luna, zi) if x is not None)
    return render(request, 'aplicatie_agentie_turism/mesaje.html', {
        'departament': dep, 'folder': departament, 'mesaje': lista, 'perioada': perioada,
    })


@user_passes_test(_este_personal, login_url='login')
def imagine_mesaj(request, departament, nume):
    if not RE_NUME_IMAGINE.match(nume) or departament_dupa_folder(departament) is None:
        raise Http404()
    cale = RADACINA / departament / nume
    if not cale.is_file():
        raise Http404()
    return FileResponse(open(cale, 'rb'))


# Task 4 / lab. 5: formular de adaugare produse 
@login_required
def adauga_produs(request):
    _log_accesare(request)
    form = ProdusForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        produs = form.save(commit=False)          # preiau inputurile aditionale inainte de salvare
        achizitie = form.cleaned_data['pret_achizitie']
        adaos = form.cleaned_data['adaos_comercial']
        produs.pret_serviciu = (achizitie * (1 + adaos / Decimal(100))).quantize(Decimal('0.01'))
        produs.save()
        form.save_m2m()
        messages.success(
            request, f'Serviciul „{produs.nume_serviciu}” a fost adăugat, la prețul de {produs.pret_serviciu} EUR.')
        return redirect(produs.get_absolute_url())
    return render(request, 'aplicatie_agentie_turism/formular.html', {
        'titlu': 'Adaugă un serviciu', 'form': form, 'buton': 'Adaugă serviciul',
    })
