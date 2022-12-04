from django.db import models
from hashlib import sha256

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