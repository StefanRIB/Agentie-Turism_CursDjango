// Task 2 bonus: filtrarea produselor cu fetch, fara reincarcarea paginii.
(function () {
    const zona = document.getElementById('zona-produse');
    if (!zona) return;

    function afiseazaMesaje(mesaje) {
        let lista = document.querySelector('.container-mesaje');
        if (!mesaje.length) {
            if (lista) lista.remove();
            return;
        }
        if (!lista) {
            lista = document.createElement('ul');
            lista.className = 'container-mesaje';
            document.querySelector('main').prepend(lista);
        }
        lista.innerHTML = '';
        mesaje.forEach(function (m) {
            const li = document.createElement('li');
            li.className = 'mesaj-notificare ' + m.tip;
            li.textContent = m.text;
            lista.appendChild(li);
        });
    }

    async function incarca(url, actualizeazaIstoric) {
        zona.classList.add('se-incarca');
        try {
            const raspuns = await fetch(url, { headers: { 'X-Requested-With': 'fetch' } });
            if (!raspuns.ok) throw new Error('HTTP ' + raspuns.status);
            const date = await raspuns.json();
            document.getElementById('zona-filtrare').innerHTML = date.formular;
            document.getElementById('continut-produse').innerHTML = date.continut;
            afiseazaMesaje(date.mesaje);
            if (actualizeazaIstoric) history.pushState({}, '', url);
        } catch (eroare) {
            window.location.href = url; // plan de rezerva: incarcare obisnuita
        } finally {
            zona.classList.remove('se-incarca');
        }
    }

    // trimiterea formularului de filtrare
    zona.addEventListener('submit', function (e) {
        const formular = e.target.closest('#form-filtrare');
        if (!formular) return;
        e.preventDefault();
        const parametri = new URLSearchParams();
        new FormData(formular).forEach(function (valoare, cheie) {
            if (valoare !== '') parametri.append(cheie, valoare);
        });
        const interogare = parametri.toString();
        incarca(formular.getAttribute('action') + (interogare ? '?' + interogare : ''), true);
    });

    zona.addEventListener('click', function (e) {
        // paginare, taguri, "Sterge toate"
        const link = e.target.closest('a[data-fetch]');
        if (link) {
            e.preventDefault();
            incarca(link.getAttribute('href'), true);
            return;
        }
        // resetarea filtrelor, cu confirmare
        const reset = e.target.closest('#btn-reset');
        if (reset) {
            e.preventDefault();
            if (confirm('Atenție! Resetarea va șterge toate filtrele aplicate până acum. Doriți să continuați?')) {
                incarca(reset.getAttribute('href'), true);
            }
        }
    });

    // butoanele Inapoi / Inainte ale browserului
    window.addEventListener('popstate', function () {
        incarca(location.pathname + location.search, false);
    });
})();
