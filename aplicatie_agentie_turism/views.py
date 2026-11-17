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
from .forms import InregistrareForm, LoginForm, EditareDateForm
from .models import Profil, Utilizator

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

def lista_produse(request, nume_categorie=None):
    
    # Verific daca ma aflu pe o pagina aferenta unei categorii
    if nume_categorie:
        categorie_curenta = get_object_or_404(CategorieServiciu, nume=nume_categorie)
        produse = ServiciuIndividual.objects.select_related('id_categorie').filter(id_categorie=categorie_curenta)
    else:
        categorie_curenta = None
        produse = ServiciuIndividual.objects.select_related('id_categorie').all()

    # Cod pentru sortare si filtrare dupa taguri
    col_param = request.GET.get('col', 'nume') 
    sort_param = request.GET.get('sort', 'a')  
    coloane_permise = {'nume': 'nume_serviciu', 'pret': 'pret_serviciu', 'rating': 'rating'}
    camp_sortare = coloane_permise.get(col_param, 'nume_serviciu')
    if sort_param == 'd':
        camp_sortare = f"-{camp_sortare}"

    taguri_active = list(dict.fromkeys(request.GET.getlist('tag')))
    if taguri_active:
        produse = produse.filter(taguri__contains=taguri_active)

    produse = produse.order_by(camp_sortare)

    taguri_active_info = []
    for tag in taguri_active:
        params_fara_tag = request.GET.copy()
        taguri_ramase = [t for t in taguri_active if t != tag]
        params_fara_tag.setlist('tag', taguri_ramase)
        url_eliminare = f"?{params_fara_tag.urlencode()}" if params_fara_tag else request.path
        taguri_active_info.append({'nume': tag, 'url_eliminare': url_eliminare})

    query_curent = request.GET.urlencode()

    # Cod pentru paginare
    paginator = Paginator(produse, settings.PROD_PER_PAG)
    numar_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numar_pagina)

    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    query_fara_page = params.urlencode()

    context = {
        'page_obj': page_obj,
        'col_curent': col_param,
        'sort_curent': sort_param,
        'stoc_min': settings.STOC_MIN,
        'taguri_active': taguri_active,
        'taguri_active_info': taguri_active_info,
        'query_curent': query_curent,
        'query_fara_page': query_fara_page,
        'categorie_curenta': categorie_curenta, 
    }
    
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
    """Inregistreaza accesarea in istoric, la fel ca celelalte pagini ale site-ului."""
    return Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )


def _salveaza_in_sesiune(request, utilizator):
    """Memoreaza in sesiune datele utilizatorului si ale profilului (valori serializabile JSON)."""
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