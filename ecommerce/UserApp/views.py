from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from hashlib import sha256
from secrets import token_hex
from datetime import datetime

from .models import *


def getHASH(password):
    return sha256(password.encode('utf-8')).hexdigest()

def refreshAcc(request, UserId: int):
    user = User.objects.filter(UserID=UserId).first()

    if user:
        request.session["UserID"] =  user.UserID
        request.session["UserName"] =  user.UserName
        request.session["UserSurename"] =  user.UserSurename
        request.session["UserGSM"] =  user.UserGSM
        request.session["UserEMAIL"] =  user.UserEMAIL
        request.session["UserPASSWORD"] =  user.UserPASSWORD
        request.session["TOKEN"] =  user.TOKEN
        request.session["TOKENDATE"] =  str(user.TOKENDATE)

def signin(request):
    if request.session.get('UserID') is not None:
        return redirect("home")
        
    if request.method == 'POST':
        passwd = getHASH(request.POST["password"])
        user = User(UserEMAIL=request.POST["email"],  UserPASSWORD=passwd)
        user = User.auth(user)
        

        if not user:
            return render(request, 'signin.html', {
            'error': 'email veya password yanlış!!'
            })
        
        else:
            request.session.modified = True
            refreshAcc(request, user.UserID)            
            
            return redirect("home")

    return render(request, 'signin.html')

def logout(request):
    request.session.flush()
    return redirect('signin')

def signup(request):
    if request.session.get('UserID') is not None:
        return redirect("home")
    
    if request.method == 'POST':
        
        if User.objects.filter(UserEMAIL=request.POST["email"]).first() is not None:
            return render(request, 'signup.html', {
            'error': 'Bu mail adresi kullanilamaz!!'
            })
        
        
        
       
        user = User(UserName = request.POST["username"],
        UserSurename = request.POST["usersurename"],
        UserEMAIL = request.POST["email"],
        UserPASSWORD = request.POST["password"]
        )
        user.save()
        return render(request, 'signup.html', {
            'succ': 'Kayıt islemi basarili'
            })

    return render(request, 'signup.html')    


def home(request):
    try:
        UserID = int(request.session.get('UserID'))
    except TypeError:
        return redirect('signin')

    refreshAcc(request, UserID)
    content = { 
        'session': request.session
    }

    return render(request, 'Home.html', context=content)

@require_http_methods(["POST"])  
def AccUpdate(request):
    try:
        UserId = int(request.session.get('UserID'))
    except TypeError:
        return redirect('signin')
    
    if User.objects.filter(UserID=UserId, UserPASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'Home.html', {
            'session': request.session,
            'Accerror': 'Girilen parola yanlış'
        }) 

    email = str(request.POST["email"])
    if (request.session.get('UserEMAIL') != email) and User.objects.filter(UserEMAIL=email):
        return render(request, 'Home.html', {
            'session': request.session,
            'Accerror': 'Girilen email kullanılamaz!!'
         
        })
    
    User.objects.filter(UserID = UserId).update(UserName = request.POST["name"],
    UserSurename = request.POST["surename"], UserEMAIL = request.POST["email"]
    )

    refreshAcc(request, UserId)
    content = { 
    'session': request.session,
    'Accsuccess': 'işlem başarılı'
    }
    return render(request, 'Home.html', context=content)


@require_http_methods(["POST"])  
def resetTOKEN(request):
    try:
        UserId = int(request.session.get('UserID'))
    except TypeError:
        return redirect('signin')    

    if User.objects.filter(UserID=UserId, UserPASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'Home.html', {
            'session': request.session,
            'errorPassword': 'Girilen parola yanlış'
        }) 


    _TOKEN = token_hex(128)[:128] # len(token_hex(64)) => 128 ?
    User.objects.filter(UserID = UserId).update(TOKEN = _TOKEN,
    TOKENDATE = datetime.now()
    )

    refreshAcc(request, UserId)
    content = { 
    'session': request.session,
    'successToken': 'işlem başarılı'
    }
    return render(request, 'Home.html', context=content)

def product(request):
    return render(request, 'product-details.html')
