from rest_framework import status
from rest_framework.response import Response

from UserApp.models import User, UrunList, UyeList, Urun
from UserApp.api.serializers import UserSerializers, UyeListSerializers, UrunListSerializers, UrunCreatSerializers

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class UserAccTokenAutAPIView(APIView):
    def get_object(self, token):
        dc_instance = get_object_or_404(User, TOKEN=token)
        return dc_instance


    def get(self, request, token):
        user = self.get_object(token)
        serializer = UserSerializers(user)
        return Response(serializer.data)



class UserUyeListAPIView(APIView):

    def get_UyeList_objects(self, UserID: int, ListName: str):
        """
        Kullanıcının ürün listelerinin listelendiği yer
        /userid/Listname/
        /2/Favoriler/
        """
        list_instance = get_object_or_404(UyeList, User= User(UserID=UserID), UyeListADI=ListName)
        return list_instance


    def get_product(self, uyeList: UyeList, urunid: int):
        """
        Eğer url e ?p parametresi ile GET isteği yapılırsa
        sadece ilgili ürünün bilgilerini dön.
        """
        product = get_object_or_404(UrunList, UyeList=uyeList, Urun=Urun(UrunID = urunid))
        return product


    def get(self, request, userid: int, listname: str):
        p = request.query_params.get('p')
        _uyeList = self.get_UyeList_objects(UserID=userid, ListName=listname)
        if p is None:
            serializer = UyeListSerializers(_uyeList)
        else:
            product = self.get_product(uyeList=_uyeList, urunid=p)
            serializer = UrunListSerializers(product)
        return Response(serializer.data)


    def post(self, request, userid: int, listname: str):
        p = request.query_params.get('p')
        _uyeList = self.get_UyeList_objects(UserID=userid, ListName=listname)
        print(_uyeList)
        if p is None:
            print(request.data)
            request.data["UyeList"] = _uyeList.UyeListID
            print(request.data)
            serializer = UrunCreatSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, userid: int, listname: str):
        p = request.query_params.get('p')
        _uyeList = self.get_UyeList_objects(UserID=userid, ListName=listname)
        if p:
            product = self.get_product(uyeList=_uyeList, urunid=p)
            product.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_400_BAD_REQUEST)

