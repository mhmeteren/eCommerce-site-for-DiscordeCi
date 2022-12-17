from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from django.db.models import Q

from ProductApp.models import Urun, UrunOzellik
from ProductApp.api.serializers import UrunSerializers
from ProductApp.api.pagination import LargePagination

class ProductsListAPIView(APIView):
    
    def get_products(self, id):
        products = get_object_or_404(Urun, UrunID = id)
        return products

    def get(self, request, id):
        product = self.get_products(id)
        serializers = UrunSerializers(product)
        return Response(serializers.data, status=status.HTTP_200_OK)



class ProductsSearchListAPIView(APIView):
    serializer_class = UrunSerializers
    pagination_class = LargePagination


    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)




    def ListProduct(self, **kwargs):
        try:
            products = Urun.objects.filter( **kwargs)
        except:
            return []
        return products

    def get(self, request):
        products = self.ListProduct(**request.data)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data) 
            
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)


class ProductsFilterListAPIView(APIView):
    serializer_class = UrunSerializers
    pagination_class = LargePagination

    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    """
    When I wrote this code, only god and I knew how it worked.
    Now only god know
    """
    def FilterProduct(self, **kwargs):
        OzList = kwargs.get('ozellikler')
        products = []
        for ozDict in OzList:
            try:
                if products == []:
                    products_temp = UrunOzellik.objects.filter(**ozDict)
                    if not products_temp:
                        break
                    products = products_temp

                else:
                    temp = []
                    for pr in products:
                        urunoz = UrunOzellik.objects.filter(Urun= pr.Urun, **ozDict).first()
                        if urunoz:
                            temp.append(urunoz) 

                    if temp:
                        products = temp
                    # else:
                    #     return []
                    # Girilen özeliklere tam uyan ürün yoksa [] döndür. Ya da bu kodu kapat sırayla uyan ozeliklere sahip urunleri getirir.        
            except:
                return []

        return [pr.Urun for pr in products]


    def get(self, request):
        products = self.FilterProduct(**request.data)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)
