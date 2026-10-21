from django.shortcuts import render
from django.http import HttpResponse
import datetime

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
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    print(accesare_curenta)
    return HttpResponse("Agenția dispune de un catalog variat de " \
    "oferte turistice către destinații din întreaga lume. Clienții " \
    "au posibilitatea să achiziționeze bilete pentru un sejur complet "
    "(transport, cazare etc) sau servicii individuale ale agenției (de " \
    "exemplu, accesul ghidat în cadrul unui obiectiv turistic).")

def info(request):
    
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    
    print(accesare_curenta)

    valoare_parametru_data = request.GET.get("data", "")
    sectiune_html_generata = accesare_curenta.calculeaza_data(valoare_parametru_data)

    html_baza = """
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Informații despre server</title>
    </head>
    <body>
        <h1>Informații despre server</h1>
    """
    html_final = html_baza + sectiune_html_generata + "</body>\n</html>"
    
    return HttpResponse(html_final)

def log_accesari(request):

    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )

    istoric = Accesare.istoric_accesari
    html = "<!DOCTYPE html><html lang='ro'><head><meta charset='UTF-8'>" \
            "<title>Log Accesări</title></head><body><h1>Log Accesări</h1>"
   
    parametri_primiti = request.GET.keys()
    html += f"<section><h2>Parametri primiți ({len(parametri_primiti)})</h2><ul>"
    for p in parametri_primiti:
        html += f"<li>{p}</li>"
    html += "</ul></section>"

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
                html += f"<p style='color:red;'>Exista doar {len(istoric)} accesari fata de {n} accesari cerute.</p>"
            else:
                istoric = istoric[-n:]
        else:
            html += "<p style='color:red;'>Eroare: Parametrul 'ultimele' trebuie să fie un număr întreg.</p>"

    accesari_param = request.GET.get('accesari')
    if accesari_param == 'nr':
        html += f"<section><h2>Total accesări de la pornirea serverului: {len(Accesare.istoric_accesari)}</h2></section>"
    elif accesari_param == 'detalii':
        html += "<section><h2>Detalii Accesări (Data și Ora)</h2><ul>"
        for acc in istoric:
            html += f"<li>Momentul accesarii cu ID-ul {acc.id}: {acc.data.strftime('%d/%m/%Y %H:%M:%S')}</li>"
        html += "</ul></section>"

    tabel_param = request.GET.get('tabel')
    if tabel_param:
        html += "<section><h2>Tabel Accesări</h2><table border='1'><tr>"
        coloane = ['id', 'ip_client', 'url', 'data'] if tabel_param == 'tot' else tabel_param.split(',')
        
        for col in coloane:
            html += f"<th>{col}</th>"
        html += "</tr>"
        
        for acc in istoric:
            html += "<tr>"
            for col in coloane:
                if col == 'id': 
                    html += f"<td>{acc.id}</td>"
                elif col == 'ip_client': 
                    html += f"<td>{acc.ip_client}</td>"
                elif col == 'url': 
                    html += f"<td>{acc.string_url()}</td>"
                elif col == 'data': 
                    html += f"<td>{acc.data.strftime('%d/%m/%Y %H:%M')}</td>"
                else: 
                    html += "<td>N/A</td>"
            html += "</tr>"
        html += "</table></section>"
    else:
        html += "<section><h2>Lista Accesări</h2><ul>"
        for acc in istoric:
            html += f"<li>ID: {acc.id}, Pagina: {acc.pagina()}, IP: {acc.ip_client}</li>"
        html += "</ul></section>"

    frecvente = {}
    for acc in Accesare.istoric_accesari:
        pag = acc.pagina()
        frecvente[pag] = frecvente.get(pag, 0) + 1
        
    if frecvente:
        pag_max = max(frecvente, key=frecvente.get)
        pag_min = min(frecvente, key=frecvente.get)
        html += f"<section><h3>Statistici Pagină</h3>"
        html += f"<p>Cea mai accesată pagină: <b>{pag_max}</b> ({frecvente[pag_max]} accesări)</p>"
        html += f"<p>Cea mai puțin accesată pagină: <b>{pag_min}</b> ({frecvente[pag_min]} accesări)</p></section>"

    html += "</body></html>"
    return HttpResponse(html)

def istoric_site(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    return HttpResponse("<h1>Istoric Agenție</h1><p>Aceasta este pagina de istoric.</p>")

def despre(request):
    accesare_curenta = Accesare(
        ip_client=get_ip(request),
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    return HttpResponse("<h1>Despre Noi</h1><p>Conținut despre echipă.</p>")

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
            return HttpResponse(html)
            
    return HttpResponse("<h1 style='color:red;'>Accesarea nu a fost găsită!</h1>")