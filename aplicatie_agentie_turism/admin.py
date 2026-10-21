from django.contrib import admin
from .models import Ambalaj, CategorieServiciu, Furnizor, ServiciuIndividual, PachetSejur, PunctIntalnire

# Register your models here.

admin.site.register(Ambalaj)
admin.site.register(CategorieServiciu)
admin.site.register(Furnizor)
admin.site.register(ServiciuIndividual)
admin.site.register(PachetSejur)
admin.site.register(PunctIntalnire)
