from django.shortcuts import render
from django.http import HttpResponse

def productDetail(request, urunid):
    return HttpResponse("<h1>hi product</h1>")
