from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Ambalaj(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nivel_rezistenta__lte=10) & models.Q(nivel_rezistenta__gte=1),
                name='limite_rezista_ambalaj',
                violation_error_message="Nivelul de rezistență trebuie să fie între 1 și 10 inclusiv!"
            )
        ]
    nume=models.CharField(max_length=200, unique=True)
    nume2=models.CharField(max_length=200, unique=True)
    culoare=models.CharField(max_length=100, null=True)
    nivel_rezistenta=models.PositiveIntegerField(
        help_text="Valori între 1 și 10. Un număr mai mare indică rezistență mai mare",
        null=True
    )
    descriere = models.TextField(null=True)
   
    def __str__(self):
        return f"{self.nume}: {self.culoare}"
    
# 1. Tabelul CATEGORIE_SERVICIU
class CategorieServiciu(models.Model):
    class TipPublic(models.TextChoices):
        FAMILIE = 'familie', 'Familie'
        CUPLU = 'cuplu', 'Cuplu'
        TINERET = 'tineret', 'Tineret'
        TOTI = 'toti', 'Toti'

    nume = models.CharField(
        max_length=100, 
        unique=True,
        error_messages={
            'unique': 'O categorie cu un astfel de nume este deja prezenta in tabel.',
            'max_length': 'Numele categoriei este prea lung. Maximum 100 de caractere sunt permise.'
        }
    )

    descriere = models.TextField(null=True, blank=True)
    culoare = models.CharField(max_length=20, help_text="Codul hexazecimal al culorii pentru frontend (ex: #FFFFFF).")
    sigla = models.CharField(max_length=50, null=True, blank=True, help_text="Ex: fa-solid fa-plane")
    
    tip_public = models.CharField(
        max_length=20, 
        choices=TipPublic.choices, 
        default=TipPublic.TOTI
    )

    class Meta:
        ordering = ['nume']
        verbose_name_plural = "Categorii Servicii"

    def __str__(self):
        return f"{self.nume} ({self.get_tip_public_display()})"
    
# Tabelul FURNIZOR
class Furnizor(models.Model):
    nume_furnizor = models.CharField(
        max_length=150, 
        unique=True,
        error_messages={'unique': 'Un furnizor cu acest nume este înregistrat deja in tabela!'}
    )

    email_contact = models.EmailField(null=True, blank=True) 
    site_web = models.URLField(null=True, blank=True)
    telefon_contact = models.CharField(
        max_length=20, 
        help_text="Va rugam sa includeți prefixul internațional al numarului de telefon (ex: +40).",
        error_messages={'max_length': 'Numărul de telefon introdus este prea lung. Maximum 20 de caractere sunt permise.'}
    )

    class Meta:
        ordering = ['nume_furnizor']
        verbose_name_plural = "Furnizori"
        indexes = [
            models.Index(fields=['nume_furnizor'], name='idx_nume_furnizor')
        ]

    def __str__(self):
        return self.nume_furnizor
    
# 3. Tabelul SERVICIU_INDIVIDUAL
class ServiciuIndividual(models.Model):
    imagine = models.ImageField(upload_to='servicii/', blank=True, null=True)
    nume_serviciu = models.CharField(max_length=200)
    
    pret_serviciu = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        help_text="Prețul de bază al serviciului, exprimat în EUR.",
        error_messages={'invalid': 'Va rugam sa introduceți un preț valid, cu maxim 2 zecimale.'}
    )
    
    este_activ = models.BooleanField(default=True, blank=True)
    data_prestare = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0.0)
    stoc_locuri = models.PositiveIntegerField(help_text="Numărul total de locuri disponibile pentru clienți.")
    facilitati_incluse = models.TextField(null=True, blank=True, help_text="Enumerați facilitățile separate prin virgulă.")
    data_adaugare = models.DateTimeField(auto_now_add=True)

    id_categorie = models.ForeignKey(CategorieServiciu, on_delete=models.CASCADE, related_name='servicii')
    id_furnizor = models.ForeignKey(Furnizor, on_delete=models.CASCADE, related_name='servicii_prestate')

    stoc_locuri = models.IntegerField(default=10)
    taguri = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list
    )

    class Meta:
        verbose_name_plural = "Servicii Individuale"
        constraints = [
            models.CheckConstraint(condition=Q(pret_serviciu__gte=0), name='pret_serviciu_pozitiv'),
            models.CheckConstraint(condition=Q(stoc_locuri__gte=0), name='stoc_locuri_pozitiv'),
            models.CheckConstraint(condition=Q(rating__gte=0) & Q(rating__lte=5), name='rating_valid_0_5')
        ]
        indexes = [
            models.Index(fields=['nume_serviciu'], name='idx_nume_serviciu'),
            models.Index(fields=['-data_adaugare'], name='idx_data_adaugare')
        ]

    def __str__(self):
        return f"{self.nume_serviciu} - {self.pret_serviciu} EUR"
    
    def get_absolute_url(self):
        return reverse('detalii_produs', kwargs={'pk': self.pk})


