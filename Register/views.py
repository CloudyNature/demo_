from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse('Your passwords do not match')
        else:
            myuser = User.objects.create_user(username,email,password1)
            myuser.save()
            send_mail(
                "You have just registered your account",
                "Thanks for registering",
                "smallinfo.nature@gmail.com",
                [email],
                fail_silently=False,
            )
            return redirect('login')


    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        email = user.email
        if user is not None:
            login(request, user)
            send_mail(
                "Login Alert",
                "You have just login to your account",
                "smallinfo.nature@gmail.com",
                [email],
                fail_silently=False,
            )
            return redirect('home')
        else:
            return HttpResponse('Username and password are incorrect')

    return render(request, 'login.html')




@login_required(login_url='login')
def Home(request):
    return render(request, 'home.html')




def Logout(request):
    logout(request)
    return redirect('login')

def get_last_login_time(username):
    try:
        user = User.objects.get(username=username)
        last_login_time = user.last_login
        return last_login_time
    except User.DoesNotExist:
        return None


@login_required
def show_last_login(request):
    last_login_time = request.user.last_login
    return HttpResponse(f'Last login: {last_login_time}')




