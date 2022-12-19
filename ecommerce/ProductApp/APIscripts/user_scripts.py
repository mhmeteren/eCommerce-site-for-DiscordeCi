from UserApp.models import User

def User_TOKEN_Control(token):
    """
    API isteğinde gelen user account access token ile uyuşan bir 
    kullanıcı olup olmadığını kontrol et.
    [ProductsSearchListAPIView, ProductsFilterListAPIView]

    NOT: Normalde gelen token a uyan kullanıcı varsa o kullanıcıya göre
    ürün öner olması gerek ama onu şuan ekliyemem çünkü proje yetişmez.
    """
    try:
        user = User.objects.get(TOKEN = token)
        return user
    except:
        return False