# 4. Tabelul PACHET_SEJUR  
class PachetSejur(models.Model):
    titlu_pachet = models.CharField(
        max_length=150,
        error_messages={'max_length': 'Titlul pachetului nu poate depăși 150 de caractere.'}
    )
    reducere_aplicata = models.FloatField(
        default=0.0,
        help_text="Procentul de reducere aplicat (între 0 și 100)."
    )
    servicii_incluse = models.ManyToManyField(ServiciuIndividual, related_name='pachete')

    class Meta:
        verbose_name_plural = "Pachete Sejur"
        constraints = [
            models.CheckConstraint(condition=Q(reducere_aplicata__gte=0), name='reducere_minima_0'),
            models.CheckConstraint(condition=Q(reducere_aplicata__lte=100), name='reducere_maxima_100')
        ]
        indexes = [
            models.Index(fields=['titlu_pachet'], name='idx_titlu_pachet')
        ]

    def __str__(self):
        return f"{self.titlu_pachet} (-{self.reducere_aplicata}%)"

# 5. Tabelul PUNCT_INTALNIRE
class PunctIntalnire(models.Model):
    adresa = models.CharField(max_length=255, null=True, blank=True)
    coordonate_gps = models.CharField(max_length=100, null=True, blank=True)
    
    id_serviciu = models.ForeignKey(ServiciuIndividual, on_delete=models.CASCADE, related_name='puncte_intalnire')

    class Meta:
        verbose_name_plural = "Puncte de Întâlnire"

    def __str__(self):
        return f"{self.adresa} (pentru: {self.id_serviciu.nume_serviciu})"

# 6. Tabelul UTILIZATOR 
class Utilizator(AbstractUser):
    class Gen(models.TextChoices):
        MASCULIN = 'M', 'Masculin'
        FEMININ = 'F', 'Feminin'
        ALTUL = 'A', 'Altul'

    telefon = models.CharField(
        max_length=20, blank=True,
        help_text="Cu prefix internațional (ex: +40712345678)."
    )
    data_nasterii = models.DateField(null=True, blank=True)
    gen = models.CharField(max_length=1, choices=Gen.choices, default=Gen.ALTUL)

    class Meta:
        verbose_name_plural = "Utilizatori"

    def __str__(self):
        return self.username


# 7. Tabelul PROFIL (one-to-one cu UTILIZATOR, toate campurile optionale)
class Profil(models.Model):
    utilizator = models.OneToOneField(Utilizator, on_delete=models.CASCADE, related_name='profil')
    judet = models.CharField(max_length=100, blank=True)
    strada = models.CharField(max_length=150, blank=True)
    cod_postal = models.CharField(max_length=10, blank=True)
    tara = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return f"Profil {self.utilizator.username}"


# 8. Tabelul DEPARTAMENT (sef = un angajat, poate fi NULL)
class Departament(models.Model):
    nume_departament = models.CharField(max_length=100, unique=True)
    sef = models.OneToOneField(
        'Angajat', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='departament_condus'
    )

    class Meta:
        verbose_name_plural = "Departamente"

    def __str__(self):
        return self.nume_departament


# 9. Tabelul ANGAJAT (one-to-one cu UTILIZATOR, N-1 cu DEPARTAMENT)
class Angajat(models.Model):
    utilizator = models.OneToOneField(Utilizator, on_delete=models.CASCADE, related_name='angajat')
    departament = models.ForeignKey(
        Departament, null=True, blank=True, on_delete=models.SET_NULL, related_name='angajati'
    )
    data_angajare = models.DateField()
    salariu = models.DecimalField(max_digits=10, decimal_places=2)
    functie = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Angajați"
        constraints = [
            models.CheckConstraint(condition=Q(salariu__gte=0), name='salariu_pozitiv')
        ]

    def __str__(self):
        return f"{self.utilizator.username} - {self.functie}"


