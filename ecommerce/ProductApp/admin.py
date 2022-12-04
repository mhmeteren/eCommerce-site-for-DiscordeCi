from django.contrib import admin

from .models import Firma, Marka, Kategori, AltKategori, Urun, UrunImg


admin.site.register(Firma)
admin.site.register(Marka)
admin.site.register(Kategori)
admin.site.register(AltKategori)
admin.site.register(Urun)
admin.site.register(UrunImg)
# Register your models here.
