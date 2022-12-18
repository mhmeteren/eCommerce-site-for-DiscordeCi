from rest_framework import serializers
from UserApp.models import User, UrunList, UyeList
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