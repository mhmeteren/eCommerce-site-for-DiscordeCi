from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response

from UserApp.models import User, UrunList, UyeList, Urun, SiparisStatus, Siparis
from UserApp.api.serializers import *


from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from django.http import Http404

class UserAccTokenAutAPIView(APIView):
    def get_object(self, token):
        dc_instance = get_object_or_404(User, TOKEN=token)
        return dc_instance


    def get(self, request, token):
        """
        Kullanıcı token doğrulama için varsa kullanıcının bilgilerini dön.
        """
        user = self.get_object(token)
        serializer = UserSerializers(user)
        return Response(serializer.data)



class UserUyeListAPIView(APIView):
    """
    Kullanıcının access tok ı ile ürün listelerinin listelendiği yer.
    GET : /Listname/ or /Listname/?p=UrunId
    {
        "Token": "testTOKEN_128_karakterli_hex_text"
    }
    POST and DELETE : /Listname/
    {
        "Urun": UrunId,
        "Token": "testTOKEN_128_karakterli_hex_text"
    }
    """
    def get_UyeList_objects(self, TOKEN: str, ListName: str):
        try:
            user = User.objects.get(TOKEN=TOKEN)
            list_instance = get_object_or_404(UyeList, User = user, UyeListADI=ListName)
            return list_instance
        except:
            raise Http404




    def get_product(self, uyeList: UyeList, urunid: int):
        product = get_object_or_404(UrunList, UyeList=uyeList, Urun=Urun(UrunID = urunid))
        return product


    def productControl(self, UyeList: UyeList, UrunId: int):
        """
        Ürün zaten iligili listede varsa ekleme.
        """
        try:
            UrunList.objects.get(UyeList= UyeList, Urun = Urun(UrunID = UrunId))
            return True
        except:
            return False


    def get(self, request, listname: str):
        """
        Eğer url de ?p parametresi ile GET isteği yapılırsa
        sadece ilgili ürünün bilgilerini response da gönder.(p param is product Id) 
        Ya da tüm listedeki ürünlerin bilgilerini response da gönder.
        """
        p = request.query_params.get('p')
        try:
            token = request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _uyeList = self.get_UyeList_objects(TOKEN=token, ListName=listname)
        if p is None:
            serializer = UyeListSerializers(_uyeList)
        else:
            product = self.get_product(uyeList=_uyeList, urunid=p)
            serializer = UrunListSerializers(product)
        return Response(serializer.data)


    def post(self, request, listname: str):
        """
        request de gelen {"UrunID": UrunId, "Token": "testTOKEN_128_karakterli_hex_text"} ye UyeList de eklenerek ürün ilgili Kullanıcının
        ilgili listesine eklenir.
        listname: str
        """
        p = request.query_params.get('p')
        try:
            token = request.data["Token"]
            del request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _uyeList = self.get_UyeList_objects(TOKEN=token, ListName=listname)
        if p is None and not self.productControl(UyeList=_uyeList, UrunId=request.data["Urun"]):
            request.data["UyeList"] = _uyeList.UyeListID
            serializer = UrunCreatSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, listname: str):
        """
        params da gelen ?p => product id ile ilgili ürün ilgili kullanıcının
        ilgili listesinden ürün silinir.
        """
        p = request.query_params.get('p')
        try:
            token = request.data["Token"]
            del request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        _uyeList = self.get_UyeList_objects(TOKEN=token, ListName=listname)
        if p:
            product = self.get_product(uyeList=_uyeList, urunid=p)
            product.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_400_BAD_REQUEST)



class UserProductListView(APIView):
    """
    Kullanıcıların oluşturdukları urun listeleri sıralanır
    
    GET : userlists/
    {
        "Token": "testTOKEN_128_karakterli_hex_text"
    }

    """

    def get_UyeList_objects(self, TOKEN: str):
        try:
            user = User.objects.get(TOKEN=TOKEN)
            list_instance = UyeList.objects.filter(User = user)
            return list_instance
        except:
            raise Http404


    def get(self, request):
        try:
            token = request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Uyelist = self.get_UyeList_objects(TOKEN=token)
        serializer = UserProductListSerializers(Uyelist, many = True)
        return Response(serializer.data)



