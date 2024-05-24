from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Message
from django.http import JsonResponse
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin/')
def Myview(request):
    if not request.user.is_authenticated:
        return render(request,'signin.html')
    else:
        users=User.objects.exclude(username=request.user) 
        return render(request,'index.html',{"users":users})


@login_required(login_url='/signin/')
def chatroom(request,receiver):
    users=User.objects.exclude(username=request.user)
    receiver=User.objects.get(id=receiver)
    sender=request.user
    message=Message.objects.filter(sender=sender,receiver=receiver)|Message.objects.filter(sender=receiver,receiver=sender).order_by('timestamp')
    # unread_msg=Message.objects.filter(receiver=request.user,is_read=False)
    # for unread in unread_msg:
    #     unread.is_read=True
    #     unread.save()
    data={'message':list(message.values()),
           'sender':request.user.id,
           'receiver_id':receiver.id,
           'receiver_name':receiver.username
           }
           
    return JsonResponse(data,safe=False)
    # return render(request,'chatroom.html',{"message": message,"sender": sender,"receiver": receiver,'users':users})

# def unread_message(request):
#     receiver=request.user.id
#     unread_msg=Message.objects.filter(receiver=receiver,is_read=False)
#     unread_msglist=[
#         {
#             'sender':unread.sender.username,
#             'receiver':unread.receiver.username,
#             'message':unread.message,
#             'is_read':unread_msg.count(),
#         }
#         for unread in unread_msg
#     ]
#     return JsonResponse(unread_msglist,safe=False)


def signup(request):
    if request.method=='POST':
        username=request.POST.get("username")
        mail=request.POST.get("mail")
        password=request.POST.get("password")
        confirm_pass=request.POST.get("confirm_pass")

        if username=="" or mail=="" or password=="" or confirm_pass=="":
            messages.warning(request,'Empty Values not accepted')
            return redirect('/signup')
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(request,f'Username already taken')
                return redirect('/signup')
            if User.objects.filter(email=mail).exists():
                messages.warning(request,f'Mail already exists')
                return redirect('/signup')
            if password==confirm_pass:
                model=User.objects.create_user(username=username,email=mail,password=password)
                model.save()
                messages.success(request,'Account created sccessfully')
                return redirect('signin')
            else:
                messages.warning(request,'Confirm password not match!')
                return redirect('/signup')    
    return render(request,'signup.html')

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username=="" or password=="":
            messages.warning(request,'Empty values not accepted')
            return redirect('/signin')
        else:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.warning(request,"Username or Password Incorrect")
                return redirect('signin')
    return render(request,'signin.html')

    
def logout_view(request):
    logout(request)
    messages.success(request,'successfully logout')
    return redirect('signin')