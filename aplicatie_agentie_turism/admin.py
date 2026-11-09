from django.contrib import admin
from django.utils.html import format_html
from .models import Ambalaj, CategorieServiciu, Furnizor, ServiciuIndividual, PachetSejur, PunctIntalnire

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

admin.site.register(Ambalaj)
admin.site.register(CategorieServiciu, CategorieServiciuAdmin)
admin.site.register(Furnizor, FurnizorAdmin)
admin.site.register(ServiciuIndividual, ServiciuIndividualAdmin)
admin.site.register(PachetSejur, PachetSejurAdmin)
admin.site.register(PunctIntalnire, PunctIntalnireAdmin)

admin.site.site_header = "Administrare Zbor & Dor"        
admin.site.site_title = "Admin Zbor & Dor"                
admin.site.index_title = "Panou de Control Agenție"       
admin.site.site_url = "http://127.0.0.1:8000/aplicatie_agentie_turism/"                           