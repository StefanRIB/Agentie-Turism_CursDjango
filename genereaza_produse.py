import random
from datetime import datetime, timedelta

tabel_furnizori = "aplicatie_agentie_turism_furnizor"
tabel_servicii = "aplicatie_agentie_turism_serviciuindividual"

destinatii_logice = [
    {
        "id_categorie": 1, # Vacanta All Inclusive
        "locatii": [("Antalya", "Turcia"), ("Tenerife", "Spania"), ("Maldive", "Exotic"), ("Punta Cana", "Exotic")],
        "servicii": ["Sejur 7 nopți All-Inclusive", "Pachet relaxare resort 5 stele", "Vacanță exotică All-Inclusive", "Sejur de lux 10 zile", "All-Inclusive Premium Resort"],
        "facilitati": ["Băuturi și mese incluse", "Acces SPA și piscină", "Transfer VIP de la aeroport", "Asigurare medicală premium"]
    },
    {
        "id_categorie": 2, # City Break
        "locatii": [("Roma", "Italia"), ("Florența", "Italia"), ("Bruxelles", "Belgia"), ("Munchen", "Germania"), ("Paris", "Franța"), ("Londra", "UK")],
        "servicii": ["City Break Cultural", "Tur ghidat in centrul istoric", "Bilet intrare muzeu", "Pachet City Break 3 nopți", "Escapadă romantică de weekend", "Tur gastronomic local"],
        "facilitati": ["Mic dejun inclus", "Ghid local autorizat", "WiFi gratuit", "Fără facilități suplimentare"]
    },
    {
        "id_categorie": 3, # Transport
        "locatii": [("București", "România"), ("Milano", "Italia"), ("Frankfurt", "Germania"), ("Madrid", "Spania")],
        "servicii": ["Zbor direct", "Bilet tren rapid", "Transfer VIP aeroport", "Închiriere mașină de lux", "Bilet tren Clasa 1", "Zbor cursă de linie premium"],
        "facilitati": ["Bagaj de cală inclus", "Check-in prioritar", "Băuturi incluse pe durata călătoriei", "Fără facilități suplimentare"]
    },
    {
        "id_categorie": 4, # Aventură și Adrenalină
        "locatii": [("Sinaia", "România"), ("Livigno", "Italia"), ("Innsbruck", "Austria"), ("Chamonix", "Franța")],
        "servicii": ["Excursie montană extremă", "Drumeție ghidată pe creastă", "Sesiune de Alpinism", "Zbor cu parapanta", "Traseu mountain bike", "Pachet camping și supraviețuire"],
        "facilitati": ["Echipament de protecție inclus", "Ghid montan autorizat", "Asigurare de risc extrem", "Transport spre traseu"]
    },
    {
        "id_categorie": 5, # Croaziere de Lux
        "locatii": [("Cinque Terre", "Italia"), ("Camogli", "Italia"), ("Barcelona", "Spania"), ("Atena", "Grecia"), ("Nisa", "Franța")],
        "servicii": ["Croazieră la apus", "O zi pe mare", "Croazieră de lux 5 zile", "Tur privat cu iahtul", "Croazieră pe Mediterana 7 zile", "Închiriere catamaran cu echipaj"],
        "facilitati": ["Cină festivă cu specific local", "Băuturi incluse", "Acces la puntea VIP", "Asigurare medicală premium"]
    }
]

furnizori_noi = [
    (1001, "Wizz Air", "contact@wizzair.com", "https://wizzair.com", "+36111222333", ["Global"]),
    (1002, "Resort & Spa International", "rezervari@resort.com", "https://resort.com", "+1800555000", ["Global", "Exotic", "Turcia", "Spania"]),
    (1003, "CFR Călători", "contact@cfr.ro", "https://cfrcalatori.ro", "+40219521", ["România"]),
    (1004, "Trenitalia", "contact@trenitalia.it", "https://trenitalia.it", "+39066847", ["Italia"]),
    (1005, "Deutsche Bahn", "contact@bahn.de", "https://bahn.de", "+49302970", ["Germania"]),
    (1006, "SNCF", "contact@sncf.fr", "https://sncf.fr", "+33184943", ["Franța"]),
    (1007, "Ghid Local Italia", "ghid@italia.it", "https://italia.it", "+3934012345", ["Italia"]),
    (1008, "Carpați Alpinism", "aventura@carpati.ro", "https://carpati.ro", "+40722123456", ["România"]),
    (1009, "Hellenic Seaways", "contact@hsw.gr", "https://hsw.gr", "+30210419", ["Grecia"]),
    (1010, "Eurostar", "contact@eurostar.com", "https://eurostar.com", "+4412345678", ["UK", "Franța", "Belgia"])
]

with open("insert_produse.sql", "w", encoding="utf-8") as fisier:
    fisier.write("-- Script generat pentru Task-ul Bonus (Laborator 4)\n")
    fisier.write("BEGIN;\n\n")

    # Mai intai inserez furnizorii 
    fisier.write("-- 1. Inserare Furnizori Generați\n")
    for furnizor_id, nume, email, site, telefon, _ in furnizori_noi:
        comanda = f"INSERT INTO {tabel_furnizori} (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES ({furnizor_id}, '{nume}', '{email}', '{site}', '{telefon}') ON CONFLICT (id) DO NOTHING;\n"
        fisier.write(comanda)

    fisier.write("\n-- 2. Inserare 50 de Servicii (Produse) Unice\n")
    
    pachete_generate = set() 
    pachete_dorite = 50
    pachete_create = 0
    
    # Bucla prin care se genereaza cele 50 de produse distincte
    while pachete_create < pachete_dorite:
        profil = random.choice(destinatii_logice)
        locatie = random.choice(profil["locatii"])
        oras = locatie[0]
        tara = locatie[1]
        tip_serviciu = random.choice(profil["servicii"])
        
        # Cheie unica pentru a evita duplicarea serviciilor
        semnatura_pachet = f"{tip_serviciu} - {oras}"
        
        if semnatura_pachet in pachete_generate:
            continue
            
        pachete_generate.add(semnatura_pachet)
        pachete_create += 1
        
        nume = f"{tip_serviciu} în {oras} (Pachet Premium)"
        pret = round(random.uniform(50.0, 2500.0), 2)
        stoc = random.randint(5, 50)
        este_activ = random.choice(['TRUE', 'FALSE'])
        facilitate = random.choice(profil["facilitati"])
        id_categorie = profil["id_categorie"] 
        rating = round(random.uniform(3.5, 5.0), 1)
        zi_aleatoare = random.randint(0, 300)
        data_adaugare = (datetime(2026, 1, 1) + timedelta(days=zi_aleatoare)).strftime('%Y-%m-%d')
        
        # Aleg un furnizor valid pentru zona geografica aferenta serviciului
        furnizori_valizi = [f for f in furnizori_noi if "Global" in f[5] or tara in f[5]]
        id_furnizor = random.choice(furnizori_valizi)[0]
        
        comanda_sql = f"INSERT INTO {tabel_servicii} (nume_serviciu, pret_serviciu, stoc_locuri, este_activ, facilitati_incluse, id_categorie_id, id_furnizor_id, rating, data_adaugare) VALUES ('{nume}', {pret}, {stoc}, {este_activ}, '{facilitate}', {id_categorie}, {id_furnizor}, {rating}, '{data_adaugare}');\n"
        fisier.write(comanda_sql)

    fisier.write("\nCOMMIT;\n")

print(f"Script generat cu succes! Au fost create {pachete_dorite} servicii unice, gata de inserare.")