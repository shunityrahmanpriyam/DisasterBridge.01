from django.contrib import admin
from .models import User, AidRequest, Donation, Feedback, Notification, VolunteerAssignment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import LiveUpdate

# admin.site.register(User)
admin.site.register(AidRequest)
admin.site.register(Donation)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(VolunteerAssignment)


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "name", "phone_number", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone_number", "role", "language_preference")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "phone_number", "role", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email", "name", "phone_number")
    ordering = ("name",)

admin.site.register(User, UserAdmin)

@admin.register(LiveUpdate)
class LiveUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'volunteer_name', 'created_at')
    list_filter = ('category', 'location', 'created_at')
    search_fields = ('title', 'description', 'volunteer_name', 'location')
    ordering = ('-created_at',)


