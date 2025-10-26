
from django.urls import path
from . import views

urlpatterns = [

   path('', views.home, name='home'),
    # User
    path("users/", views.user_list, name="user_list"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),

    # AidRequest
    path("aidrequests/", views.aidrequest_list, name="aidrequest_list"),

    # Donation
    path("donations/", views.donation_list, name="donation_list"),

    # Feedback
    path("feedbacks/", views.feedback_list, name="feedback_list"),

    # Notification
    path("notifications/", views.notification_list, name="notification_list"),
    path("notifications/add/", views.add_notification, name="add_notification"),
    path("notifications/delete/<int:notif_id>/", views.delete_notification, name="delete_notification"),
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('notifications/<int:notification_id>/approve/', views.approve_notification, name='approve_notification'),
    path('notifications/<int:notification_id>/deny/', views.deny_notification, name='deny_notification'),

    # VolunteerAssignment
    path("assignments/", views.volunteerassignment_list, name="volunteerassignment_list"),


path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("donationinfo/", views.donationinfo, name="donationinfo"),


    path("about/", views.about_page, name="about"),
    path("contact/", views.contact_page, name="contact"),
    path("faq/", views.faq_page, name="faq"),

# 1oct
path("profile/", views.user_profile, name="user_profile"),
path('change-language/', views.change_language, name='change_language'),
path("dashboard/", views.dashboard, name="dashboard"),
path("donate/", views.make_donation, name="make_donation"),
    path("my-donations/", views.donation_history, name="donation_history"),
path("request-aid/", views.request_aid, name="request_aid"),
    path("my-requests/", views.my_requests, name="my_requests"),
    path("updates/", views.live_updates, name="live_updates"),
    path("privacy/", views.privacy_policy, name="privacy"),
    path("terms/", views.terms_of_service, name="terms"),

path('assigned-requests/', views.assigned_requests, name='assigned_requests'),
path('update-status/<int:pk>/', views.update_request_status, name='update_request_status'),

    path('help/', views.help_page, name='help_page'),
]