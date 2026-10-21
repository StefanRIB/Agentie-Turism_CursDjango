from django.db import models
from django.db.models import Q

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
    sigla = models.ImageField(upload_to='categorii_sigle/', null=True, blank=True)
    
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
    telefon_contact = models.CharField(max_length=20, help_text="Includeți prefixul internațional (ex: +40).")

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