from django.urls import path,include
from . import views

urlpatterns = [
    #participant views
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('contact/',views.contact,name="contact"),
    path('gallery/',views.gallery,name="gallery"),
    path('pricing/',views.pricing,name="pricing"),
    path('shedule_detail/<int:pk>',views.shedule_detail,name="shedule_detail"),
    path('schedule/',views.schedule,name="schedule"),
    path('single_post/',views.single_post,name="single_post"),
    path('speakers/',views.speakers,name="speakers"),
    path('sponsors/',views.sponsors,name="sponsors"),
    path('profile/',views.profile,name="profile"),
    path('feedback/',views.feedback,name="feedback"),
    path('feedback_page/',views.feedback_page,name="feedback_page"),
    path('participant_registraion/',views.participant_registraion,name="participant_registraion"),
    path('reg_next/',views.reg_next,name='reg_next'),
    path('reg_details/',views.reg_details,name="reg_details"),
    path('reg_email/',views.reg_email,name="reg_email"),

    #paytm
    path('callback/',views.callback, name='callback'),
    path('initiate_payment/<int:pk>',views.initiate_payment,name="initiate_payment"),
    path('payment_success/',views.payment_success,name="payment_success"),
    path('participant_callback/',views.participant_callback,name="participant_callback"),
    path('participant_redirect/',views.participant_redirect,name="participant_redirect"),
    #path('return_participate_registration/',views.return_participate_registration,name="return_participate_registration"),

    #logout
    path('logout/',views.logout,name="logout"),
    
    #login
    path('login/',views.login,name="login"),
    path("showlogin/",views.showlogin,name="showlogin"),

    #forget_pw
    path("showemail/",views.showemail,name="showemail"),
    path("sendotp/",views.sendotp,name="sendotp"),
    path("otp_forget_pw",views.otp_forget_pw,name="otp_forget_pw"),
    path("forget_password/",views.forget_password,name="forget_password"),

    #signup
    path('signup/',views.signup,name="signup"),
    path('create_user',views.create_user,name="create_user"),
    path('otp/',views.otp,name="otp"),
    path('etemp/',views.etemp,name="etemp"),
    path('otp_var/',views.otp_var,name="otp_var"),

    #change_password
    path('change_password/',views.change_password,name='change_password'),

    #researcher views
    path('researcher_index/',views.researcher_index,name='researcher_index'),
    path('researcher_profile/',views.researcher_profile,name='researcher_profile'),
    path('researcher_change_password/',views.researcher_change_password,name='researcher_change_password'),
    path('researcher_home/',views.researcher_home,name='researcher_home'),
    path('researcher_feedback/',views.researcher_feedback,name='researcher_feedback'),
    path('researcher_feedback_page/',views.researcher_feedback_page,name='researcher_feedback_page'),
    path('researcher_about/',views.researcher_about,name='researcher_about'),
    path('researcher_contact/',views.researcher_contact,name='researcher_contact'),
    path('researcher_gallery/',views.researcher_gallery,name='researcher_gallery'),
    path('researcher_pricing/',views.researcher_pricing,name='researcher_pricing'),
    path('researcher_speaker/',views.researcher_speaker,name='researcher_speaker'),
    path('res_shedule_detail/<int:pk>',views.res_shedule_detail,name="res_shedule_detail"),
    path('researcher_schedule/',views.researcher_schedule,name='researcher_schedule'),
    path('researcher_registration/',views.researcher_registration,name='researcher_registration'),
    path('res_reg_next/',views.res_reg_next,name='res_reg_next'),
    path('co_author/',views.co_author,name='co_author'),
    path('res_reg_details/',views.res_reg_details,name='res_reg_details'),
    
    path('abstract_submit/',views.abstract_submit,name='abstract_submit'),
    path('res_abstract_list/',views.res_abstract_list,name='res_abstract_list'),
    path('view_abs_review/<int:pk>',views.view_abs_review,name='view_abs_review'),
    
    path('fullpaper_submit/<int:pk>',views.fullpaper_submit,name='fullpaper_submit'),
    path('view_full_review/<int:pk>',views.view_full_review,name='view_full_review'),
    path('res_fullpaper_list/',views.res_fullpaper_list,name='res_fullpaper_list'),
    
    #researcher_payment
    path('researcher_initiate_payment/<int:pk>',views.researcher_initiate_payment,name='researcher_initiate_payment'),
    path('res_callback/',views.res_callback, name='res_callback'),
    path('res_payment_success/',views.res_payment_success, name='res_payment_success'),
    path('researcher_callback/',views.researcher_callback,name="researcher_callback"),
    path('researcher_redirect/',views.researcher_redirect,name="researcher_redirect"),

    #reviewer views
    path('reviewer_index/',views.reviewer_index,name='reviewer_index'),
    path('reviewer_profile/',views.reviewer_profile,name='reviewer_profile'),
    path('reviewer_change_password/',views.reviewer_change_password,name='reviewer_change_password'),
    path('reviewer_home/',views.reviewer_home,name='reviewer_home'),
    path('reviewer_feedback/',views.reviewer_feedback,name='reviewer_feedback'),
    path('reviewer_feedback_page/',views.reviewer_feedback_page,name='reviewer_feedback_page'),
    path('reviewer_about/',views.reviewer_about,name='reviewer_about'),
    path('reviewer_contact/',views.reviewer_contact,name='reviewer_contact'),
    path('reviewer_gallery/',views.reviewer_gallery,name='reviewer_gallery'),
    path('reviewer_pricing/',views.reviewer_pricing,name='reviewer_pricing'),
    path('reviewer_speaker/',views.reviewer_speaker,name='reviewer_speaker'),
    path('rev_shedule_detail/<int:pk>',views.rev_shedule_detail,name="rev_shedule_detail"),
    path('reviewer_schedule/',views.reviewer_schedule,name='reviewer_schedule'),
    path('rev_abstract_list/',views.rev_abstract_list,name='rev_abstract_list'),
    path('rev_fullpaper_list/',views.rev_fullpaper_list,name='rev_fullpaper_list'),
    path('add_abs_review/<int:pk>',views.add_abs_review,name='add_abs_review'),
    path('save_abs_review/',views.save_abs_review,name='save_abs_review'),
    path('add_fullpaper_rev/<int:pk>/',views.add_fullpaper_rev,name='add_fullpaper_rev'),
    path('rev_fullpaper_list/',views.rev_fullpaper_list,name='rev_fullpaper_list'),
    path('save_fullpaper_rev/',views.save_fullpaper_rev,name='save_fullpaper_rev'),
]
