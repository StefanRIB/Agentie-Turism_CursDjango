from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    Ambalaj, CategorieServiciu, Furnizor, ServiciuIndividual, PachetSejur, PunctIntalnire,
    Utilizator, Profil, Departament, Angajat, Voucher, Review, Intrebare, Comanda, ComandaServiciu,
    TipMesaj,
)

@admin.action(description='Activează serviciile selectate')
def activeaza_servicii(modeladmin, request, queryset):
    queryset.update(este_activ=True)

@admin.action(description='Dezactivează serviciile selectate')
def dezactiveaza_servicii(modeladmin, request, queryset):
    queryset.update(este_activ=False)

class CategorieServiciuAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'tip_public') 
    search_help_text = "Căutați categoria după nume sau după tipul publicului."

    list_per_page = 5

class FurnizorAdmin(admin.ModelAdmin):
    search_fields = ('nume_furnizor', 'telefon_contact')
    search_help_text = "Căutați furnizorul după nume sau după numărul de telefon."

    list_per_page = 5

class PachetSejurAdmin(admin.ModelAdmin):
    search_fields = ('titlu_pachet', 'servicii_incluse__nume_serviciu') 
    search_help_text = "Căutați pachetul după nume sau după serviciile incluse."

    list_per_page = 5

class PunctIntalnireAdmin(admin.ModelAdmin):
    search_fields = ('adresa', 'id_serviciu__nume_serviciu') 
    search_help_text = "Căutați punctul de întâlnire după adresă sau după numele serviciului asociat."

    list_per_page = 5

    fieldsets = (
        ('Informații Principale', {
            'fields': ('id_serviciu',),
        }),
        ('Detalii Locație (Opționale)', {
            'classes': ('collapse',), 
            'fields': ('adresa', 'coordonate_gps'),
            'description': "Aceste detalii nu sunt obligatorii și pot fi completate ulterior."
        }),
    )

class ServiciuIndividualAdmin(admin.ModelAdmin):
    list_display = ('nume_serviciu', 'este_activ', 'stoc_locuri', 'pret_stilizat', 'get_furnizor_contact')

    search_fields = ('nume_serviciu', 'facilitati_incluse')
    search_help_text = "Căutați serviciul după nume sau după facilitățile incluse."

    ordering = ('-pret_serviciu',)
    list_filter = ('este_activ', 'id_categorie', 'id_furnizor')
    list_per_page = 5

    actions = [activeaza_servicii, dezactiveaza_servicii]

    fieldsets = (
        ('Informații Principale', {
            'fields': ('nume_serviciu', 'pret_serviciu', 'id_categorie', 'id_furnizor', 'este_activ')
        }),
        ('Detalii Opționale', {
            'classes': ('collapse',), 
            'fields': ('facilitati_incluse', 'rating', 'imagine', 'taguri', 'stoc_locuri') 
        }),
    )

    @admin.display(description='Contact Furnizor (One-to-Many)')
    def get_furnizor_contact(self, obj):
        if obj.id_furnizor and obj.id_furnizor.email_contact:
            return obj.id_furnizor.email_contact
        return "Fără contact"
    
    @admin.display(description='Preț Custom')
    def pret_stilizat(self, obj):
        return format_html(
            '<span style="color: red; font-weight: bold; font-style: italic;">{} EUR</span>',
            obj.pret_serviciu
        )

class UtilizatorAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefon', 'gen', 'is_staff')
    list_filter = ('gen', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefon')
    search_help_text = "Căutați utilizatorul după username, e-mail, nume sau telefon."
    list_per_page = 5

    fieldsets = UserAdmin.fieldsets + (
        ('Date suplimentare', {'fields': ('telefon', 'data_nasterii', 'gen')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Date suplimentare', {'fields': ('email', 'first_name', 'last_name', 'telefon', 'data_nasterii', 'gen')}),
    )

class ProfilAdmin(admin.ModelAdmin):
    list_display = ('utilizator', 'tara', 'judet', 'strada', 'cod_postal')
    search_fields = ('utilizator__username', 'tara', 'judet', 'strada')
    search_help_text = "Căutați profilul după utilizator, țară, județ sau stradă."
    list_per_page = 5

class DepartamentAdmin(admin.ModelAdmin):
    list_display = ('nume_departament', 'sef')
    search_fields = ('nume_departament', 'sef__utilizator__username')
    search_help_text = "Căutați departamentul după nume sau după șef."
    list_per_page = 5

class AngajatAdmin(admin.ModelAdmin):
    list_display = ('utilizator', 'functie', 'departament', 'data_angajare', 'salariu')
    list_filter = ('departament',)
    search_fields = ('utilizator__username', 'functie')
    search_help_text = "Căutați angajatul după username sau funcție."
    ordering = ('-salariu',)
    list_per_page = 5

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('cod_voucher', 'utilizator', 'procent_reducere', 'valabilitate')
    list_filter = ('valabilitate',)
    search_fields = ('cod_voucher', 'utilizator__username')
    search_help_text = "Căutați voucherul după cod sau după utilizator."
    list_per_page = 5

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('utilizator', 'serviciu', 'nota_review', 'data_postare')
    list_filter = ('nota_review',)
    search_fields = ('utilizator__username', 'serviciu__nume_serviciu')
    search_help_text = "Căutați review-ul după utilizator sau după serviciu."
    list_per_page = 5

class IntrebareAdmin(admin.ModelAdmin):
    list_display = ('text_intrebare', 'utilizator', 'serviciu', 'data_intrebare', 'are_raspuns')
    search_fields = ('text_intrebare', 'utilizator__username', 'serviciu__nume_serviciu')
    search_help_text = "Căutați întrebarea după text, utilizator sau serviciu."
    list_per_page = 5

    @admin.display(description='Răspuns oficial', boolean=True)
    def are_raspuns(self, obj):
        return bool(obj.raspuns_oficial)

class ComandaServiciuInline(admin.TabularInline):
    model = ComandaServiciu
    extra = 1

class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilizator', 'status_comanda', 'metoda_plata', 'data_inregistrarii')
    list_filter = ('status_comanda', 'metoda_plata')
    search_fields = ('utilizator__username', 'servicii__nume_serviciu')
    search_help_text = "Căutați comanda după utilizator sau după serviciile comandate."
    list_per_page = 5
    inlines = [ComandaServiciuInline]

admin.site.register(Ambalaj)
admin.site.register(CategorieServiciu, CategorieServiciuAdmin)
admin.site.register(Furnizor, FurnizorAdmin)
admin.site.register(ServiciuIndividual, ServiciuIndividualAdmin)
admin.site.register(PachetSejur, PachetSejurAdmin)
admin.site.register(PunctIntalnire, PunctIntalnireAdmin)
admin.site.register(Utilizator, UtilizatorAdmin)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(Departament, DepartamentAdmin)
admin.site.register(Angajat, AngajatAdmin)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Intrebare, IntrebareAdmin)
admin.site.register(Comanda, ComandaAdmin)


class TipMesajAdmin(admin.ModelAdmin):
    list_display = ('nume', 'cod', 'zile_minime')
    filter_horizontal = ('departamente',)
    search_fields = ('nume', 'cod')
    search_help_text = "Căutați tipul de mesaj după nume sau cod."


admin.site.register(TipMesaj, TipMesajAdmin)
admin.site.site_header = "Administrare Zbor & Dor"        
admin.site.site_title = "Admin Zbor & Dor"                
admin.site.index_title = "Panou de Control Agenție"       
admin.site.site_url = "http://127.0.0.1:8000/aplicatie_agentie_turism/"