from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LightSaltUser, LightSaltPastor
from .forms import UserCreationForm, UserChangeForm, LightSaltPastorCreationForm, LightSaltPastorChangeForm




###########################
### 사용자 정보 관리자 페이지

class LightSaltUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("member_id", "name", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    serach_fields = ("member_id", "name", "email")
    ordering = ("member_id",)
    filter_horizontal = ("groups", "user_permissions",)
    fieldsets = (
        (None, {"fields" : ("member_id", "name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('member_id', 'name', 'email', 'password1', 'password2'),
        }),
    )

###########################
### 목사 정보 관리자 페이지

class LightSaltPastorAdmin(admin.ModelAdmin):
    add_form = LightSaltPastorCreationForm
    form = LightSaltPastorChangeForm

    list_display = ("pastor_id", "church_name", "church_post", "church_address", "authentication_yn")
    serach_fields = ("pastor_id", "church_name", "authentication_yn")
    ordering = ("pastor_id",)
    fieldsets = (
        (None, {"fields" : ("pastor_id", "church_name", "church_post", "church_address")}),       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('pastor_id', 'church_name', 'church_post', 'church_address', 'authentication_yn'),
        }),
    )

admin.site.register(LightSaltUser, LightSaltUserAdmin)
admin.site.register(LightSaltPastor, LightSaltPastorAdmin)
