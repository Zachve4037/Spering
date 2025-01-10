from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import PermissionDenied

from .models import Profile
from .models import Post, Comment, Genre

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Genre)

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and 'profile' in form.changed_data:
            profile = form.cleaned_data['profile']
            if profile.role =='admin':
                raise PermissionDenied("Only superadmins can assign the admin role!")
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)