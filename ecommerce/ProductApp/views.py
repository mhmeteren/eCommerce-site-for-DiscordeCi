from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import *

@require_http_methods(["GET"])  
def productDetail(request, urunid):
    try:
        urun = Urun.objects.get(UrunID = urunid)
        urunImg = UrunImg.objects.get(UrunID = Urun(UrunID = urunid))
    except Urun.DoesNotExist:
        urun = None



    content = { 
        'product': urun,
        'productImgUrl': urunImg,
    }

    return render(request, 'product-details.html', context=content)

