--
-- PostgreSQL database dump
--

\restrict NNuTqZs3zFcIpuytNxT5ywzw3pdgeem8FxLWqCQPEcms7sVzKEmmCWrqczle46Z

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: aplicatie_agentie_turism_ambalaj; Type: TABLE DATA; Schema: django; Owner: stefan
--



--
-- Data for Name: aplicatie_agentie_turism_categorieserviciu; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (6, 'Categorie Fara Produse', 'Categorie de Test pentru punctul 8 / Laboratorul 4 (Task QuerySets)', '#9C27B0', '', 'toti');
INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (4, 'Aventură și Adrenalină', 'Experiențe extreme precum rafting, parapantă, drumeții montane și tabere de supraviețuire.', '#FF9800', 'fa-solid fa-person-hiking', 'tineret');
INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (5, 'Croaziere de Lux', 'Călătorii premium pe mare sau ocean, cu servicii de înaltă calitate și opriri în porturi exotice.', '#9C27B0', 'fa-solid fa-ship', 'toti');
INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (3, 'Transport', 'Servicii individuale de mobilitate (bilete de avion, tren, închirieri auto sau transfer de la aeroport).', '#2196F3', 'fa-solid fa-train', 'toti');
INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (1, 'Vacante All-Inclusive', 'Pachete turistice complete cu cazare, zbor, mese și activități de divertisment, destinate părinților și copiilor.', '#4CAF50', 'fa-solid fa-umbrella-beach', 'familie');
INSERT INTO django.aplicatie_agentie_turism_categorieserviciu (id, nume, descriere, culoare, sigla, tip_public) VALUES (2, 'City Break', 'Escapade de weekend în marile capitale europene, cu cazare centrală și acces rapid la obiective turistice.', '#6c5ce7', 'fa-solid fa-city', 'cuplu');


--
-- Data for Name: aplicatie_agentie_turism_furnizor; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1, 'Wizz Air Hungary', 'contact@wizzair.com', 'https://wizzair.com', '+40311234567');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (2, 'Trenitalia SpA', 'info@trenitalia.it', 'https://www.trenitalia.com', '+390612345678');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (3, 'Hotel Colosseum Roma', 'booking@hotelcolosseum.it', 'https://hotelcolosseum.com', '+390643211234');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (4, 'ChocoTours Brussels', 'hello@chocotours.be', 'https://chocotours.be', '+3221234567');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (5, 'Cinque Terre Navigazione', 'info@navigazionecinqueterre.it', 'https://navigazionecinqueterre.it', '+390187123456');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (6, 'Hotel Ibis Milano Centrale', 'contact@ibis.com', 'https://ibismilanocentrale.com', '+390643211256');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1001, 'Wizz Air', 'contact@wizzair.com', 'https://wizzair.com', '+36111222333');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1002, 'Resort & Spa International', 'rezervari@resort.com', 'https://resort.com', '+1800555000');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1003, 'CFR Călători', 'contact@cfr.ro', 'https://cfrcalatori.ro', '+40219521');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1004, 'Trenitalia', 'contact@trenitalia.it', 'https://trenitalia.it', '+39066847');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1005, 'Deutsche Bahn', 'contact@bahn.de', 'https://bahn.de', '+49302970');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1006, 'SNCF', 'contact@sncf.fr', 'https://sncf.fr', '+33184943');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1007, 'Ghid Local Italia', 'ghid@italia.it', 'https://italia.it', '+3934012345');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1008, 'Carpați Alpinism', 'aventura@carpati.ro', 'https://carpati.ro', '+40722123456');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1009, 'Hellenic Seaways', 'contact@hsw.gr', 'https://hsw.gr', '+30210419');
INSERT INTO django.aplicatie_agentie_turism_furnizor (id, nume_furnizor, email_contact, site_web, telefon_contact) VALUES (1010, 'Eurostar', 'contact@eurostar.com', 'https://eurostar.com', '+4412345678');


