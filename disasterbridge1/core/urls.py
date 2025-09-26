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

    # VolunteerAssignment
    path("assignments/", views.volunteerassignment_list, name="volunteerassignment_list"),


path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("donationinfo/", views.donationinfo, name="donationinfo"),


]
