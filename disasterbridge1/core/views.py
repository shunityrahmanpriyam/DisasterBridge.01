from django.shortcuts import render, get_object_or_404
from .models import User, AidRequest, Donation, Feedback, Notification, VolunteerAssignment

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from .forms import SignUpForm, LoginForm


def home(request):
    return render(request, 'core/home.html')

# ==== USER ====
def user_list(request):
    users = User.objects.all()
    return render(request, "core/user_list.html", {"users": users})


def user_detail(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    return render(request, "core/user_detail.html", {"user": user})


# ==== AID REQUEST ====
def aidrequest_list(request):
    requests = AidRequest.objects.all()
    return render(request, "core/aidrequest_list.html", {"requests": requests})


# ==== DONATION ====
def donation_list(request):
    donations = Donation.objects.all()
    return render(request, "core/donatenow.html", {"donations": donations})


# ==== FEEDBACK ====
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, "core/feedback_list.html", {"feedbacks": feedbacks})


# ==== NOTIFICATION ====
def notification_list(request):
    notifications = Notification.objects.all()
    return render(request, "core/notification_list.html", {"notifications": notifications})


# ==== VOLUNTEER ASSIGNMENT ====
def volunteerassignment_list(request):
    assignments = VolunteerAssignment.objects.all()
    return render(request, "core/assignment_list.html", {"assignments": assignments})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully! Please login.")
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                # Find user by email or phone
                user_obj = User.objects.get(Q(email=username) | Q(phone_number=username))
                user = authenticate(request, username=user_obj.email, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid login credentials")
    else:
        form = LoginForm()
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def donationinfo(request):
    return render(request, "core/donation_info.html")



def about_page(request):
    return render(request, "core/about.html")

def contact_page(request):
    return render(request, "core/contact.html")

def faq_page(request):
    return render(request, "core/faq.html")