
from django.shortcuts import render, redirect,get_object_or_404
from .models import User, AidRequest,  Feedback,  VolunteerAssignment

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
# 30sept
from .forms import LanguageForm
from .models import Notification
from .forms import DonationForm
from .models import Donation
import datetime
from .forms import AidRequestForm
from .models import LiveUpdate



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
    return render(request, "core/donation_list.html", {"donations": donations})


# ==== FEEDBACK ====
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, "core/feedback_list.html", {"feedbacks": feedbacks})


# ==== NOTIFICATION ====
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def notification_list(request):
    user = request.user
    if user.role == "admin":
        notifications = Notification.objects.all().order_by('-timestamp')
    else:
        notifications = Notification.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'core/notification_list.html', {'notifications': notifications})



@login_required
@user_passes_test(is_admin)
def add_notification(request):
    if request.method == "POST":
        message = request.POST.get("message")
        notif_type = request.POST.get("type")


        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.exclude(role="admin")
        for u in users:
            Notification.objects.create(user=u, message=message, type=notif_type)

        return redirect("notification_list")
    return render(request, "core/add_notification.html")


@login_required
@user_passes_test(is_admin)
def delete_notification(request, notif_id):
    notif = get_object_or_404(Notification, notification_id=notif_id)
    notif.delete()
    return redirect("notification_list")


@login_required
def mark_as_read(request, notification_id):
    n = get_object_or_404(Notification, notification_id=notification_id, user=request.user)
    n.status = 'read'
    n.save()
    return redirect('notification_list')

@login_required
def approve_notification(request, notification_id):
    if request.user.role != "admin":
        return redirect('notification_list')
    n = get_object_or_404(Notification, notification_id=notification_id)
    n.action_status = 'approved'
    n.status = 'read'
    n.save()

    # Send feedback notification to user
    Notification.objects.create(
        user=n.user,
        type=n.type,
        message=f"Your {n.type.lower()} has been approved by admin.",
        status='unread'
    )
    return redirect('notification_list')


@login_required
def deny_notification(request, notification_id):
    if request.user.role != "admin":
        return redirect('notification_list')
    n = get_object_or_404(Notification, notification_id=notification_id)
    n.action_status = 'denied'
    n.status = 'read'
    n.save()

    Notification.objects.create(
        user=n.user,
        type=n.type,
        message=f"Your {n.type.lower()} has been denied by admin.",
        status='unread'
    )
    return redirect('notification_list')



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
                return redirect("user_profile")
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
# 30sept

@login_required
def user_profile(request):
    user = request.user

    if request.method == "POST":
        # Update editable fields only
        user.name = request.POST.get("name", user.name)
        user.phone_number = request.POST.get("phone_number", user.phone_number)
        user.language_preference = request.POST.get("language_preference", user.language_preference)

        user.save()  # Save changes to DB
        messages.success(request, "Profile updated successfully!")
        return redirect("user_profile")  # Refresh the page

    return render(request, "core/user_profile.html", {"user": user})


def change_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Language updated successfully!")
            return redirect('user_profile')
    else:
        form = LanguageForm(instance=request.user)

    return render(request, "core/change_language.html", {"form": form})

@login_required
def dashboard(request):
    user = request.user

    if user.role == "admin":
        template = "core/dashboard_admin.html"
    elif user.role == "donor":
        template = "core/dashboard_donor.html"
    elif user.role == "volunteer":
        template = "core/dashboard_volunteer.html"
        assigned_requests = AidRequest.objects.filter(assigned_volunteer=user)
        context = {"user": user, "assigned_requests": assigned_requests}
        return render(request, template, context)
    elif user.role == "victim":
        template = "core/dashboard_victim.html"
    else:
        template = "core/dashboard_default.html"

    return render(request, template, {"user": user})



@login_required
def make_donation(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user

            # Auto-generate receipt number like "DR-YYYYMMDD-XXXX"
            today = datetime.date.today().strftime("%Y%m%d")
            donation.receipt_number = f"DR-{today}-{Donation.objects.count()+1:04d}"

            donation.save()
            # ✅ Notify Admin automatically
            admin_user = User.objects.filter(role="admin").first()
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    type='Donation',
                    message=f"New donation submitted by {request.user.username} for review.",
                    status='unread'
                )

            messages.success(request, "Donation submitted successfully!")
            return redirect('donation_history')
    else:
        form = DonationForm()

    return render(request, "core/donation.html", {"form": form})

@login_required
def donation_history(request):
    donations = Donation.objects.filter(donor=request.user).order_by("-created_at")
    return render(request, "core/history.html", {"donations": donations})

@login_required
def request_aid(request):
    if request.method == "POST":
        form = AidRequestForm(request.POST, request.FILES)
        if form.is_valid():
            aid_request = form.save(commit=False)
            aid_request.user = request.user
            aid_request.save()

            # ✅ Automatically notify Admin
            admin_user = User.objects.filter(role="admin").first()
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    type='Aid Request',
                    message=f"New aid request submitted by {request.user.name} for review.",
                    status='unread'
                )

            messages.success(request, f"Your request has been submitted! Request ID: {aid_request.request_id}")
            return redirect("my_requests")
    else:
        form = AidRequestForm()
    return render(request, "core/request_aid.html", {"form": form})

@login_required
def my_requests(request):
    requests = AidRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "core/my_requests.html", {"requests": requests})


def live_updates(request):
    category = request.GET.get("category")
    location = request.GET.get("location")
    date = request.GET.get("date")

    updates = LiveUpdate.objects.all()

    if category and category != "All":
        updates = updates.filter(category=category)
    if location and location != "All":
        updates = updates.filter(location__icontains=location)
    if date:
        updates = updates.filter(created_at__date=date)

    return render(request, "core/live_updates.html", {"updates": updates})



def privacy_policy(request):
    return render(request, "core/privacy.html")

def terms_of_service(request):
    return render(request, "core/terms.html")


@login_required
def assigned_requests(request):
    if request.user.role != "volunteer":
        return redirect('home')

    requests = AidRequest.objects.filter(assigned_volunteer=request.user)
    return render(request, 'core/volunteer_assigned_requests.html', {'requests': requests})


@login_required
def update_request_status(request, pk):
    req = get_object_or_404(AidRequest, pk=pk, assigned_volunteer=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        req.status = new_status
        req.save()
        messages.success(request, "Status updated successfully!")
        return redirect('assigned_requests')

    return render(request, 'core/update_request_status.html', {'req': req})

@login_required
def help_page(request):
    user = request.user
    role = user.role if hasattr(user, "role") else "guest"

    return render(request, "core/user_help.html", {"role": role})