from django.contrib import admin
from .models import User, UrunList, UrunYorum, Sepet, UyeList

admin.site.register(User)
admin.site.register(UrunList)
admin.site.register(UyeList)
admin.site.register(UrunYorum)
admin.site.register(Sepet)
# Register your models here.
