from django.contrib import admin
from . models import *

class userAdmin(admin.ModelAdmin):
    list_display=('Firstname','Lastname','Role',)
    list_filter=('Role',)
    list_per_page=4
    search_fields=('Firstname','Lastname','Role',)

class ResearcherAdmin(admin.ModelAdmin):
    list_display=('Res_user',)
    list_per_page=4
    search_fields=('Res_user__Firstname',)

class ReviewerAdmin(admin.ModelAdmin):
    list_display=('Reviewer_user',)
    list_per_page=4
    search_fields=('Reviewer_user__Firstname',)


class ParticipantAdmin(admin.ModelAdmin):
    list_display=('Parti_user',)
    list_per_page=4
    search_fields=('Parti_user__Firstname',)


class NoticeAdmin(admin.ModelAdmin):
    list_display=('Date','Title',)
    list_filter=('Date','Title',)
    list_per_page=4
    search_fields=('Title',)


class ConferenceAdmin(admin.ModelAdmin):
    list_display=('Date','Conference_Theme','Conference_Mode',)
    list_filter=('Date','Conference_Theme',)
    list_per_page=4
    search_fields=('Conference_Theme__Theme_name',)


class FeedBackAdmin(admin.ModelAdmin):
    list_display=('Feedback_Date','Feedback_user','Feedback_Theme',)
    list_filter=('Feedback_user','Feedback_Theme',)
    list_per_page=4
    search_fields=('Feedback_Theme',)


class RegCategoryAdmin(admin.ModelAdmin):
    list_display=('Category','Amount',)
    list_filter=('Category',)
    list_per_page=4
    search_fields=('Category',)

    
class Participant_registration_Admin(admin.ModelAdmin):
    list_display=('Date','Participant_users','Conference_Theme',)
    list_filter=('Date','Participant_users','Conference_Theme',)
    list_per_page=4
    #search_fields=('Participant_users','Conference_Theme',)


class Researcher_registration_Admin(admin.ModelAdmin):
    list_display=('Date','Researcher_users','Conference_Theme',)
    list_filter=('Date','Researcher_users','Conference_Theme',)
    list_per_page=4
    #search_fields=('Researcher_users','Conference_Theme',)


class AbstractAdmin(admin.ModelAdmin):
    list_display=('Date','PaperID','Title','Status',)
    list_filter=('Date','Status',)
    list_per_page=4
    search_fields=('PaperID','Title','Status',)


class FullpaperAdmin(admin.ModelAdmin):
    list_display=('Date','PaperID','Title','Status',)
    list_filter=('Date','Status',)
    list_per_page=4
    search_fields=('PaperID','Title','Status',)


class Review_Abstract_Admin(admin.ModelAdmin):
    list_display=('Date','Abstract','Reviewer','Evaluation',)
    list_filter=('Date','Reviewer','Evaluation','Abstract',)
    list_per_page=4
    search_fields=('Abstract__Title','Evaluation',)


class Review_Fullpaper_Admin(admin.ModelAdmin):
    list_display=('Date','fullpaper','Reviewer','Evaluation',)
    list_filter=('Date','Reviewer','Evaluation','fullpaper',)
    list_per_page=4
    search_fields=('fullpaper__Title','Evaluation',)



admin.site.register(User,userAdmin)
admin.site.register(Researcher,ResearcherAdmin)
admin.site.register(Reviewer,ReviewerAdmin)
admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Notice,NoticeAdmin)
admin.site.register(Theme)
admin.site.register(Conference,ConferenceAdmin)
admin.site.register(FeedBack,FeedBackAdmin)
admin.site.register(Participant_registration,Participant_registration_Admin)
#admin.site.register(Transaction)
admin.site.register(RegCategory,RegCategoryAdmin)
admin.site.register(Researcher_registration,Researcher_registration_Admin)
admin.site.register(Co_author)
admin.site.register(Abstract,AbstractAdmin)
admin.site.register(Review_Abstract,Review_Abstract_Admin)
admin.site.register(Fullpaper,FullpaperAdmin)
admin.site.register(Review_Fullpaper,Review_Fullpaper_Admin)
admin.site.register(Winners)

