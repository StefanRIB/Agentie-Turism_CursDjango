from django.db import migrations

# tip -> (nume afisat, zile minime, departamente care pot primi mesajul)
TIPURI = {
    'reclamatie': ('Reclamație', 2, ['Relații clienți', 'Administrație', 'Comenzi']),
    'intrebare': ('Întrebare', 2, ['Relații clienți', 'Comenzi', 'Programări']),
    'review': ('Review', 4, ['QA', 'Administrație', 'Relații clienți']),
    'cerere': ('Cerere', 4, ['Angajări', 'Administrație', 'Comenzi']),
    'programare': ('Programare', 2, ['Programări', 'Relații clienți']),
}


def adauga_date(apps, schema_editor):
    Departament = apps.get_model('aplicatie_agentie_turism', 'Departament')
    TipMesaj = apps.get_model('aplicatie_agentie_turism', 'TipMesaj')
    for cod, (nume, zile, departamente) in TIPURI.items():
        tip, _ = TipMesaj.objects.get_or_create(cod=cod, defaults={'nume': nume, 'zile_minime': zile})
        for nume_dep in departamente:
            dep, _ = Departament.objects.get_or_create(nume_departament=nume_dep)
            tip.departamente.add(dep)


def sterge_date(apps, schema_editor):
    TipMesaj = apps.get_model('aplicatie_agentie_turism', 'TipMesaj')
    TipMesaj.objects.filter(cod__in=TIPURI).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_agentie_turism', '0002_tipmesaj'),
    ]

    operations = [
        migrations.RunPython(adauga_date, sterge_date),
    ]