class UserSepetListAddDeleteAPIView(APIView):
    """
    İlgili kulanıcının Access token ı ile sepetindeki ürünler üzerinde listemleme/Ekleme/Silme gibi
    işlemlerin yapıldığı APIView class
    """

    def get_User(self, UserAccessToken: str):
        user = get_object_or_404(User, TOKEN = UserAccessToken)
        return user


    def get_Cart(self, User: User):
        """
        İlgili kullanıcının sepetindeki tüm ürünleri filtreleyen fonksiyon
        """
        tepes = Sepet.objects.filter(User=User)
        return tepes


    def get_product_Sepet(self, id: int, user: User):
        """
        Sepet id de ürün var mı ?(y/N) Bu ürün bu access token a sahip kullanıcının sepetinde mi?(y/N)
        y - y return product
        other return 404
        """
        pr = get_object_or_404(Sepet, SepetID = id, User = user)
        return pr


    def get(self, request):
        try:
            token = request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_User(UserAccessToken=token)
        tepes = self.get_Cart(User=user)
        serializer = UserSepetListSerializers(tepes, many = True)
        return Response(serializer.data)


    def post(self, request):
        """
        Eğer Ürün daha önce sepete eklenmişse ürün adedini gelen adet kadar artır.
        Eğer Ürürn daha önce sepete eklenmemişse de ürünü sepete ekle.
        {   
            "Urun": UrunID,
            "UrunADET": Urun adedi,
            "Token": "UserAccessTOKEN" 
        }
        """
        try:
            token = request.data["Token"]
            del request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_User(UserAccessToken=token)
        if 0 < request.data["UrunADET"] and user:
            request.data["User"] = user.UserID
            # product = get_object_or_404(Sepet, Urun = Urun(UrunID = request.data["Urun"]), User = user)
            product = Sepet.objects.filter(Urun = Urun(UrunID = request.data["Urun"]), User = user).first()
            if product:
                request.data["UrunADET"] = request.data["UrunADET"] + product.UrunADET
                serializer = UserSepetAddProductsSerializers(product, data=request.data)
            else:
                serializer = UserSepetAddProductsSerializers(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        """
        params da gelen ?p => ilgili ürünün sepete tutulduğu ID değeri ile
        ilgili ürün sepeten silinir
        {   
            "Token": "UserAccessTOKEN" 
        }
        """

        pid = request.query_params.get('p')
        try:
            token = request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_User(UserAccessToken=token)
        if pid and user:
            product = self.get_product_Sepet(id = pid, user=user)
            product.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_400_BAD_REQUEST)



class UserSiparisListAddDeleteAPIView(APIView):
    """
    Kullanıcının Sepete eklediği ürünlerin satın alınması, daha önce satın aldığı
    ürünlerin listelenmesi(sipariş geçmişi) ve sipariş iptal gibi işlemlerin gerçekleştiği APIView class ı
    """
    
    def get_User(self, UserAccessToken: str):
        user = get_object_or_404(User, TOKEN = UserAccessToken)
        return user


    def get_Siparis(self, SiparisID: int):
        siparis = get_object_or_404(Siparis, SiparisID= SiparisID)
        return siparis


    def get_Sepet_List(self, user: User):
        sepetList = Sepet.objects.filter(User=user)
        return sepetList


    def SepetListToSiparisDict(self, sepetList: list(), **kwargs):
        """
        Sepeteki değerleri Siparis serializerına göre ayarlama
        Sepetlist içindeki tüm ürünlerin maliyetini hesaplama
        """
        productsDict = dict()
        productsDict["productList"] = []
        SepetToplam = Decimal()
        for product in sepetList:
            SepetToplam = SepetToplam + (product.UrunADET * product.Urun.UrunFIYAT)
            productsDict["productList"].append({
                "User": product.User.UserID,
                "Urun": product.Urun.UrunID,
                **kwargs,
                "SiparisADET": product.UrunADET,
                "SiparisFIYAT": product.Urun.UrunFIYAT,
                "SiparisDURUM": SiparisStatus.status1
            })
        
        productsDict["SepetToplam"] = SepetToplam
        return productsDict


    def SepetCleaning(self, user:User):
        try:
            Sepet.objects.filter(User=user).delete()
            return True
        except:
            return False


    def get(self, request):
        """
        Kullanıcı siparis geçmişi, en son yapılan alışverişten ilk yapılana doğru sıralanır.
        """
        try:
            token = request.data["Token"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_User(UserAccessToken=token)
        siparis = Siparis.objects.filter(User = user).order_by("-SiparisTARIH")
        serializer = UserSiparisSerializers(siparis, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        """
        Siparislerin kullanıcının ürün sepetinden sipariş tablosuna eklenemsi ve satın alma işleminin tamamlanması.
        """
        try:
            token = request.data["Token"]
            userWALLET = Decimal(request.data["userWALLET"])
            address = dict(
            SiparisADRES = request.data["ADRES"][:300],
            SiparisADRESBASLIK = request.data["ADRESBASLIK"][:50],
            SiparisADRESALICI = request.data["ADRESALICI"][:50],
            SiparisADRESALICIGSM = request.data["ADRESALICIGSM"][:11],
            SiparisADRESALICITC = request.data["ADRESALICITC"][:11]
            )
            user = self.get_User(UserAccessToken=token)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sepetList = self.get_Sepet_List(user=user)
        siparisDict = self.SepetListToSiparisDict(sepetList=sepetList, **address)
        SepetToplam = siparisDict["SepetToplam"]
        siparisList = siparisDict["productList"]

        if siparisList == []:
            return Response({
                "islem":{
                    "message": "sepete herhangi bir ürün bulunamadı!"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        if SepetToplam <= userWALLET:
            for product in siparisList:
                serializer = UserSiparisSerializers(data=product)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "islem":{
                    "message": "Satın alma işlemi başarılı"
                }
            }, status= status.HTTP_201_CREATED) if self.SepetCleaning(user=user) else Response({
                "islem":{
                    "message": "Satın alma işlemi başarılı ama sepete birşeyler ters gitti!"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                "islem":{
                    "message": "Sanal cüzdanda yeterli miktarda bakiye yok!"
                }
            }, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        """
        Kullanıcı siparis güncelleme veya direkt siparis iptal
        """
        try:
            token = request.data["Token"]
            del request.data["Token"]
            sid = request.data["SiparisID"]
            del request.data["SiparisID"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = self.get_User(UserAccessToken=token)

        siparis = self.get_Siparis(SiparisID=sid)
        request.data["SiparisDURUM"]= SiparisStatus.status0 # Sipariş iptal
        serializer = UserSiparisSerializers(siparis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)