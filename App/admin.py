from django.contrib import admin

from App.models import korisnici
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.


@admin.register(korisnici)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
