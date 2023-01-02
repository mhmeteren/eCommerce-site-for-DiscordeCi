from rest_framework import serializers

from ProductApp.models import Urun, Firma, AltKategori, Marka, UrunImg, UrunOzellik, OnerilenUrunler


class MarkaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Marka
        fields = '__all__'


class AltKategoriSerializers(serializers.ModelSerializer):
    Kategori = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AltKategori
        fields = ['Kategori', 'AltKategoriID', 'AltKategoriADI']



class FirmaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = ['FirmaID', 'FirmaADI']


class ProductImgSerializers(serializers.ModelSerializer):
    class Meta:
        model = UrunImg
        fields = '__all__'



class OzellikSerializers(serializers.ModelSerializer):
    class Meta:
        model = UrunOzellik
        exclude = ['UrunOzID', 'Urun']



class UrunImgSerializers(serializers.ModelSerializer):
    class Meta:
        model = UrunImg
        fields = ['UrunImgUrl']


class UrunSerializers(serializers.ModelSerializer):
    Firma = FirmaSerializers(read_only = True)
    AltKategori = AltKategoriSerializers(read_only = True)
    Marka = MarkaSerializers(read_only=True)
    ozellikler = OzellikSerializers(many= True, read_only=True)
    resimler = UrunImgSerializers(many=True, read_only = True)
    class Meta:
        model = Urun
        fields = '__all__'



class OnerilenUrunlerSerializers(serializers.ModelSerializer):
    OnerilenUrun = UrunSerializers(read_only=True)
    class Meta:
        model = OnerilenUrunler
        fields = '__all__'