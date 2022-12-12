from django.db import models
from hashlib import sha256



class Firma(models.Model):

    FirmaID = models.AutoField(primary_key=True)
    FirmaADI = models.CharField(max_length=50)
    FirmaEMAIL = models.CharField(max_length=50)
    FirmaPASSWD = models.CharField(max_length=128)

    class Meta:
        db_table = "Firma"
        verbose_name= "Firma"

    def __str__(self):
        return self.FirmaADI

    def save(self):
        self.FirmaPASSWD = sha256(self.FirmaPASSWD.encode('utf-8')).hexdigest()
        super(Firma, self).save()



class Marka(models.Model):

    MarkaID = models.AutoField(primary_key=True)
    MarkaADI = models.CharField(max_length=50)

    class Meta:
        db_table = "Marka"
        verbose_name= "Marka"

    def __str__(self):
        return self.MarkaADI


class Kategori(models.Model):
    
    KategoriID = models.AutoField(primary_key=True)
    KategoriADI = models.CharField(max_length=50)
    KategoriTARIH = models.DateTimeField(auto_now_add=True)
    KategoriDURUM = models.BooleanField(default=False)

    class Meta:
        db_table = "Kategori"
        verbose_name= "Kategori"

    def __str__(self):
        return self.KategoriADI

class AltKategori(models.Model):
    
    AltKategoriID = models.AutoField(primary_key=True)
    Kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, name="Kategori")
    AltKategoriADI = models.CharField(max_length=50)
    AltKategoriTARIH = models.DateTimeField(auto_now_add=True)
    AltKategoriDURUM = models.BooleanField(default=False)

    class Meta:
        db_table = "AltKategori"
        verbose_name= "AltKategori"

    def __str__(self):
        return self.AltKategoriADI



class UrunColor(models.TextChoices):
    KIRMIZI = 'KIRMIZI', 'kırmızı'
    MAVI = 'MAVI', 'mavi'
    YESIL = 'YESIL', 'yeşil'
    SARI = 'SARI', 'sarı'
    TURUNCU = 'TURUNCU', 'turuncu'
    SIYAH = 'SIYAH', 'siyah'




class Urun(models.Model):

    UrunID = models.AutoField(primary_key=True)
    Firma = models.ForeignKey(Firma, on_delete=models.CASCADE, name="Firma")
    Kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, name="Kategori")
    AltKategori = models.ForeignKey(AltKategori, on_delete=models.CASCADE, name="AltKategori")
    Marka = models.ForeignKey(Marka, on_delete=models.CASCADE, name="Marka")

    UrunKODU = models.CharField(max_length=50)
    UrunADI = models.CharField(max_length=100)
    UrunFIYAT = models.DecimalField(max_digits=15, decimal_places=2)
    UrunACIKLAMA = models.TextField(max_length=500)
    UrunRENK = models.CharField(max_length=20, choices=UrunColor.choices)
    UrunTARIH = models.DateTimeField(auto_now_add=True)
    UrunDURUM = models.BooleanField(default=False)
    UrunSTOK = models.BigIntegerField()

    class Meta:
        db_table = "Urun"
        verbose_name= "Urun"
    
    def __str__(self):
        return self.UrunADI

    def get_absolute_url(self):
        return '/p/product-detail/%i/' % self.UrunID

class UrunImg(models.Model):

    UrunImgID = models.AutoField(primary_key=True)
    Urun = models.ForeignKey(Urun, on_delete=models.CASCADE, name="Urun", related_name="resimler")
    UrunImgUrl = models.CharField(max_length=200)

    class Meta:
        db_table = "UrunImg"
        verbose_name= "UrunImg"

    def __str__(self):
        return f'UrunID: {self.Urun.UrunID}'
    
    def get_absolute_url(self):
        return '/p/product-detail/%i/' % self.Urun.UrunID

class UrunOzellik(models.Model):
    UrunOzID = models.AutoField(primary_key=True)
    Urun = models.ForeignKey(Urun, on_delete=models.CASCADE, name="Urun", related_name="ozellikler")
    UrunOzType = models.CharField(max_length=50)
    UrunOzValue = models.CharField(max_length=50)

    class Meta:
        db_table = "UrunOzellik"
        verbose_name= "UrunOzellik"
    
    def __str__(self):
        return f'UrunID: {self.Urun.UrunID} - Type: {self.UrunOzType} - Value: {self.UrunOzValue}'
