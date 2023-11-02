#from fnmatch import fnmatch
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog, User, Resume , Education, Experience, JobNotifications, JobReceived
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.template.loader import render_to_string
from uuid import uuid4
# import weasyprint




# Create your views here.

def emailer(subject,toEmail,message):
    send_mail(
        subject,
        message,
        'developer@mapralglobal.com',
        [toEmail,'developer@mapralglobal.com'],
        fail_silently=False,
    )


def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = "Thank you for contacting Mapral Global"
        message = "We will get back to you soon"
        emailer(subject,email,message)
        messages.success(request, 'Thank you for contacting us. We will get back to you soon.')
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']
        message = "Name: " + name + "with email id" + email + "and phone number" + phone + "wants to contact you regarding" + subject + "and the message is" + message
        emailer(subject,"developer@mapralglobal.com",message)
        messages.success(request, 'Thank you for contacting us. We will get back to you soon.')
    return render(request, 'contact.html')

def blog(request):
    blogs = Blog.objects.all()
    blogs = blogs.filter(status=1)
    return render(request, 'blog.html',{'blogs':blogs})
    
def services(request):
    return render(request, 'services.html')

def blogItem(request,slug):
    blog = Blog.objects.filter(slug=slug)
    blog = blog[0]
    return render(request, 'blogItem.html',{'blog':blog})

def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_verified == True:
                login(request, user)
                messages.success(request, 'You are logged in successfully.')
                return redirect('/')
            else:
                messages.success(request, 'Please verify your email address to login.')
                return redirect('/login')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('/login')

    return render(request, 'login.html')

def signView(request):
    if request.method == 'POST':
        role = request.POST['role']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        try:
            gender = request.POST['gender']
            qualification = request.POST['qualification']
        except:
            gender = None
            qualification = None

        password = request.POST['pass']
        confirmPassword = request.POST['pass1']

        try:
            companyName = request.POST['companyName']
            companyAbout = request.POST['companyAbout']
        except:
            companyName = None
            companyAbout = None
        
        user = User.objects.filter(email=email)
        if user.count() > 0:
            messages.error(request, 'Email already exists.')
            return redirect('/signup')

        if password == confirmPassword:
            user = User.objects.create_user(email=email,password=password,fname=fname,lname=lname,phone=phone,gender=gender,qualification=qualification,company=companyName,aboutCompany=companyAbout)
            user.save()
            token = str(uuid4())
            user.token = token
            user.save()
            email = user.email
            subject = "Verify your email address"
            message = "Please click on the link below to verify your email address. http://127.0.0.1:8000/verifyEmail/" + token + " Thank you."
            emailer(subject,email,message)
            messages.success(request, 'Your account has been created successfully. Please verify your email to continue.')
            return redirect('/login')
        else:
            messages.error(request, 'Password and Confirm Password does not match.')
            return redirect('/signup')



    return render(request, 'signup.html')


def verifyEmail(request,token):
    user = User.objects.filter(token=token)
    if user.count() > 0:
        user = user[0]
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified successfully.')
        return redirect('/login')
    else:
        messages.error(request, 'Invalid token.')
        return redirect('/login')

def rbuilder(request):
    if request.user.is_authenticated:
        user = request.user
        email = user.email
        user = User.objects.filter(email=email)
        user = user[0]
        # return render(request, 'resumebuilder.html',{'user':user})

        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            city = request.POST['city']
            profilePic = request.FILES['img']
            jobTitle = request.POST['jtitle']
            aboutWork = request.POST['aboutWork']
            skills = request.POST['skills']
            companyName = request.POST['cname']
            jobPosition = request.POST['jobPosition']
            date = request.POST['date']
            jobDesc = request.POST['jobDesc']
            resp = request.POST['resp']
            school = request.POST['school']
            degree = request.POST['degree']
            sdate = request.POST['sdate']
            language = request.POST['lang']
            
            ruser = request.user
            resume = Resume.objects.create(user=ruser,name=name,email=email,phone=phone,jobTitle=jobTitle,aboutWork=aboutWork,skills=skills,profilePic=profilePic,city=city,languages=language)
            resume.save()

            user = User.objects.filter(email=email)
            user = user[0]
            education = Education.objects.create(user=user,schoolName=school,degree=degree,startDate=sdate)
            education.save()
            experience = Experience.objects.create(user=user,companyName=companyName,jobPosition=jobPosition,startDate=date,jobDescription=jobDesc,responsibilities=resp)
            experience.save()

            messages.success(request, 'Your resume has been created successfully.')
            return redirect('/')

        return render(request, 'resumebuilder.html',{'user':user})

    else:
        return redirect('/login')


def resume(request,id):
    if request.user.is_authenticated:
        user = request.user
        resume = Resume.objects.filter(id=id)
        education = Education.objects.filter(user=user)
        try:
            education = education[0]
        except:
            education = None
        experience = Experience.objects.filter(user=user)
        try:
            experience = experience[0]
        except:
            experience = None
        if resume.count() > 0:
            resume = resume[0]
            initials = resume.name.split(' ')
            initials = initials[0][0] + initials[1][0]
            skills = resume.skills.split(',')

            # rendered = render_to_string('resume.html', {'resume':resume,'education':education,'experience':experience,'skills':skills,'initials':initials})
            # pdf = weasyprint.HTML(string=rendered).write_pdf()
            # response = HttpResponse(pdf, content_type='application/pdf')
            # return HTTPResponse(response, content_type='application/pdf')

    
            return render(request, 'resume.html',{'resume':resume,'initials':initials,'skills':skills,'education':education,'experience':experience})
        else:
            return redirect('/rbuilder')
    return redirect('/login')

def jobUpdate(request):
    open = True
    notify = JobNotifications.objects.all()
    return render(request, 'jobUpdate.html' ,{'open':open,'notify':notify})

def jobUpdate1(request):
    open = False
    update = JobReceived.objects.all()
    return render(request, 'jobUpdate.html' ,{'open':open,'update':update})

def logoutView(request):
    logout(request)
    messages.success(request, 'You are logged out successfully.')
    return redirect('/')

def resumeList(request):
    if request.user.is_authenticated:
        user = request.user
        resume = Resume.objects.filter(user=user)
        if resume.count() > 0:
            resume = resume[0]
            return render(request, 'res.html',{'resume':resume})
        else:
            return redirect('/rbuilder')


    else:
        return redirect('/login')


def resumeDelete(request,id):
    if request.user.is_authenticated:
        user = request.user
        resume = Resume.objects.filter(id=id)
        experience = Experience.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        if resume.count() > 0:
            resume = resume[0]
            resume.delete()
            experience.delete()
            education.delete()
            messages.success(request, 'Your resume has been deleted successfully.')
            return redirect('/rbuilder')
        else:
            return redirect('/rbuilder')
    else:
        return redirect('/login')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        resume = Resume.objects.filter(user=user)
        if resume.count() > 0:
            resume = resume[0]
            return render(request, 'dashboard.html',{'resume':resume})
        else:
            messages.success(request, 'Please create your resume first.')
            return redirect('/rbuilder')
    return render(request, 'dashboard.html')