--
-- Data for Name: aplicatie_agentie_turism_pachetsejur; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_pachetsejur (id, titlu_pachet, reducere_aplicata) VALUES (1, 'City Break la Roma', 15);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur (id, titlu_pachet, reducere_aplicata) VALUES (2, 'Degustare și Tradiție în Bruxelles', 10);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur (id, titlu_pachet, reducere_aplicata) VALUES (3, 'Magia Apusului în Cinque Terre', 12.5);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur (id, titlu_pachet, reducere_aplicata) VALUES (4, 'O zi pe mare in Cinque Terre', 6);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur (id, titlu_pachet, reducere_aplicata) VALUES (5, 'City Break Urban: Milano & Bergamo', 18);


--
-- Data for Name: aplicatie_agentie_turism_serviciuindividual; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (40, 'Croazieră de lux 5 zile în Atena (Pachet Premium)', 245.75, false, NULL, 4.5, 20, 'Băuturi incluse', '2026-10-10 00:00:00+03', 5, 1009, '{mare,grecia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (44, 'All-Inclusive Premium Resort în Tenerife (Pachet Premium)', 818.95, true, NULL, 4.1, 21, 'Transfer VIP de la aeroport', '2026-04-26 00:00:00+03', 1, 1002, '{mare,all-inclusive,spania}', 'servicii/tenerife.jpeg');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (49, 'Escapadă romantică de weekend în Roma (Pachet Premium)', 511.28, false, NULL, 3.8, 23, 'Mic dejun inclus', '2026-10-08 00:00:00+03', 2, 1004, '{"city break",italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (30, 'Închiriere catamaran cu echipaj în Barcelona (Pachet Premium)', 2081.45, true, NULL, 4.9, 10, 'Băuturi incluse', '2026-04-18 00:00:00+03', 5, 1002, '{mare,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (15, 'Sesiune de Alpinism în Chamonix (Pachet Premium)', 809.24, true, NULL, 3.9, 24, 'Transport spre traseu', '2026-04-11 00:00:00+03', 4, 1006, '{munte,franta}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (38, 'O zi pe mare în Atena (Pachet Premium)', 1922.66, true, NULL, 4.5, 39, 'Acces la puntea VIP', '2026-04-09 00:00:00+03', 5, 1001, '{mare,grecia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (43, 'Bilet tren rapid în Milano (Pachet Premium)', 2175.31, false, NULL, 4, 32, 'Check-in prioritar', '2026-08-05 00:00:00+03', 3, 1004, '{tren,transport,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (39, 'Tur gastronomic local în Munchen (Pachet Premium)', 1394.92, false, NULL, 3.8, 5, 'Fără facilități suplimentare', '2026-08-20 00:00:00+03', 2, 1001, '{gastronomie,germania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (6, 'Mic dejun tradițional italian', 15.00, true, '2026-10-29', 4.6, 30, 'Bufet suedez, Cafea espresso, Produse de patiserie', '2026-10-21 12:55:47.783851+03', 2, 3, '{gastronomie,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (9, 'Croazieră la apus în Cinque Terre', 90.00, true, '2027-07-21', 5, 13, 'Cina, Muzica live', '2026-10-21 13:03:02.257837+03', 5, 5, '{mare,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (45, 'Tur gastronomic local în Bruxelles (Pachet Premium)', 148.25, true, NULL, 4.4, 25, 'WiFi gratuit', '2026-07-08 00:00:00+03', 2, 1010, '{gastronomie,belgia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (26, 'Închiriere catamaran cu echipaj în Nisa (Pachet Premium)', 239.95, true, NULL, 4.7, 24, 'Cină festivă cu specific local', '2026-05-23 00:00:00+03', 5, 1001, '{mare,franta}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (1, 'Zbor direct București - Roma', 45.50, true, '2026-10-31', 4.2, 180, 'Bagaj de mână, Check-in online', '2026-10-21 12:42:22.437943+03', 3, 1, '{transport,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (24, 'City Break Cultural în Londra (Pachet Premium)', 420.72, true, NULL, 4.9, 29, 'Ghid local autorizat', '2026-10-24 00:00:00+03', 2, 1001, '{"city break",anglia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (5, 'Cazare 3 nopți Hotel Colosseum', 320.00, false, '2026-10-24', 4.7, 15, 'Cameră dublă, Vedere la oraș, Baie privată', '2026-10-21 12:54:11.841949+03', 2, 3, '{"city break",italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (29, 'City Break Cultural în Bruxelles (Pachet Premium)', 715.58, false, NULL, 4.2, 15, 'Mic dejun inclus', '2026-08-15 00:00:00+03', 2, 1002, '{"city break",belgia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (21, 'Vacanță exotică All-Inclusive în Tenerife (Pachet Premium)', 778.15, false, NULL, 3.8, 46, 'Asigurare medicală premium', '2026-10-15 00:00:00+03', 1, 1001, '{mare,all-inclusive,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (41, 'City Break Cultural în Roma (Pachet Premium)', 1212.44, false, NULL, 4.7, 41, 'Fără facilități suplimentare', '2026-02-10 00:00:00+02', 2, 1007, '{"city break",italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (4, 'Bilet tren regional Bergamo - Milano', 6.00, true, '2026-10-21', 4.7, 500, 'Loc la geam', '2026-10-21 12:53:05.962855+03', 3, 2, '{tren,transport,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (34, 'Tur privat cu iahtul în Cinque Terre (Pachet Premium)', 2119.52, false, NULL, 4.3, 34, 'Cină festivă cu specific local', '2026-03-31 00:00:00+03', 5, 1007, '{mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (32, 'Excursie montană extremă în Innsbruck (Pachet Premium)', 1865.96, true, NULL, 4.4, 17, 'Ghid montan autorizat', '2026-08-06 00:00:00+03', 4, 1002, '{munte,austria}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (36, 'Zbor direct în Madrid (Pachet Premium)', 1842.59, true, NULL, 4.8, 31, 'Fără facilități suplimentare', '2026-09-19 00:00:00+03', 3, 1002, '{transport,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (42, 'Zbor cu parapanta în Innsbruck (Pachet Premium)', 1397.22, false, NULL, 3.7, 43, 'Echipament de protecție inclus', '2026-08-06 00:00:00+03', 4, 1001, '{munte,austria}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (33, 'Zbor cursă de linie premium în Madrid (Pachet Premium)', 1011.22, false, NULL, 4.7, 10, 'Fără facilități suplimentare', '2026-06-29 00:00:00+03', 3, 1002, '{transport,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (27, 'Zbor cursă de linie premium în Frankfurt (Pachet Premium)', 145.16, true, NULL, 3.9, 11, 'Bagaj de cală inclus', '2026-10-20 00:00:00+03', 3, 1002, '{germania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (18, 'Sejur de lux 10 zile în Punta Cana (Pachet Premium)', 2319.91, false, NULL, 4.6, 15, 'Băuturi și mese incluse', '2026-04-08 00:00:00+03', 1, 1002, '{mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (10, 'Plimbare cu Skijet in Cinque Terre', 100.00, true, '2027-04-09', 4.8, 10, 'Skijet, Vesta salvare', '2026-10-21 13:05:13.028597+03', 4, 5, '{mare,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (28, 'Zbor cu parapanta în Livigno (Pachet Premium)', 907.16, true, NULL, 4.5, 10, 'Ghid montan autorizat', '2026-10-11 00:00:00+03', 4, 1002, '{munte}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (17, 'Excursie montană extremă în Livigno (Pachet Premium)', 966.96, true, NULL, 4.6, 29, 'Echipament de protecție inclus', '2026-08-04 00:00:00+03', 4, 1002, '{munte,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (23, 'Pachet relaxare resort 5 stele în Punta Cana (Pachet Premium)', 1465.78, false, NULL, 4.4, 7, 'Transfer VIP de la aeroport', '2026-02-02 00:00:00+02', 1, 1001, '{mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (2, 'Zbor direct București - Bruxelles', 65.00, true, '2026-11-19', 4, 150, 'Bagaj de mână', '2026-10-21 12:43:37.511635+03', 3, 1, '{transport,belgia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (19, 'Pachet camping și supraviețuire în Sinaia (Pachet Premium)', 2050.70, false, NULL, 4.6, 48, 'Ghid montan autorizat', '2026-06-25 00:00:00+03', 4, 1008, '{munte}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (35, 'Transfer VIP aeroport în București (Pachet Premium)', 2285.35, false, NULL, 5, 37, 'Bagaj de cală inclus', '2026-03-23 00:00:00+02', 3, 1001, '{transport}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (46, 'Croazieră de lux 5 zile în Nisa (Pachet Premium)', 1492.66, true, NULL, 4.9, 33, 'Acces la puntea VIP', '2026-08-25 00:00:00+03', 5, 1001, '{franta,mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (7, 'Tur ghidat și degustare ciocolată', 40.00, true, '2026-10-22', 4.9, 20, 'Ghid local, Degustare 5 tipuri de praline', '2026-10-21 12:56:49.879467+03', 2, 4, '{gastronomie,belgia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (62, 'Bilet tren rapid în București (Pachet Premium)', 1382.08, false, NULL, 4.3, 23, 'Fără facilități suplimentare', '2026-07-09 00:00:00+03', 3, 1008, '{tren,transport,romania}', 'servicii/bucuresti.webp');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (20, 'Tur privat cu iahtul în Camogli (Pachet Premium)', 2217.71, false, NULL, 4.2, 33, 'Asigurare medicală premium', '2026-10-23 00:00:00+03', 5, 1001, '{mare,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (57, 'Bilet tren rapid în Frankfurt (Pachet Premium)', 735.45, true, NULL, 4.5, 33, 'Check-in prioritar', '2026-06-16 00:00:00+03', 3, 1001, '{tren,transport,germania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (25, 'Traseu mountain bike în Innsbruck (Pachet Premium)', 705.84, false, NULL, 4.9, 30, 'Asigurare de risc extrem', '2026-04-05 00:00:00+03', 4, 1001, '{munte,austria}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (54, 'Sejur 7 nopți All-Inclusive în Maldive (Pachet Premium)', 1928.94, false, NULL, 4.6, 24, 'Băuturi și mese incluse', '2026-04-17 00:00:00+03', 1, 1001, '{mare,all-inclusive}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (22, 'Sejur 7 nopți All-Inclusive în Antalya (Pachet Premium)', 2125.10, false, NULL, 4.6, 14, 'Băuturi și mese incluse', '2026-03-06 00:00:00+02', 1, 1002, '{mare,all-inclusive,turcia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (64, 'Drumeție ghidată pe creastă în Livigno (Pachet Premium)', 221.52, true, NULL, 4.2, 29, 'Transport spre traseu', '2026-05-31 00:00:00+03', 4, 1002, '{munte}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (12, 'Cazare 2 nopți Hotel Milano Centrale', 240.00, true, '2026-10-21', 5, 10, 'Mic dejun inclus, WiFi de mare viteză, Acces metrou', '2026-10-21 14:06:29.958673+03', 2, 6, '{"city break"}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (59, 'Croazieră pe Mediterana 7 zile în Barcelona (Pachet Premium)', 384.50, false, NULL, 3.7, 16, 'Acces la puntea VIP', '2026-06-05 00:00:00+03', 5, 1001, '{mare,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (60, 'Pachet City Break 3 nopți în Londra (Pachet Premium)', 255.91, false, NULL, 4, 24, 'WiFi gratuit', '2026-04-22 00:00:00+03', 2, 1010, '{"city break",anglia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (16, 'All-Inclusive Premium Resort în Punta Cana (Pachet Premium)', 993.30, true, NULL, 3.8, 15, 'Băuturi și mese incluse', '2026-05-13 00:00:00+03', 1, 1001, '{mare,all-inclusive}', 'servicii/punta_cana.jpg');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (8, 'Atelier preparare praline artizanale', 75.00, false, '2026-10-27', 5, 10, 'Echipament, Ingrediente, Cutie cadou', '2026-10-21 12:58:34.042089+03', 2, 4, '{"city break",belgia}', 'servicii/praline.jpg');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (48, 'Croazieră de lux 5 zile în Cinque Terre (Pachet Premium)', 1875.94, false, NULL, 4.8, 36, 'Cină festivă cu specific local', '2026-07-05 00:00:00+03', 5, 1004, '{mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (37, 'Croazieră la apus în Barcelona (Pachet Premium)', 2082.63, false, NULL, 3.8, 13, 'Cină festivă cu specific local', '2026-07-05 00:00:00+03', 5, 1001, '{mare,spania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (31, 'Escapadă romantică de weekend în Bruxelles (Pachet Premium)', 68.90, true, NULL, 4.6, 47, 'WiFi gratuit', '2026-06-03 00:00:00+03', 2, 1001, '{"city break",belgia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (47, 'Tur gastronomic local în Roma (Pachet Premium)', 2149.73, false, NULL, 4.1, 49, 'Fără facilități suplimentare', '2026-06-03 00:00:00+03', 2, 1004, '{gastronomie,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (58, 'Excursie montană extremă în Chamonix (Pachet Premium)', 2302.63, true, NULL, 4.2, 7, 'Transport spre traseu', '2026-06-21 00:00:00+03', 4, 1006, '{munte,franta}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (51, 'Pachet City Break 3 nopți în Paris (Pachet Premium)', 2279.10, false, NULL, 4.6, 16, 'Mic dejun inclus', '2026-08-05 00:00:00+03', 2, 1006, '{"city break",franta}', 'servicii/paris.jpg');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (52, 'O zi pe mare în Nisa (Pachet Premium)', 1218.37, true, NULL, 4.9, 12, 'Cină festivă cu specific local', '2026-02-20 00:00:00+02', 5, 1010, '{mare,franta}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (56, 'Croazieră pe Mediterana 7 zile în Atena (Pachet Premium)', 2029.58, false, NULL, 4.9, 50, 'Asigurare medicală premium', '2026-01-25 00:00:00+02', 5, 1002, '{mare,grecia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (63, 'Închiriere catamaran cu echipaj în Atena (Pachet Premium)', 2494.57, true, NULL, 4.5, 12, 'Asigurare medicală premium', '2026-07-22 00:00:00+03', 5, 1009, '{mare}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (50, 'Zbor direct în Frankfurt (Pachet Premium)', 2024.78, true, NULL, 4.5, 48, 'Bagaj de cală inclus', '2026-04-12 00:00:00+03', 3, 1001, '{transport,germania}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (11, 'Zbor direct București - Bergamo (Orio al Serio)', 55.00, true, '2026-11-12', 4.3, 100, 'Bagaj de mână, Prioritate la îmbarcare', '2026-10-21 14:03:50.792822+03', 3, 1, '{transport,italia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (61, 'Transfer VIP aeroport în Frankfurt (Pachet Premium)', 2215.21, true, NULL, 5, 23, 'Fără facilități suplimentare', '2026-10-16 00:00:00+03', 3, 1001, '{transport}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (3, 'Bilet tren rapid Florența - Roma', 35.00, true, '2026-10-22', 4.8, 300, 'Aer condiționat, WiFi gratuit, Prize', '2026-10-21 12:44:51.113693+03', 3, 2, '{tren,transport,italia}', 'servicii/trenitalia.jpeg');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (55, 'Tur ghidat in centrul istoric în Londra (Pachet Premium)', 1314.78, false, NULL, 4.8, 7, 'Mic dejun inclus', '2026-01-13 00:00:00+02', 2, 1001, '{"city break",anglia}', '');
INSERT INTO django.aplicatie_agentie_turism_serviciuindividual (id, nume_serviciu, pret_serviciu, este_activ, data_prestare, rating, stoc_locuri, facilitati_incluse, data_adaugare, id_categorie_id, id_furnizor_id, taguri, imagine) VALUES (53, 'Vacanță exotică All-Inclusive în Antalya (Pachet Premium)', 1064.07, true, NULL, 4, 33, 'Acces SPA și piscină', '2026-05-16 00:00:00+03', 1, 1001, '{mare,all-inclusive,turcia}', '');


--
-- Data for Name: aplicatie_agentie_turism_pachetsejur_servicii_incluse; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (1, 1, 1);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (2, 1, 5);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (3, 1, 6);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (4, 2, 8);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (5, 2, 2);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (6, 2, 7);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (7, 3, 9);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (8, 3, 3);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (9, 4, 9);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (10, 4, 10);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (11, 4, 6);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (12, 5, 11);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (13, 5, 4);
INSERT INTO django.aplicatie_agentie_turism_pachetsejur_servicii_incluse (id, pachetsejur_id, serviciuindividual_id) VALUES (14, 5, 12);


--
-- Data for Name: aplicatie_agentie_turism_punctintalnire; Type: TABLE DATA; Schema: django; Owner: stefan
--

INSERT INTO django.aplicatie_agentie_turism_punctintalnire (id, adresa, coordonate_gps, id_serviciu_id) VALUES (1, 'Grand Place (Piața Mare), lângă statuia principală', '50.8467, 4.3528', 7);
INSERT INTO django.aplicatie_agentie_turism_punctintalnire (id, adresa, coordonate_gps, id_serviciu_id) VALUES (2, 'Strada Rue de l''Etuve nr. 15, Bruxelles', '50.8449, 4.3499', 8);
INSERT INTO django.aplicatie_agentie_turism_punctintalnire (id, adresa, coordonate_gps, id_serviciu_id) VALUES (3, 'Pontonul central, Portul Vernazza', '44.1352, 9.6828', 9);
INSERT INTO django.aplicatie_agentie_turism_punctintalnire (id, adresa, coordonate_gps, id_serviciu_id) VALUES (4, 'Terminalul Plecări, Aeroportul Otopeni, Poarta 14', '44.5711, 26.0849', 1);
INSERT INTO django.aplicatie_agentie_turism_punctintalnire (id, adresa, coordonate_gps, id_serviciu_id) VALUES (5, 'Gara Santa Maria Novella, Peronul 8, Florența', '43.7765, 11.2476', 3);


--
-- Name: aplicatie_agentie_turism_ambalaj_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_ambalaj_id_seq', 1, false);


--
-- Name: aplicatie_agentie_turism_categorieserviciu_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_categorieserviciu_id_seq', 6, true);


--
-- Name: aplicatie_agentie_turism_furnizor_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_furnizor_id_seq', 6, true);


--
-- Name: aplicatie_agentie_turism_pachetsejur_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_pachetsejur_id_seq', 5, true);


--
-- Name: aplicatie_agentie_turism_pachetsejur_servicii_incluse_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_pachetsejur_servicii_incluse_id_seq', 14, true);


--
-- Name: aplicatie_agentie_turism_punctintalnire_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_punctintalnire_id_seq', 5, true);


--
-- Name: aplicatie_agentie_turism_serviciuindividual_id_seq; Type: SEQUENCE SET; Schema: django; Owner: stefan
--

SELECT pg_catalog.setval('django.aplicatie_agentie_turism_serviciuindividual_id_seq', 64, true);


--
-- PostgreSQL database dump complete
--

\unrestrict NNuTqZs3zFcIpuytNxT5ywzw3pdgeem8FxLWqCQPEcms7sVzKEmmCWrqczle46Z