# 10. Tabelul VOUCHER (un utilizator detine mai multe vouchere)
class Voucher(models.Model):
    utilizator = models.ForeignKey(Utilizator, on_delete=models.CASCADE, related_name='vouchere')
    cod_voucher = models.CharField(max_length=30, unique=True)
    procent_reducere = models.FloatField(help_text="Între 0 și 100.")
    valabilitate = models.DateField(help_text="Data până la care este valabil voucherul.")

    class Meta:
        verbose_name_plural = "Vouchere"
        constraints = [
            models.CheckConstraint(
                condition=Q(procent_reducere__gte=0) & Q(procent_reducere__lte=100),
                name='procent_voucher_valid'
            )
        ]

    def __str__(self):
        return f"{self.cod_voucher} (-{self.procent_reducere}%)"


# 11. Tabelul REVIEW (un utilizator scrie review-uri pentru servicii)
class Review(models.Model):
    utilizator = models.ForeignKey(Utilizator, on_delete=models.CASCADE, related_name='review_uri')
    serviciu = models.ForeignKey(ServiciuIndividual, on_delete=models.CASCADE, related_name='review_uri')
    data_postare = models.DateTimeField(auto_now_add=True)
    nota_review = models.PositiveSmallIntegerField(help_text="Notă între 1 și 5.")

    class Meta:
        verbose_name_plural = "Review-uri"
        constraints = [
            models.CheckConstraint(
                condition=Q(nota_review__gte=1) & Q(nota_review__lte=5),
                name='nota_review_1_5'
            )
        ]

    def __str__(self):
        return f"{self.utilizator.username} -> {self.serviciu.nume_serviciu}: {self.nota_review}/5"


# 12. Tabelul INTREBARE (utilizatorul adreseaza intrebari despre un serviciu)
class Intrebare(models.Model):
    utilizator = models.ForeignKey(Utilizator, on_delete=models.CASCADE, related_name='intrebari')
    serviciu = models.ForeignKey(ServiciuIndividual, on_delete=models.CASCADE, related_name='intrebari')
    text_intrebare = models.TextField()
    data_intrebare = models.DateTimeField(auto_now_add=True)
    raspuns_oficial = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Întrebări"

    def __str__(self):
        return f"{self.text_intrebare[:50]}"


# 13. Tabelul COMANDA (M-N cu SERVICIU_INDIVIDUAL prin COMANDA_SERVICIU)
class Comanda(models.Model):
    class Status(models.TextChoices):
        PLASATA = 'plasata', 'Plasată'
        IN_PROCESARE = 'in_procesare', 'În procesare'
        EFECTUATA = 'efectuata', 'Efectuată'
        ANULATA = 'anulata', 'Anulată'

    class MetodaPlata(models.TextChoices):
        CARD = 'card', 'Card'
        RAMBURS = 'ramburs', 'Ramburs'
        TRANSFER = 'transfer', 'Transfer bancar'

    utilizator = models.ForeignKey(Utilizator, on_delete=models.CASCADE, related_name='comenzi')
    status_comanda = models.CharField(max_length=20, choices=Status.choices, default=Status.PLASATA)
    data_inregistrarii = models.DateTimeField(auto_now_add=True)
    metoda_plata = models.CharField(max_length=20, choices=MetodaPlata.choices, default=MetodaPlata.CARD)
    servicii = models.ManyToManyField(
        ServiciuIndividual, through='ComandaServiciu', related_name='comenzi'
    )

    class Meta:
        verbose_name_plural = "Comenzi"

    def __str__(self):
        return f"Comanda #{self.pk} - {self.utilizator.username} ({self.get_status_comanda_display()})"


# Tabela de legatura COMANDA - SERVICIU_INDIVIDUAL (cu atributul "cantitate")
class ComandaServiciu(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    serviciu = models.ForeignKey(ServiciuIndividual, on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Servicii din comenzi"
        constraints = [
            models.UniqueConstraint(fields=['comanda', 'serviciu'], name='serviciu_unic_in_comanda'),
            models.CheckConstraint(condition=Q(cantitate__gte=1), name='cantitate_minim_1'),
        ]

    def __str__(self):
        return f"{self.cantitate} x {self.serviciu.nume_serviciu} (comanda #{self.comanda_id})"