from django.conf import settings 
from .models import CategorieServiciu

def informatii_firma(request):
    return {'firma': settings.DATE_FIRMA}

def categorii_globale(request):
    # Extrag toate categoriile din baza de date
    categorii = CategorieServiciu.objects.filter(servicii__isnull=False).distinct()
    # Intorc rezultatul sub forma unui dictionar ce va fi folosit in templates
    return {'categorii_meniu': categorii}