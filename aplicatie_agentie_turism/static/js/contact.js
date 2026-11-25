/* 
    Pagina de contact (Laborator 5, Task 3):
    JavaScript vine in ajutorul utilizatorului pentru a face formularul 
    mai prietenos, dar nu inlocuieste validarea serverului. 
*/
(function () {
    const formular = document.getElementById('form-contact');
    if (!formular) return;

    const mapare = JSON.parse(document.getElementById('mapare-departamente').textContent);
    const cnp = document.getElementById('id_cnp');
    const contorCnp = document.getElementById('contor-cnp');
    const tip = document.getElementById('id_tip_mesaj');
    const departament = document.getElementById('id_departament');
    const gdpr = document.getElementById('id_gdpr');
    const trimite = document.getElementById('btn-trimite');
    const blocuriImagini = Array.from(document.querySelectorAll('.camp-imagine'));
    const mesajImagini = document.getElementById('mesaj-imagini');

    // (b) contor de cifre pentru CNP
    function actualizeazaContor() {
        contorCnp.textContent = cnp.value.replace(/\D/g, '').length;
    }

    // (g) departamentele depind de tipul mesajului (datele vin din baza de date)
    function actualizeazaDepartamente() {
        const ales = departament.value;
        const permise = mapare[tip.value] ? mapare[tip.value].departamente : [];
        departament.innerHTML = '';
        departament.add(new Option('neselectat', 'neselectat'));
        permise.forEach(function (nume) { departament.add(new Option(nume, nume)); });
        departament.value = permise.indexOf(ales) !== -1 ? ales : 'neselectat';
    }

    // (k) imaginile apar pe rand
    function actualizeazaImagini() {
        const inputuri = blocuriImagini.map(function (b) { return b.querySelector('input[type=file]'); });
        blocuriImagini.forEach(function (bloc, i) {
            const vizibil = i === 0 || inputuri[i - 1].files.length > 0 || inputuri[i].files.length > 0;
            bloc.hidden = !vizibil;
        });
        mesajImagini.hidden = !inputuri.every(function (inp) { return inp.files.length > 0; });
    }

    // (l) butonul de trimitere se deblocheaza doar cu acordul GDPR
    function actualizeazaTrimitere() {
        trimite.disabled = !gdpr.checked;
    }

    function actualizeazaTot() {
        actualizeazaContor();
        actualizeazaDepartamente();
        actualizeazaImagini();
        actualizeazaTrimitere();
    }

    cnp.addEventListener('input', actualizeazaContor);
    tip.addEventListener('change', actualizeazaDepartamente);
    gdpr.addEventListener('change', actualizeazaTrimitere);
    blocuriImagini.forEach(function (bloc) {
        bloc.querySelector('input[type=file]').addEventListener('change', actualizeazaImagini);
    });
    // dupa reset, browserul reface valorile initiale abia dupa eveniment
    formular.addEventListener('reset', function () { setTimeout(actualizeazaTot, 0); });

    actualizeazaTot();
})();
