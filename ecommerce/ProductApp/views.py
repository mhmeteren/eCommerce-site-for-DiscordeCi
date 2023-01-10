from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .models import *

import locale

@require_http_methods(["GET"])  
def productDetail(request, urunid):
    try:
        urun = Urun.objects.get(UrunID = urunid)
        urunImg = UrunImg.objects.get(Urun = Urun(UrunID = urunid))
    except Urun.DoesNotExist:
        urun = None
        urunImg = None


    if urun is None or urunImg is None:
        return render(request, '404page.html')

    urun.UrunACIKLAMA = urun.UrunACIKLAMA.split("|")

    urun.UrunFIYAT = ConvertFiyat(urun.UrunFIYAT)

    related_products = Urun.objects.filter(~Q(UrunID = urun.UrunID), Marka = urun.Marka)[:4]
    related_products_img =list()

    urunoz = UrunOzellik.objects.filter(Urun = urun)
    
    for product in related_products:
        related_products_img.append(UrunImg.objects.get(Urun = product).UrunImgUrl)
        product.UrunFIYAT = ConvertFiyat(product.UrunFIYAT)
    


    related_productsPac = zip(related_products, related_products_img)

    
    content = { 
        'product': urun,
        'productOptions': urunoz,
        'productImgUrl': urunImg,
        'related_productsPac': related_productsPac,
    }  

    return render(request, 'product-details.html', context=content)


def ConvertFiyat(fiyat):
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    return locale.format_string('%.2f', fiyat, True)

