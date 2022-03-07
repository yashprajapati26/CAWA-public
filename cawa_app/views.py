from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
from random import *
from django.conf import settings
from .utils import *
from django.contrib import messages
import random
import string
import datetime

from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password , check_password

# Create your views here.
app_data = {}

def home(request):
    notice = Notice.objects.all().order_by("-id")
    return render(request,'index.html',{'notice':notice})

def about(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def gallery(request):
    return render(request,'gallery.html')

def pricing(request):
    RegCat = RegCategory.objects.all()
    return render(request,'pricing.html',{'RegCat':RegCat})

def shedule_detail(request,pk):
    theme = Theme.objects.all()
    theme_pk = Theme.objects.get(pk=pk)
    print(theme_pk)
    sub_theme=theme_pk.Sub_themes

    try:
        conf = Conference.objects.get(Conference_Theme=theme_pk)
        print(conf)
        return render(request,'schedule.html',{'theme':theme,'sub':sub_theme,'conf':conf})
    except:
        theme1=theme_pk.Theme_name
        return render(request,'schedule.html',{'theme':theme,'sub':sub_theme,'theme1':theme1})


def schedule(request):
    theme = Theme.objects.all()
    return render(request,'schedule.html',{'theme':theme})

def single_post(request):
    return render(request,'single-post.html')

def speakers(request):
    winners = Winners.objects.all().order_by("-id")
    return render(request,'speakers.html',{'winners':winners})

def sponsors(request):
    return render(request,'sponsors.html')

def login(request):
    try:
        del request.session['name']
        del request.session['email']
        del request.session['image']
        del request.session['role']
        return redirect(login)
    except:
        return render(request,'login.html')

def signup(request):
    try:
        del request.session['name']
        del request.session['email']
        del request.session['image']
        del request.session['role']
        return redirect(login)
    except:
        return render(request,'signup.html')

def otp(request):
    return render(request,'otp.html')

def etemp(request):
    return render(request,'otpVerification_emailTemplate.html')


# def feedback(request):
#     feeds = FeedBack.objects.all().order_by("-Feedback_Date")
#     theme = Theme.objects.all()
    
#     try:
#        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
#        p_user=Participant.objects.get(Parti_user=user)
#        if user:
#            if request.method=="POST":
#                vtheme=request.POST['ltheme']
#                vfeedback=request.POST['lfeedback']
#                request.session['image']=p_user.Image.url
#                new_feed=FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
#                return render(request,'Feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#            else:
#                 return render(request,'Feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#     except:
#         return render(request,'Feedback.html',{'feeds':feeds,'theme':theme})


def load_feeds():
    feeds = FeedBack.objects.all().order_by("-Feedback_Date")
    theme = Theme.objects.all()
    app_data['feeds'] = feeds
    app_data['theme'] = theme

def feedback_page(request):
    load_feeds()
    return render(request,'Feedback.html', app_data)

def feedback(request):
    if request.method=="POST":
        vtheme=request.POST['ltheme']
        vfeedback=request.POST['lfeedback']
        #request.session['image']=p_user.Image.url
        try:
            user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
            app_data['user'] = user
            p_user=Participant.objects.get(Parti_user=user)
            FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
            return redirect(feedback_page)
        except:
            app_data['msg'] = ''
            return redirect(feedback_page)
    else:
        return redirect(feedback_page)



def create_user(request):
    if request.method=="POST":
        vtitle=request.POST['stitle']
        vfname=request.POST['sfname']
        vlname=request.POST['slname']
        vemail=request.POST['semail']
        vpass=request.POST['spass']
        vcpass=request.POST['scpass']
        vrole=request.POST['srole']

        try:
            check_mail=User.objects.get(Email=vemail,Role=vrole)
            if check_mail:
                msg="This email is allready registered!"
                return render(request,'signup.html',{'msg':msg})
        except:
            if vtitle=="" or vfname=="" or vemail=="" or vlname=="" or vpass=="" or vcpass=="":
                msg="please enter all fileds"
                return render(request,'signup.html',{'msg':msg})
            elif vpass!=vcpass:
                msg="Password & Confirm password does not matched"
                return render(request,'signup.html',{'msg':msg})
            else:
                #User.objects.create(Firstname=vfname,Lastname=vlname,Email=vemail,Password=vpass,Role=vrole)
                # reciever=[vemail,]
                # subject="OTP For Registration:"
                # otp=random.randint(1000,9999)
                # message="Your OTP For Registration is :"+str(otp)
                # email_from=settings.EMAIL_HOST_USER
                # send_mail(subject, message, email_from, reciever)

                otp1 = randint(100000,999999)
                otp = make_password(str(otp1))
                print(otp)
                email_Subject = "OTP For SignUp Verification"
                sendmail(email_Subject,'otpVerification_emailTemplate',vemail,{'name':'Dear User','otp':otp1})

                return render(request,'otp.html',{'gotp':otp,'email':vemail,'title':vtitle,'fname':vfname,'lname':vlname,'pass':vpass,'role':vrole})
    else:
        return render(request,"signup.html")

def otp_var(request):

        votp=request.POST['otp']
        vgotp=request.POST['gotp']
        vemail=request.POST['email']
        vtitle=request.POST['title']
        vfname=request.POST['fname']
        vlname=request.POST['lname']
        vpass=request.POST['pass']
        vrole=request.POST['role']


        print("OTP : ",votp)
        print("GOTP : ",vgotp)
        print("Email : ",vemail)

        match_otp=check_password(votp,vgotp)
        print(match_otp)
       
        if match_otp:
            
            user = User.objects.create(Title=vtitle,Firstname=vfname,Lastname=vlname,Email=vemail,Password=vpass,Role=vrole)
            print("Password -------->")
            print(user.Password)

            user.Password = make_password(user.Password) 
            user.save()
            print("Encryption-------->")
            print(user.Password)

            new_user=User.objects.get(Email=vemail,Role=vrole)
            if vrole=="participant":
                newp=Participant.objects.create(Parti_user=new_user,Phone=0)
            elif vrole=="researcher":
                newr1=Researcher.objects.create(Res_user=new_user,Phone=0)
            elif vrole=="reviewer":
                newr2=Reviewer.objects.create(Reviewer_user=new_user,Phone=0)

            
            msg="OTP verified successfully."
            return render(request,'login.html',{'msg':msg})
        else:
            msg="Please enter correct otp!"
            return render(request,'otp.html',{'msg':msg,'gotp':vgotp,'email':vemail,'title':vtitle,'fname':vfname,'lname':vlname,'pass':vpass,'role':vrole})


def showlogin(request):
    if request.method=="POST":
        notice = Notice.objects.all().order_by("-id")
        vrole=request.POST['lrole']
        vemail=request.POST['lemail']
        vpass=request.POST['lpass']
        
        try:
            
            user=User.objects.get(Email=vemail,Role=vrole)
            app_data['user'] = user
            password=user.Password
            print("---->",password)
            print(vpass)
            match_pass=check_password(vpass,password)
            print(match_pass)

            if match_pass:
                if user.Role=="participant":
                    p_user=Participant.objects.get(Parti_user=user)
                    request.session['name']=user.Firstname
                    request.session['email']=user.Email
                    request.session['role']=user.Role
                    request.session['image']=p_user.Image.url
                    return render(request,'index.html',{'notice':notice})

                elif user.Role=="researcher":
                    re_user=Researcher.objects.get(Res_user=user)
                    request.session['name']=user.Firstname
                    request.session['email']=user.Email
                    request.session['role']=user.Role
                    request.session['image']=re_user.Image.url
                    return render(request,'Researcher_templates/researcher_index.html',{'notice':notice})

                elif user.Role=="reviewer":
                    print("rev")
                    r_user=Reviewer.objects.get(Reviewer_user=user)
                    request.session['name']=user.Firstname
                    request.session['email']=user.Email
                    request.session['role']=user.Role
                    request.session['image']=r_user.Image.url
                    print("rev2")
                    return render(request,'Reviewer_templates/reviewer_index.html',{'notice':notice})
            else:
                msg="Password is incorrect !"
                return render(request,'login.html',{'msg':msg})

        except Exception as e:
            print("Login Exception---------------------->",e)
            if vemail=="" or vpass=="":
                msg="Please enter both fileds!"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Email is not registered !"
                return render(request,'login.html',{'msg':msg})
            
    else:       
        return render(request,"login.html")

        
def showemail(request):
    return render(request,"showemail.html")

def sendotp(request):
    vrole=request.POST['srole']
    vemail=request.POST['email']

    print("role :",vrole)

    user=User.objects.filter(Email=vemail,Role=vrole)
    if user:
        otp = randint(100000,999999)
        email_Subject = "OTP For Forget Passwrod"
        sendmail(email_Subject,'otpVerification_emailTemplate',vemail,{'name':'Dear User','otp':otp})

        return render(request,"otp_forget_pw.html",{'gotp':otp,'email':vemail,'role':vrole})
    else:
        msg="Enter valid Email And Role" 
        return render(request,"showemail.html",{'msg':msg})

def otp_forget_pw(request):

    vrole=request.POST['role']
    vemail=request.POST['email']
    vgotp=request.POST['gotp']
    votp=request.POST['otp']
    
    if vgotp==votp:
        return render(request,"forget_password.html",{'email':vemail,'role':vrole})
    else:
        msg="Incorect OTP !"
        return render(request,"otp_forget_pw.html",{'msg':msg,'email':vemail,'gotp':vgotp,'role':vrole})


def forget_password(request):

    vrole=request.POST['role']
    vemail=request.POST['email']
    vpassword=request.POST['npass']
    vcpassword=request.POST['cpass']
    print("-------------------")
    print(vrole)
    user=User.objects.get(Email=vemail,Role=vrole)
    
    if vpassword==vcpassword:
        # user.Password=vpassword
        # user.save()
        user.Password = make_password(vpassword) 
        user.save()
        msg="Password changed successfully."
        return render(request,"login.html",{'msg':msg})
    else:
        msg="Password does not match!"
        return render(request,"forget_password.html",{'msg':msg,'email':vemail,'role':vrole})


def logout(request):
    try:
        del request.session['name']
        del request.session['email']
        del request.session['image']
        del request.session['role']
        return render(request,'login.html')
    except:
        return render(request,'login.html')


def profile(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    p_user=Participant.objects.get(Parti_user=user)
    if request.method=="POST":
        user.Firstname=request.POST['fname']
        user.Lastname=request.POST['lname']
        p_user.Phone=request.POST['phone']
        p_user.About=request.POST['about']
        p_user.Address=request.POST['address']
        try:
            if request.FILES['pimage']:
                p_user.Image=request.FILES['pimage']
                user.save()
                p_user.save()
                del request.session['image']
                request.session['image']=p_user.Image.url
                del request.session['name']
                request.session['name']=user.Firstname
                msg="Profile Updated Successfully."
                return render(request,"particiapnt_profile.html",{'user':user,'p_user':p_user,'msg':msg})
        except:
            user.save()
            p_user.save()
            del request.session['name']
            request.session['name']=user.Firstname
            msg="Profile Updated Successfully."
            return render(request,"particiapnt_profile.html",{'user':user,'p_user':p_user,'msg':msg})
    else:
        return render(request,"particiapnt_profile.html",{'user':user,'p_user':p_user})



def change_password(request):
    user = User.objects.get(Email=request.session['email'],Role=request.session['role'])

    if request.method=="POST":
        v_old_pass=request.POST['l_old_pass']
        v_new_pass=request.POST['l_new_pass']
        v_new_confirm_pass=request.POST['l_new_confirm_pass']

        password=user.Password
        print("---->",password)
        match_pass=check_password(v_old_pass,password)
        print(match_pass)
        same_pass=check_password(v_new_pass,password)
        print(same_pass)

        # if v_old_pass!=user.Password:
        #     msg="Old Password Is Incorrect"
        #     return render(request,'change_password.html',{'msg':msg})

        # elif v_old_pass==v_new_pass:
        #     msg="Please Enter Different Password"
        #     return render(request,'change_password.html',{'msg':msg})

        # elif v_new_pass==v_new_confirm_pass:
        #     user.Password=v_new_pass
        #     user.save()
        #     return redirect('logout')
        # else:
        #     msg="New Password And Confirm Password Is Not Matched"
        #     return render(request,'change_password.html',{'msg':msg})

        if not match_pass:
            msg="Old Password Is Incorrect"
            return render(request,'change_password.html',{'msg':msg})
        elif same_pass:
            msg="Please Enter Different Password"
            return render(request,'change_password.html',{'msg':msg})
        elif v_new_pass==v_new_confirm_pass:
            user.Password = make_password(v_new_pass) 
            user.save()
            return redirect('logout')
        else:
            msg="New Password And Confirm Password Is Not Matched"
            return render(request,'change_password.html',{'msg':msg})

    else:
        return render(request,'change_password.html')

#---------------------------Researcher views-----------------------------------------------------

def researcher_profile(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user= Researcher.objects.get(Res_user=user)
    if request.method=="POST":
        user.Firstname=request.POST['fname']
        user.Lastname=request.POST['lname']
        researcher_user.Phone=request.POST['phone']
        researcher_user.About=request.POST['about']
        researcher_user.Address=request.POST['address']
        try:
            if request.FILES['pimage']:
                researcher_user.Image=request.FILES['pimage']
                user.save()
                researcher_user.save()
                del request.session['image']
                request.session['image']=researcher_user.Image.url
                del request.session['name']
                request.session['name']=user.Firstname
                msg="Profile Updated Successfully."
                return render(request,"Researcher_templates/researcher_profile.html",{'user':user,'researcher_user':researcher_user,'msg':msg})
        except:
            user.save()
            researcher_user.save()
            del request.session['name']
            request.session['name']=user.Firstname
            msg="Profile Updated Successfully."
            return render(request,"Researcher_templates/researcher_profile.html",{'user':user,'researcher_user':researcher_user,'msg':msg})
    else:
        return render(request,"Researcher_templates/researcher_profile.html",{'user':user,'researcher_user':researcher_user})

def researcher_change_password(request):
    user = User.objects.get(Email=request.session['email'],Role=request.session['role'])

    if request.method=="POST":
        v_old_pass=request.POST['l_old_pass']
        v_new_pass=request.POST['l_new_pass']
        v_new_confirm_pass=request.POST['l_new_confirm_pass']

        password=user.Password
        print("---->",password)
        match_pass=check_password(v_old_pass,password)
        print(match_pass)
        same_pass=check_password(v_new_pass,password)
        print(same_pass)

        if not match_pass:
            msg="Old Password Is Incorrect"
            return render(request,'Researcher_templates/researcher_change_password.html',{'msg':msg})
        elif same_pass:
            msg="Please Enter Different Password"
            return render(request,'Researcher_templates/researcher_change_password.html',{'msg':msg})
        elif v_new_pass==v_new_confirm_pass:
            user.Password = make_password(v_new_pass) 
            user.save()
            return redirect('logout')
        else:
            msg="New Password And Confirm Password Is Not Matched"
            return render(request,'Researcher_templates/researcher_change_password.html',{'msg':msg})

    else:
        return render(request,'Researcher_templates/researcher_change_password.html')

    

def researcher_index(request):
    return render(request,'Researcher_templates/researcher_index.html')

def researcher_home(request):
    notice = Notice.objects.all().order_by("-id")
    return render(request,'Researcher_templates/researcher_index.html', {'notice': notice})

# def researcher_feedback(request):
#     feeds = FeedBack.objects.all().order_by("-Feedback_Date")
#     theme = Theme.objects.all()
    
#     try:
#        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
#        researcher_user= Researcher.objects.get(Res_user=user)
#        if user:
#            if request.method=="POST":
#                vtheme=request.POST['ltheme']
#                vfeedback=request.POST['lfeedback']
#                request.session['image']=researcher_user.Image.url
#                new_feed=FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
#                return render(request,'Researcher_templates/researcher_feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#            else:
#                 return render(request,'Researcher_templates/researcher_feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#     except:
#         return render(request,'Researcher_templates/researcher_feedback.html',{'feeds':feeds})

def researcher_feedback_page(request):
    load_feeds()
    return render(request,'Researcher_templates/researcher_feedback.html', app_data)

def researcher_feedback(request):
    if request.method=="POST":
        vtheme=request.POST['ltheme']
        vfeedback=request.POST['lfeedback']
        #request.session['image']=p_user.Image.url
        try:
            print("1")
            user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
            app_data['user'] = user
            r_user=Researcher.objects.get(Res_user=user)
            FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
            return redirect(researcher_feedback_page)
        except:
            print("2")
            app_data['msg'] = ''
            return redirect(researcher_feedback_page)
    else:
        return redirect(researcher_feedback_page)



def researcher_about(request):
    return render(request,'Researcher_templates/researcher_about.html')

def researcher_gallery(request):
    return render(request,'Researcher_templates/researcher_gallery.html')

def researcher_contact(request):
    return render(request,'Researcher_templates/researcher_contact.html')

def researcher_pricing(request):
    RegCat = RegCategory.objects.all()
    return render(request,'Researcher_templates/researcher_pricing.html',{'RegCat':RegCat})

def researcher_speaker(request):
    winners = Winners.objects.all().order_by("-id")
    return render(request,'Researcher_templates/researcher_speaker.html',{'winners':winners})


def res_shedule_detail(request,pk):
    theme = Theme.objects.all()
    theme_pk = Theme.objects.get(pk=pk)
    print(theme_pk)
    sub_theme=theme_pk.Sub_themes

    try:
        conf = Conference.objects.get(Conference_Theme=theme_pk)
        print(conf)
        return render(request,'Researcher_templates/researcher_schedule.html',{'theme':theme,'sub':sub_theme,'conf':conf})
    except:
        theme1=theme_pk.Theme_name
        return render(request,'Researcher_templates/researcher_schedule.html',{'theme':theme,'sub':sub_theme,'theme1':theme1})

def researcher_schedule(request):
    theme = Theme.objects.all()
    return render(request,'Researcher_templates/researcher_schedule.html',{'theme':theme})

def researcher_registration(request):
    try:
        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
        cate = RegCategory.objects.all()
        p_user=Researcher.objects.get(Res_user=user)
        conf=Conference.objects.all()
        now = datetime.datetime.now()
        print(now.date())
        today=now.date()
        if user:
            return render(request,'Researcher_templates/researcher_registration.html',{'user':user,'p_user':p_user,'category':cate,'conf':conf,'today':today})
    except:
        return render(request,'Researcher_templates/researcher_registration.html')

def res_reg_next(request):
    user = User.objects.get(Email=request.session['email'],Role=request.session['role'])
    user1= Researcher.objects.get(Res_user=user)
    cate = RegCategory.objects.all()
    
    vtheme=request.POST['theme']
    vIn_name=request.POST['In_name']
    vIn_address=request.POST['In_address']
    vdesg=request.POST['desg']
    vrole=request.POST['srole'] 
    vauthor= request.POST['sauthor']

    vcat = RegCategory.objects.get(Category=vrole)
    vcat_amount=vcat.Amount
    vconf=Conference.objects.get(Conference_Theme=vtheme)
    new_reg=Researcher_registration.objects.create(Researcher_users=user1,Conference_Theme=vconf,Institute=vIn_name,Address=vIn_address,Category=vcat,Designation=vdesg,Total_amount=vcat_amount)
    
    print("crete user in researcher_registreation")
    if vauthor=="yes":
        return render(request,'Researcher_templates/co_author.html',{'category':cate,'user':user,'reg':new_reg})
    else:
        return render(request,'Researcher_templates/abstract_submit.html',{'reg':new_reg,'user':user})

    

def co_author(request):
    cate = RegCategory.objects.all()
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user= Researcher.objects.get(Res_user=user)
    
    if request.method=="POST":
        vtitle=request.POST['stitle']
        vfname=request.POST['sfname']
        vlname=request.POST['slname']
        vemail=request.POST['semail']
        vphone=request.POST['sphone']
        vIn_name=request.POST['sIn_name']
        vIn_address=request.POST['sIn_address']
        vdesg=request.POST['sdesg']
        vrole=request.POST['srole']
        vauthor= request.POST['sauthor']

        vcat = RegCategory.objects.get(Category=vrole) 
        vcat_amount=vcat.Amount     
        vregid=request.POST['regid']
        member_update=Researcher_registration.objects.get(Registraion_number=vregid,Researcher_users=researcher_user)
        coauthor=Co_author.objects.create(Registration_FK=member_update,Author=researcher_user,Title=vtitle,Firstname=vfname,Lastname=vlname,Email=vemail,Phone=vphone,Institute=vIn_name,Address=vIn_address,Designation=vdesg,Category=vcat)
        cnt=Co_author.objects.filter(Registration_FK=member_update)
        ca=''
        import re
        regex = r"[[/']]"
        for i in cnt:
            ca+=f"{i.Firstname} {i.Lastname},"
        
        cnt1=len(cnt)
        
        member_update.Total_amount+=int(vcat_amount)
        member_update.Members=cnt1
        member_update.co_authors=ca
        member_update.save()
        coauthor.Registration_FK=member_update
        coauthor.save()
    
        if vauthor=="yes":
            msg="CO Author Created Suceessfully"
            return render(request,'Researcher_templates/co_author.html',{'msg':msg,'category':cate,'user':user,'reg':member_update})
        else:
            return render(request,'Researcher_templates/abstract_submit.html',{'reg':member_update,'user':user})

    else:
        return render(request,'Researcher_templates/co_author.html',{'category':cate,'user':user})

def abstract_submit(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user=Researcher.objects.get(Res_user=user)
    if request.method=="POST":
        vid=request.POST['sid']
        vtitle=request.POST['stitle']
        vdesc=request.POST['sdesc']
        vfile = request.FILES['sfiles']
        vregid=request.POST['regid']
        regobj=Researcher_registration.objects.get(Registraion_number=vregid,Researcher_users=researcher_user)
        abs1=Abstract.objects.create(Registration_FK=regobj,Researcher_FK=researcher_user,PaperID=vid,Title=vtitle,Description=vdesc,File=vfile)
        return redirect(res_reg_details)
    else:
        return render(request,'Researcher_templates/abstract_submit.html',{'user':user})


def res_reg_details(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user=Researcher.objects.get(Res_user=user)
    abstract=Abstract.objects.filter(Researcher_FK=researcher_user).order_by("-id")
    return render(request,'Researcher_templates/resercher_reg_details.html',{'abs':abstract})


def fullpaper_submit(request,pk):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user=Researcher.objects.get(Res_user=user)
    abstract=Abstract.objects.get(pk=pk)
    no=abstract.Registration_FK.Registraion_number
    print("-----------------------")
    print(abstract)
    print(no)
    reg = Researcher_registration.objects.get(Registraion_number=no,Researcher_users=researcher_user)
    print(reg)
    if request.method == "POST":
        vid=request.POST['sid']
        vtitle=request.POST['stitle']
        vdesc=request.POST['sdesc']
        vfile = request.FILES['sfiles']
        #vregid=request.POST['regid']
        FP1=Fullpaper.objects.create(Registration_FK=reg,Researcher_FK=researcher_user,PaperID=vid,Title=vtitle,Description=vdesc,File=vfile)
        return redirect(res_fullpaper_list)
    else:    
        return render(request,'Researcher_templates/fullpaper_submit.html',{'user':user,'pk':pk})


def researcher_initiate_payment(request,pk):
    request.session['key']=pk
    regpk=request.session.get('key')
    
    print("regpk------------------------")
    print(regpk)

    if request.method == 'POST':
        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
        amount=request.POST['amount']
        print(amount)

        transaction = Transaction.objects.create(made_by=user, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(request.session["email"])),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/res_callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request,'Researcher_templates/researcher_redirect.html', context=paytm_params)
    else:
        return render(request,'Researcher_templates/researcher_registration.html')

def res_payment_success(request):
    
    regpk=request.session.get('key')
    print("regpk------------------------")
    print(regpk)
    registration1=Researcher_registration.objects.get(Registraion_number=regpk)
    print(registration1)
    print(registration1.Conference_Theme)
    print("theme---------")
    theme=registration1.Conference_Theme.Conference_Theme
    print(theme)
    conf=Conference.objects.get(Conference_Theme=theme)
    print(conf)

    email=registration1.Researcher_users.Res_user.Email
    name=registration1.Researcher_users.Res_user.Firstname+" "+registration1.Researcher_users.Res_user.Lastname
    print(email)
    
    registration1.Payment_Status=True

    if conf.Include_Breakfast==True:
        breakfast_coupon=ran_gen(5, "AEIOSUMA23")
        registration1.Breakfast_Coupon=breakfast_coupon

    if conf.Include_Tea_Coffee==True:
        tea_coupon=ran_gen(5, "AEIOSUMA23")
        registration1.Tea_Coupon=tea_coupon

    if conf.Include_Lunch==True:
        lunch_coupon=ran_gen(5, "AEIOSUMA23")
        registration1.Lunch_Coupon=lunch_coupon
    
    registration1.save()
    print("Payment status-------------")
    print(registration1.Payment_Status)

    email_Subject = "Conference Registration"
    res_sendmail(email_Subject,'Res_Registration_Email',email,{'name': name,'reg':registration1})

    del request.session['key']
    return redirect(res_reg_details)

@csrf_exempt
def res_callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
                is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            msg="Somthing went wrong.Your Payment is not done!"
            print(msg)
            return redirect(res_payment_success)
        return redirect(res_payment_success)


def researcher_callback(request):
    return render(request,'Researcher_templates/researcher_callback.html')

def researcher_redirect(request):
    return render(request,'Researcher_templates/researcher_redirect.html')

def res_abstract_list(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user=Researcher.objects.get(Res_user=user)
    abstract=Abstract.objects.filter(Researcher_FK=researcher_user)
    return render(request,'Researcher_templates/res_abstract_list.html',{'abstract':abstract})

def view_abs_review(request,pk):
    print(pk)
    abstract=Abstract.objects.get(pk=pk)
    review=Review_Abstract.objects.filter(Abstract=abstract)
    print(abstract)
    now = datetime.datetime.now()
    print(now.date())
    today=now.date()
    return render(request,'Researcher_templates/view_abs_review.html',{'abstract':abstract,'review':review,'today':today})

def res_fullpaper_list(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    researcher_user=Researcher.objects.get(Res_user=user)
    fullpaper=Fullpaper.objects.filter(Researcher_FK=researcher_user)
    return render(request,'Researcher_templates/res_fullpaper_list.html',{'FP':fullpaper})

def view_full_review(request,pk):
    print(pk)
    fullpaper=Fullpaper.objects.get(pk=pk)
    review=Review_Fullpaper.objects.filter(fullpaper=fullpaper)
    print(fullpaper)
    print(review)
    return render(request,'Researcher_templates/view_full_review.html',{'FP':review,'fullpaper':fullpaper})




#----------------------Reviewer views---------------------------------------

def reviewer_profile(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    reviewer_user= Reviewer.objects.get(Reviewer_user=user)
    if request.method=="POST":
        
        user.Firstname=request.POST['fname']
        user.Lastname=request.POST['lname']
        reviewer_user.Phone=request.POST['phone']
        reviewer_user.About=request.POST['about']
        reviewer_user.Address=request.POST['address']
        try:
            if request.FILES['pimage']:
                reviewer_user.Image=request.FILES['pimage']
                user.save()
                reviewer_user.save()
                del request.session['image']
                request.session['image']=reviewer_user.Image.url
                del request.session['name']
                request.session['name']=user.Firstname
                msg="Profile Updated Successfully."
                return render(request,"Reviewer_templates/reviewer_profile.html",{'user':user,'reviewer_user':reviewer_user,'msg':msg})
        except:
            user.save()
            reviewer_user.save()
            del request.session['name']
            request.session['name']=user.Firstname
            msg="Profile Updated Successfully."
            return render(request,"Reviewer_templates/reviewer_profile.html",{'user':user,'reviewer_user':reviewer_user,'msg':msg})
    else:
        return render(request,"Reviewer_templates/reviewer_profile.html",{'user':user,'reviewer_user':reviewer_user})

def reviewer_change_password(request):
    user = User.objects.get(Email=request.session['email'],Role=request.session['role'])

    if request.method=="POST":
        v_old_pass=request.POST['l_old_pass']
        v_new_pass=request.POST['l_new_pass']
        v_new_confirm_pass=request.POST['l_new_confirm_pass']
         
        password=user.Password
        print("---->",password)
        match_pass=check_password(v_old_pass,password)
        print(match_pass)
        same_pass=check_password(v_new_pass,password)
        print(same_pass)

        if not match_pass:
            msg="Old Password Is Incorrect"
            return render(request,'Reviewer_templates/reviewer_change_password.html',{'msg':msg})
        elif same_pass:
            msg="Please Enter Different Password"
            return render(request,'Reviewer_templates/reviewer_change_password.html',{'msg':msg})
        elif v_new_pass==v_new_confirm_pass:
            user.Password = make_password(v_new_pass) 
            user.save()
            return redirect('logout')
        else:
            msg="New Password And Confirm Password Is Not Matched"
            return render(request,'Reviewer_templates/reviewer_change_password.html',{'msg':msg})
        
    else:
        return render(request,'Reviewer_templates/reviewer_change_password.html')



def reviewer_index(request):
    return render(request,'Reviewer_templates/reviewer_index.html')

def reviewer_home(request):
    notice = Notice.objects.all().order_by("-id")
    return render(request,'Reviewer_templates/reviewer_index.html', {'notice': notice})

# def reviewer_feedback(request):
#     feeds = FeedBack.objects.all().order_by("-Feedback_Date")
#     theme = Theme.objects.all()
    
#     try:
#        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
#        reviewer_user= Reviewer.objects.get(Reviewer_user=user)
#        if user:
#            if request.method=="POST":
#                vtheme=request.POST['ltheme']
#                vfeedback=request.POST['lfeedback']
#                request.session['image']=reviewer_user.Image.url
#                new_feed=FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
#                return render(request,'Reviewer_templates/reviewer_feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#            else:
#                 return render(request,'Reviewer_templates/reviewer_feedback.html',{'feeds':feeds,'user':user,'theme':theme})
#     except:
#         return render(request,'Reviewer_templates/reviewer_feedback.html',{'feeds':feeds})


def reviewer_feedback_page(request):
    load_feeds()
    return render(request,'Reviewer_templates/reviewer_feedback.html', app_data)

def reviewer_feedback(request):
    if request.method=="POST":
        vtheme=request.POST['ltheme']
        vfeedback=request.POST['lfeedback']
        #request.session['image']=p_user.Image.url
        try:
            print("1")
            user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
            app_data['user'] = user
            rev_user=Reviewer.objects.get(Reviewer_user=user)
            FeedBack.objects.create(Feedback_user=user,Feedback_Theme=vtheme,Feedback_Description=vfeedback)
            return redirect(reviewer_feedback_page)
        except:
            print("2")
            app_data['msg'] = ''
            return redirect(reviewer_feedback_page)
    else:
        return redirect(reviewer_feedback_page)



def reviewer_about(request):
    return render(request,'Reviewer_templates/reviewer_about.html')

def reviewer_gallery(request):
    return render(request,'Reviewer_templates/reviewer_gallery.html')

def reviewer_contact(request):
    return render(request,'Reviewer_templates/reviewer_contact.html')

def reviewer_pricing(request):
    RegCat = RegCategory.objects.all()
    return render(request,'Reviewer_templates/reviewer_pricing.html',{'RegCat':RegCat})

def reviewer_speaker(request):
    winners = Winners.objects.all().order_by("-id")
    return render(request,'Reviewer_templates/reviewer_speaker.html',{'winners':winners})

def rev_shedule_detail(request,pk):
    theme = Theme.objects.all()
    theme_pk = Theme.objects.get(pk=pk)
    print(theme_pk)
    sub_theme=theme_pk.Sub_themes

    try:
        conf = Conference.objects.get(Conference_Theme=theme_pk)
        print(conf)
        return render(request,'Reviewer_templates/reviewer_schedule.html',{'theme':theme,'sub':sub_theme,'conf':conf})
    except:
        theme1=theme_pk.Theme_name
        return render(request,'Reviewer_templates/reviewer_schedule.html',{'theme':theme,'sub':sub_theme,'theme1':theme1})

def reviewer_schedule(request):
    theme = Theme.objects.all()
    return render(request,'Reviewer_templates/reviewer_schedule.html',{'theme': theme})

def rev_abstract_list(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    reviewer_user= Reviewer.objects.get(Reviewer_user=user) 
    abstracts=Review_Abstract.objects.filter(Reviewer=reviewer_user)
    return render(request,'Reviewer_templates/rev_abstract_list.html',{'abstracts':abstracts})

def rev_fullpaper_list(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    reviewer_user= Reviewer.objects.get(Reviewer_user=user) 
    fullpaper=Review_Fullpaper.objects.filter(Reviewer=reviewer_user)
    return render(request,'Reviewer_templates/rev_fullpaper_list.html',{'fullpaper':fullpaper})

def add_abs_review(request,pk):
    print(pk)
    abstract=Review_Abstract.objects.get(pk=pk)
    print(abstract)
    return render(request,'Reviewer_templates/add_abs_review.html',{'pk':pk,'abstract':abstract})

def add_fullpaper_rev(request,pk):
    print(pk)
    fullpaper=Review_Fullpaper.objects.get(pk=pk)
    print(fullpaper)
    return render(request,'Reviewer_templates/add_fullpaper_rev.html',{'pk':pk,'fullpaper':fullpaper})

def save_abs_review(request):
    if request.method=='POST':
        vpk=request.POST['spk']
        vdesc=request.POST['sdesc']
        veval=request.POST['seval']
        abstract=Review_Abstract.objects.get(pk=vpk)   
        abstract.Evaluation=veval
        abstract.Reviews=vdesc
        abstract.save()
        return redirect(rev_abstract_list)
    else:
        return redirect(rev_abstract_list)

def save_fullpaper_rev(request):
    if request.method=='POST':
        vpk=request.POST['spk']
        vdesc=request.POST['sdesc']
        veval=request.POST['seval']
        fullpaper=Review_Fullpaper.objects.get(pk=vpk)   
        fullpaper.Evaluation=veval
        fullpaper.Reviews=vdesc
        fullpaper.save()
        return redirect(rev_fullpaper_list)
    else:
        return redirect(rev_fullpaper_list)




#-------------------------------------Participant Registration----------------------------------------#


def participant_registraion(request):
    try:
        user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
        cate=RegCategory.objects.all()
        p_user=Participant.objects.get(Parti_user=user)
        conf=Conference.objects.all()
        now = datetime.datetime.now()
        print(now.date())
        today=now.date()
        if user:
            return render(request,'participant_registraion.html',{'user':user,'p_user':p_user,'category':cate,'conf':conf,'today':today})
    except:
        now = datetime.datetime.now()
        print(now)
        return render(request,'participant_registraion.html')

def reg_next(request):
    if request.method=='POST':
        user = User.objects.get(Email=request.session['email'],Role=request.session['role'])
        cate = RegCategory.objects.all()
        user1 = Participant.objects.get(Parti_user=user)
        vtheme=request.POST['theme']
        vIn_name=request.POST['In_name']
        vIn_address=request.POST['In_address']
        vdesg=request.POST['desg']
        vrole=request.POST['srole']  
        vamount=request.POST['samount']
        vcat = RegCategory.objects.get(Category=vrole)
        vconf = Conference.objects.get(Conference_Theme=vtheme)
        new_reg=Participant_registration.objects.create(Participant_users=user1,Conference_Theme=vconf,Institute=vIn_name,Address=vIn_address,Category=vcat,Designation=vdesg,Amount=vamount)
        return redirect(reg_details)
    else:
        return render(request,'participant_registraion.html')

def reg_details(request):
    user=User.objects.get(Email=request.session['email'],Role=request.session['role'])
    user1=Participant.objects.get(Parti_user=user)
    regobj=Participant_registration.objects.filter(Participant_users=user1).order_by("-id")
    speaker=Fullpaper.objects.all()
    return render(request,'participant_reg_details.html',{'reg':regobj,'speaker':speaker})

def initiate_payment(request,pk):
    if request.method == 'POST':

        user = User.objects.get(Email=request.session['email'],Role=request.session['role'])
        amount=request.POST['amount']
        print(amount)
        request.session['key']=pk
        regpk=request.session.get('key')
    
        print("regpk------------------------")
        print(regpk)
        transaction = Transaction.objects.create(made_by=user, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(request.session["email"])),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request,'participant_redirect.html', context=paytm_params)
    else:
        return render(request,'participant_registraion.html')

def participant_callback(request):
    return render(request,'participant_callback.html')

def participant_redirect(request):
    return render(request,'participant_redirect.html')


def reg_email(request):
    return render(request,'Registration_Email.html')
    
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
                is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            msg="Somthing went wrong.Your Payment is not done!"
            print(msg)
            return redirect(payment_success)
        return redirect(payment_success)

# defining function for random
# string id with parameter
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
  
# function call for random string
# generation with size 8 and string 
#print (ran_gen(5, "AEIOSUMA23"))

def payment_success(request):
    
    regpk=request.session.get('key')
    
    print("regpk------------------------")
    print(regpk)
    
    registration=Participant_registration.objects.get(id=regpk)
    theme=registration.Conference_Theme.Conference_Theme
    print(theme)
    conf=Conference.objects.get(Conference_Theme=theme)
    print(conf)


    email=registration.Participant_users.Parti_user.Email
    name=registration.Participant_users.Parti_user.Firstname+" "+registration.Participant_users.Parti_user.Lastname
    print(email)
    registration.Payment_status=True

    if conf.Include_Breakfast==True:
        breakfast_coupon=ran_gen(5, "AEIOSUMA23")
        registration.Breakfast_Coupon=breakfast_coupon


    if conf.Include_Tea_Coffee==True:
        tea_coupon=ran_gen(5, "AEIOSUMA23")
        registration.Tea_Coupon=tea_coupon

    if conf.Include_Lunch==True:
        lunch_coupon=ran_gen(5, "AEIOSUMA23")
        registration.Lunch_Coupon=lunch_coupon
    
    registration.save()
    speaker=Fullpaper.objects.all()
    print("Payment status-------------")
    print(registration.Payment_status)
    print(registration.Breakfast_Coupon)
    email_Subject = "Conference Registration"
    sendmail(email_Subject,'Registration_Email',email,{'name': name,'reg':registration,'speaker':speaker})

    del request.session['key']
    return redirect(reg_details)



