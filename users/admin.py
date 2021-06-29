from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms
from .models import Division, District, Thana, Speciality, Schedule, Payment, VoterID, Treatment, Test, BMA, OTP, Days
User = get_user_model()
# Register your models here.



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ['sn']
    add_form = UserCreationForm
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'sn', 'verified', 'birthday', 'mobile', 'image', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'bg', 'gender', 'nid', 'bma', 'institute', 'pm_division', 'pm_district', 'pm_thana', 'ps_division', 'ps_district', 'ps_thana', 'ps_village', 'pm_village', 'user_type', 'payment', 'specialist', 'designation', 'password1', 'password2')}
        ),
    )
    ordering = ['-date_joined']
    exclude = ('username',)

UserAdmin.fieldsets += ('User Details', {'fields': ('sn', 'verified', 'birthday', 'mobile','image', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'bg', 'gender', 'nid', 'bma', 'institute', 'pm_division', 'pm_district', 'pm_thana', 'ps_division', 'ps_district', 'ps_thana', 'ps_village', 'pm_village', 'user_type', 'payment', 'specialist', 'designation',)}),

admin.site.register(User, UserAdmin)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Thana)
admin.site.register(Speciality)
admin.site.register(Schedule)
admin.site.register(Payment)
# admin.site.register(Transaction)
admin.site.register(VoterID)
admin.site.register(Treatment)
admin.site.register(Test)
admin.site.register(BMA)
admin.site.register(OTP)
admin.site.register(Days)

# admin.site.register(User)