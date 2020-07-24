from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Contact,BlogPost,PersonalBlogPost
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request,'index.html')
    

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('num')
        desc=request.POST.get('desc')
        from_email=settings.EMAIL_HOST_USER
        
        if len(phone)<10:
            messages.warning(request,"Please Provide Valid Phone.no!!")
            return render(request,'contact.html') 
        try:
            if len(phone)>10:
                messages.warning(request,"Please Provide Exactly 10 digits!!")
                return render(request,'contact.html')
        except ValueError as error:
                pass
        

        if len(desc)<5:
            messages.warning(request,"Please Provide Valid Description!!")
            return redirect('/contact')  

        connection=mail.get_connection()

        connection.open()
        email1=mail.EmailMessage(name,f'email: {email} \nphone number: {phone} \nQuery : {desc}',from_email,['syedaafreen182@gmail.com'],connection=connection)
        connection.send_messages([email1])
        connection.close()
        

        connection.open()
        email2=mail.EmailMessage(f'Hello {name}','Your Response has been recorded successfully,We will get back to you soon ASAP',from_email,[email],connection=connection)
        connection.send_messages([email2])
        connection.close()
        myusercontact=Contact(name=name,email=email,phone=phone,desc=desc)

        myusercontact.save()
        messages.info(request,"Your Response Has Been Recorded Successfully. ThankYou!")
        return redirect('/')
    return render(request,'contact.html')

def handleSignup(request):
    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1 != pass2:
            messages.warning(request,"Password does'nt Match,Please Try Again!")
            return redirect('/signup')
        try:
            if User.objects.get(username=username):
                messages.warning(request,"UserName Already Taken!")
                return redirect('/signup')
        except Exception as identifier:
                pass   
            
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.warning(request,"Signup Successfull. ThankYou!")
        return redirect('/login')
        

    return render(request,'signup.html')

def handleLogin(request):
    if request.method == "POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        user=authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            messages.info(request,"Login SuccessFull.")
            return redirect("/")
        else:
           messages.error(request,"Invalid Credentials.")
           return redirect("/login")
    return render(request,'login.html')

def friends(request):
    if not request.user.is_authenticated:
        messages.error(request,"Please login and Try Again")
        return redirect('/login')

    allPosts=BlogPost.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'friends.html',context)

def handleBlog(request):
    if not request.user.is_authenticated:
        messages.error(request,"Please login and Try Again")
        return redirect('/login')

    posts=PersonalBlogPost.objects.all()
    context = {'posts':posts}
    return render(request,'handleblog.html',context)
 

def about(request):
    return render(request,'about.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Successfull.")
    return redirect('/login')

def search(request):
    query=request.GET['search']
    if len(query)>80:
        allPosts = BlogPost.objects.none()
    else:
        allPostsTitle=BlogPost.objects.filter(title__icontains=query)
        allPostsContent=BlogPost.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"No Search Results Found!!")
    params={'allPosts':allPosts,'query':query}

    return render(request,'search.html',params)