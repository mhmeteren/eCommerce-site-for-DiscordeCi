from rest_framework import serializers
from UserApp.models import User, UrunList, UyeList, Sepet
from ProductApp.api.serializers import UrunSerializers

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['UserName', 'UserSurename', 'TOKEN', 'TOKENDATE']
        read_only_fields = ['UserName', 'UserSurename', 'TOKEN', 'TOKENDATE']



class UrunListSerializers(serializers.ModelSerializer):
    Urun = UrunSerializers(read_only = True)
    class Meta:
        model = UrunList
        exclude = ["UyeList"]



class UyeListSerializers(serializers.ModelSerializer):
    UrunList = UrunListSerializers(many = True, read_only = True)
    class Meta:
        model = UyeList
        fields = '__all__'



class UrunCreatSerializers(serializers.ModelSerializer):
    class Meta:
        model = UrunList
        fields = '__all__'


class UserProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UyeList
        fields = '__all__'


class UserSepetListSerializers(serializers.ModelSerializer):
    Urun = UrunSerializers(read_only = True)
    class Meta:
        model = Sepet
        fields = '__all__'
        read_only_fields = ["User"]


class UserSepetAddProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sepet
        fields = '__all__'