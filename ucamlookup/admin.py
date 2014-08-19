from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    username = forms.RegexField(label="Username", max_length=30, regex=r'^[a-z][a-z0-9]{3,7}$', help_text="Required.",
                                error_messages={'invalid': "Invalid crsid format"})

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "A user with that username already exists.",
            code='duplicate_username',
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class LookupUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'is_staff', 'is_superuser')
    add_form = UserCreationForm
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )
    add_form_template = 'admin/auth/lookup_user/add_form.html'


admin.site.unregister(User)
admin.site.register(User, LookupUserAdmin)