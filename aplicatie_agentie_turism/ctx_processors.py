from django.conf import settings 

def informatii_firma(request):
    return {'firma': settings.DATE_FIRMA}