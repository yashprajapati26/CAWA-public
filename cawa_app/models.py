
from django.db import models
from django.utils import timezone
from django import forms
from django_mysql.models import ListTextField

# Create your models here.

class User(models.Model):
    Role=models.CharField(max_length=20,default="participant")
    Title=models.CharField(max_length=10,default="Mr.")
    Firstname=models.CharField(max_length=50)
    Lastname=models.CharField(max_length=50)
    Email=models.EmailField()
    Password=models.CharField(max_length=100)
    
    def __str__(self):
        return self.Firstname+" "+self.Lastname

class Researcher(models.Model):
    Res_user=models.ForeignKey(User,on_delete=models.CASCADE)
    Phone=models.BigIntegerField()
    Image=models.ImageField(upload_to='images/researcher/',default="avtar.png")
    About=models.CharField(max_length=50,default="",blank=True)
    Address=models.CharField(max_length=50,default="",blank=True)
  
    def __str__(self):
        return self.Res_user.Firstname+" "+self.Res_user.Lastname

class Reviewer(models.Model):
    Reviewer_user=models.ForeignKey(User,on_delete=models.CASCADE)
    Phone=models.BigIntegerField()
    Image=models.ImageField(upload_to='images/reviewer/',default="avtar.png")
    About=models.CharField(max_length=50,default="",blank=True)
    Address=models.CharField(max_length=50,default="",blank=True)
  
    def __str__(self):
        return self.Reviewer_user.Firstname+" "+self.Reviewer_user.Lastname

class Participant(models.Model):
    Parti_user=models.ForeignKey(User,on_delete=models.CASCADE)
    Phone=models.BigIntegerField()
    Image=models.ImageField(max_length=255,upload_to='images/participant/',default="avtar.png")
    About=models.CharField(max_length=50,default="",blank=True)
    Address=models.CharField(max_length=50,default="",blank=True)
  
    def __str__(self):
        return self.Parti_user.Firstname+" "+self.Parti_user.Lastname

class Notice(models.Model):
    Date=models.DateTimeField(auto_now_add=True)
    Title=models.CharField(max_length=50)
    Description=models.CharField(max_length=100)
    File=models.FileField(upload_to='files/',default="Abc.pdf")

    def __str__(self):
        return self.Title

Theme_Choice=(
        ("Strategic Management",'Strategic Management'),
        ("Accounting & Finance",'Accounting & Finance'),
        ("Marketing",'Marketing'),
        ("Human Resource Management",'Human Resource Management'),
        ("Enterpreneueship and Innovations",'Enterpreneueship and Innovations'),
        ("IT",'IT'),
    )
Conference_Choice=(
        ("Offline",'Offline'),
        ("Online",'Online'),
    )

class Theme(models.Model):
    Theme_name=models.CharField(max_length=100)
    Sub_themes=ListTextField(Theme_name)

    def __str__(self):
        return self.Theme_name

class Conference(models.Model):
    Conference_Theme=models.ForeignKey(Theme,on_delete=models.CASCADE)
    Conference_Mode=models.CharField(choices=Conference_Choice,max_length=100)
    Date=models.DateField()
    End_Date=models.DateField()
    Start_Time=models.TimeField()
    End_Time=models.TimeField()
    Place=models.CharField(max_length=100,blank=True)
    Online_Link=models.CharField(max_length=100,blank=True)
    Abstract_Submission_Date=models.DateField()
    Abstract_Acceptance_Date=models.DateField()
    FullPaper_Submission_Date=models.DateField()
    FullPaper_Acceptance_Date=models.DateField()
    Participant_registration_start_Date=models.DateField()
    Participant_registration_end_Date=models.DateField()
    Conference_Description=models.TextField()
    Include_Breakfast=models.BooleanField(default=False)
    Include_Tea_Coffee=models.BooleanField(default=False)
    Include_Lunch=models.BooleanField(default=False)


    def __str__(self):
        return self.Conference_Theme.Theme_name

class FeedBack(models.Model):
    Feedback_user=models.ForeignKey(User,on_delete=models.CASCADE)
    Feedback_Date=models.DateTimeField(auto_now_add=True)
    Feedback_Theme=models.CharField(choices=Theme_Choice,max_length=100)
    Feedback_Description=models.TextField(max_length=200)

    def __str__(self):
        return self.Feedback_user.Firstname + self.Feedback_user.Lastname

Category_choice=(
    ("Acedemician","Acedemician"),
    ("Industry","Industry"),
    ("Research Scholar","Research Scholar"),
    ("Student","Student"),
)

class RegCategory(models.Model):
    Category = models.CharField(max_length=20)
    Amount = models.CharField(max_length=20)

    def __str__(self):
        return self.Category

