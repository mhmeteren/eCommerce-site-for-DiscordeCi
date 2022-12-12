from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from django.db.models import Q

from ProductApp.models import Urun, UrunOzellik

from ProductApp.api.serializers import UrunSerializers, OzellikSerializers


class ProductsListAPIView(APIView):

    def get_products(self, id):
        products = get_object_or_404(Urun, UrunID = id)
        return products

    def get(self, request, id):
        product = self.get_products(id)
        serializers = UrunSerializers(product)
        return Response(serializers.data, status=status.HTTP_200_OK)



class ProductsSearchListAPIView(APIView):

    def ListProduct(self, **kwargs):
        products = Urun.objects.filter( **kwargs)
        return products

    def get(self, request):
        products = self.ListProduct(**request.data)
        serializers = UrunSerializers(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ProductsFilterListAPIView(APIView):



    def FilterProduct(self, **kwargs):
        OzList = kwargs.get('ozellikler')
        products = []
        for ozDict in OzList:
            if products == []:
                products = UrunOzellik.objects.filter(**ozDict)
                
            else:
                temp = []
                for pr in products:
                    urunoz = UrunOzellik.objects.filter(Urun= pr.Urun, **ozDict).first()
                    
                    if urunoz:
                        temp.append(urunoz) 

                products = temp        
        
        return [pr.Urun for pr in products]

    def get(self, request):
        products = self.FilterProduct(**request.data)
        serializers = UrunSerializers(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
