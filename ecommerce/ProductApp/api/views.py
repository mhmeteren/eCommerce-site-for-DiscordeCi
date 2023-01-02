from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from django.db.models import Q

from ProductApp.models import Urun, UrunOzellik, OnerilenUrunler
from ProductApp.api.serializers import UrunSerializers, OnerilenUrunlerSerializers
from ProductApp.api.pagination import LargePagination

from ..APIscripts.user_scripts import User_TOKEN_Control

class ProductsListAPIView(APIView):
    
    def get_products(self, id):
        products = get_object_or_404(Urun, UrunID = id)
        return products


    def get(self, request, id):
        """
        ürün id ye göre ürün bilgilerini dön.
        """
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
            products = Urun.objects.filter( **kwargs).order_by('UrunADI')
        except:
            return []
        return products


    def get(self, request):
        """
        UrunADI__icontains, UrunFIYAT__range ve UrunKODU göre ürün arama yapılan yer.
        "UrunSTOK__gt": 0, "UrunDURUM": true => Otomatik eklenenler.
        """
        UserAccessToken = request.query_params.get('UserAccessToken')
        Token_Status = User_TOKEN_Control(token=UserAccessToken)
        if Token_Status:
            products = self.ListProduct(**request.data)
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data) 

            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)



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
                    #     """
                    #     Girilen özeliklere tam uyan ürün yoksa [] döndür. Ya da bu kodu kapat sırayla uyan ozeliklere sahip urunleri getirir.
                    #     """
                    #     return []
                            
            except:
                return []

        return [pr.Urun for pr in products]


    def get(self, request):
        """
        "ozellikler": [
                {
                    "UrunOzType": "İşlemci Tipi",
                    "UrunOzValue": "AMD Ryzen 7"
                },
                .
                .
            ]
        Şekilde ürün özelliklerine göre filtreleme yapılan yer.
        """
        UserAccessToken = request.query_params.get('UserAccessToken')
        Token_Status = User_TOKEN_Control(token=UserAccessToken)
        if Token_Status:
            products = self.FilterProduct(**request.data)
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class OnerilenUrunlerListAPIView(APIView):
    """
    Kullanıcılara Discord tarafında Notification Bot ile önerilen ürünleri listelemek için.
    """
    serializer_class = OnerilenUrunlerSerializers
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


    def ListProduct(self):
        products = OnerilenUrunler.objects.filter(UrunDURUM=True).order_by('-UrunTARIH')
        return products


    def get_product(self, id):
        product = get_object_or_404(OnerilenUrunler, OuID = id)
        return product


    def get(self, request):
        """
        Onerilen ürünleri pagination_class ın kısıtlamaları ile gönder.
        """
        product = self.ListProduct()
        page = self.paginate_queryset(product)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data) 
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data)


    def put(self, request):
        """
        Önerilen ürünlerin hem güvenli bir şekilde Notification Bot una ulaşıp ulaşmadığını hemde
        ulaşan urunlerin(yani kullanıcılara bildirim yoluyla sunulan) bir daha önerilmemesi için UrunDURUM güncellemesi.
        "OnerilenUrunler":[
            {
                "OuID": OuID,
                "UrunDURUM": false
            },
            .
            .
            .
        ]
        """
        try:
            productList = request.data["OnerilenUrunler"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for p in productList:
            product = self.get_product(id = p["OuID"])
            serializer = OnerilenUrunlerSerializers(product, data=p)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status":{
                "message": "Islem basarili."
            }
        })