class Participant_registration(models.Model):
    Conference_Theme=models.ForeignKey(Conference,on_delete=models.CASCADE)
    Participant_users=models.ForeignKey(Participant,on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True)
    Institute=models.CharField(max_length=50)
    Address=models.TextField(max_length=150)
    Category=models.ForeignKey(RegCategory, on_delete=models.CASCADE)
    Designation=models.CharField(max_length=50)
    Amount=models.IntegerField()
    Payment_status=models.BooleanField(default=False)
    Breakfast_Coupon=models.CharField(max_length=20,blank=True)
    Tea_Coupon=models.CharField(max_length=20,blank=True)
    Lunch_Coupon=models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.Participant_users.Parti_user.Title + self.Participant_users.Parti_user.Firstname + self.Participant_users.Parti_user.Lastname


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.made_by.Email

class Researcher_registration(models.Model):
    Registraion_number=models.AutoField(primary_key=True)
    Date=models.DateField(auto_now_add=True)
    Conference_Theme=models.ForeignKey(Conference,on_delete=models.CASCADE)
    Researcher_users=models.ForeignKey(Researcher,on_delete=models.CASCADE)
    Institute=models.CharField(max_length=50)
    Address=models.TextField(max_length=150)
    Category=models.ForeignKey(RegCategory, on_delete=models.CASCADE)
    Designation=models.CharField(max_length=50)
    Members=models.CharField(max_length=10,blank=True)
    co_authors=models.CharField(max_length=100,blank=True)
    Total_amount=models.IntegerField()
    Payment_Status=models.BooleanField(default=False)
    Breakfast_Coupon=models.CharField(max_length=20,blank=True)
    Tea_Coupon=models.CharField(max_length=20,blank=True)
    Lunch_Coupon=models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.Conference_Theme.Conference_Theme.Theme_name

class Co_author(models.Model):
    Registration_FK=models.ForeignKey(Researcher_registration,on_delete=models.CASCADE)
    Author=models.ForeignKey(Researcher,on_delete=models.CASCADE)
    Title=models.CharField(max_length=10,default="Mr.")
    Firstname=models.CharField(max_length=50)
    Lastname=models.CharField(max_length=50)
    Email=models.EmailField()
    Phone=models.BigIntegerField()
    Institute=models.CharField(max_length=50)
    Address=models.TextField(max_length=150)
    Category=models.ForeignKey(RegCategory, on_delete=models.CASCADE)
    Designation=models.CharField(max_length=50)

    def __str__(self):
        return self.Title + self.Firstname + self.Lastname


status_choice=(
    ('pending','pending'),
    ('accepted','accepted'),
    ('rejected','rejected'),
)

class Abstract(models.Model):
    Registration_FK=models.ForeignKey(Researcher_registration,on_delete=models.CASCADE)
    Researcher_FK=models.ForeignKey(Researcher,on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True)
    PaperID=models.IntegerField()
    Title=models.CharField(max_length=100)
    Description=models.TextField()
    File=models.FileField(upload_to='files/')
    Status=models.CharField(choices=status_choice,max_length=100,default='pending')

    def __str__(self):
        return self.Title


class Fullpaper(models.Model):
    Registration_FK=models.ForeignKey(Researcher_registration,on_delete=models.CASCADE)
    Researcher_FK=models.ForeignKey(Researcher,on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True)
    PaperID=models.IntegerField()
    Title=models.CharField(max_length=100)
    Description=models.TextField()
    File=models.FileField(upload_to='files/')
    Status=models.CharField(choices=status_choice,max_length=100,default='pending')

    def __str__(self):
        return self.Title


class Review_Abstract(models.Model):
    Date=models.DateField(auto_now_add=True)
    Abstract=models.ForeignKey(Abstract,on_delete=models.CASCADE)
    Reviewer=models.ForeignKey(Reviewer,on_delete=models.CASCADE)
    Evaluation=models.CharField(max_length=100,blank=True)
    Reviews=models.TextField(blank=True)

    def __str__(self):
        return self.Abstract.Title

class Review_Fullpaper(models.Model):
    Date=models.DateField(auto_now_add=True)
    fullpaper=models.ForeignKey(Fullpaper,on_delete=models.CASCADE)
    Reviewer=models.ForeignKey(Reviewer,on_delete=models.CASCADE) 
    Evaluation=models.CharField(max_length=100,blank=True)
    Reviews=models.TextField(blank=True)

    def __str__(self):
        return self.fullpaper.Title


class Winners(models.Model):
    Date=models.DateField(auto_now_add=True)
    Full_Paper=models.ForeignKey(Fullpaper,on_delete=models.CASCADE)

    def __str__(self):
        return self.Full_Paper.Title
