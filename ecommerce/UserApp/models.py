from django.db import models
from hashlib import sha256

from ProductApp.models import Urun

class User(models.Model):

    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    UserSurename = models.CharField(max_length=50)
    UserGSM = models.CharField(max_length=11)
    UserEMAIL = models.CharField(max_length=100)
    UserPASSWORD = models.CharField(max_length=128)
    TOKEN = models.CharField(max_length=128, null=True, editable=False)
    TOKENDATE = models.DateTimeField(null=True)

    class Meta:
        db_table = "User"
        verbose_name= "User"
    
    def __str__(self):
        return f'{self.UserName} {self.UserSurename}'
 
    def auth(self):
        user = User.objects.filter(UserEMAIL= self.UserEMAIL, UserPASSWORD=self.UserPASSWORD).first()
        return user

    def save(self):
        self.UserPASSWORD = sha256(self.UserPASSWORD.encode('utf-8')).hexdigest()
        super(User, self).save()
    
    
    # """ilgili ürünü web sayfasında görme"""
    # def get_absolute_url(self):
    #     return '/learning/product/detail/%i/' % self.id

    # @property
    # def summary(self):
    #     return self.content[:50]    



class SiparisStatus(models.TextChoices):
    status1 = 'HAZIRLANMA ASAMASINDA', 'Hazırlanma aşamasında'
    status2 = 'KARGOYA VERILDI', 'Kargoya verildi'
    status3 = 'TESLIM EDILDI', 'Teslim edildi'

    

class Siparis(models.Model):

    SiparisID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, name="UserID")
    UrunID = models.ForeignKey(Urun, on_delete=models.PROTECT, name="UrunID")

    SiparisADRES = models.CharField(max_length=300)
    SiparisADET = models.IntegerField()
    SiparisFIYAT = models.DecimalField(max_digits=15, decimal_places=2)
    SiparisDURUM = models.CharField(max_length=50, choices=SiparisStatus.choices)
    SiparisTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Siparis"
        verbose_name= "Siparis"

    def __str__(self):
        return f'User: {self.UserID.UserName} {self.UserID.UserSurename}, Urun ID: {self.UrunID.UrunID}'



class UyeList(models.Model):

    UyeListID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, name="UserID")

    UyeListADI = models.CharField(max_length=50)
    UyeListTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UyeList"
        verbose_name= "UyeList"

    def __str__(self):
        return self.UyeListADI
    

class UrunList(models.Model):

    UrunListID = models.AutoField(primary_key=True)
    UyeListID = models.ForeignKey(UyeList, on_delete=models.CASCADE, name="UyeListID")
    UrunID = models.ForeignKey(Urun, on_delete=models.CASCADE, name="UrunID")

    class Meta:
        db_table = "UrunList"
        verbose_name= "UrunList"

    def __str__(self):
        return f'URUN ID: {self.UrunID.UrunID}, LISTE ADI: {self.UyeListID.UyeListADI}'
    
    def get_absolute_url(self):
        return '/p/product-detail/%i/' % self.UrunID.UrunID
    


    
class UrunYorum(models.Model):
    
    UrunYorumID = models.AutoField(primary_key=True)
    UrunID = models.ForeignKey(Urun, on_delete=models.CASCADE, name="UrunID")
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, name="UserID")

    Yorum = models.CharField(max_length=200)
    YorumTARIH = models.DateTimeField(auto_now_add=True)
    YorumDURUM = models.BooleanField(default=True)

    class Meta:
        db_table = "UrunYorum"
        verbose_name= "UrunYorum"

    def __str__(self):
        return f'UrunID: {self.UrunID.UrunID}'


class Sepet(models.Model):
    
    SepetID = models.AutoField(primary_key=True)
    UrunID = models.ForeignKey(Urun, on_delete=models.CASCADE, name="UrunID")
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, name="UserID")
    
    UrunADET = models.IntegerField()
    UrunTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Sepet"
        verbose_name= "Sepet"

    def __str__(self):
        return f'UrunID: {self.UrunID.UrunID}'


