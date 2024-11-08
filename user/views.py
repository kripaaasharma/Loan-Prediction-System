from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as log
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.form import LoanForm





def index(request):
    return render(request,'home.html')





def login(request):
    return render(request,'user/login.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']    
        
        user = authenticate(request,username=username, password=password)

        if user is not None:
            if user.is_superuser == 0:

                log(request,user)
                return redirect('/home')

            else:
                messages.error(request,"Username and Password Don't Match, Please Try Again !")

                return redirect("/user/login")


        else:
            messages.error(request,"Username and Password Don't Match, Please Try Again !")

            return redirect("/user/login")

    else:
            messages.error(request,"Something is worng with your form validation, Please Try Again !")

            return redirect("/user/login")


def register(request):
    return render(request,'user/register.html')

# To register User

def register_user(request):
    if request.method == "POST":
        User.objects.create_user(
            first_name = request.POST['fullname'],
            username = request.POST['username'],
            password = request.POST['password'],
            email = request.POST['phonenumber'],

        )
        return redirect('/user/login')
    


    else:
        return render(request, '404.html', status=404)

def log_out(request):
    logout(request)
    return redirect('/home')

def contact(request):

    return render(request,'contact.html')

@login_required(login_url='/user/login')

def loan(request):
    return render(request, 'loan.html')


@login_required(login_url='/user/login')

def addloan(request,uid):


    if request.method == 'POST':
        # Create a new LoanModel instance with the submitted data
        loan_instance = LoanForm(
            request.POST
        )

        if loan_instance.is_valid():
            loan_instance.save()
        # # else:
        # #     print(loan_instance.errors)


    return redirect('/index')


# def addloan(request):
#     if request.method == 'POST':
#         form = LoanForm(request.POST)
#         if form.is_valid():
#             loan_instance = form.save(commit=False)
#             loan_instance.user_id = request.user
#             loan_instance.save()
#             return redirect('/index')
#     else:
#         form = LoanForm()
#     return render(request, 'loan.html', {'form': form})


