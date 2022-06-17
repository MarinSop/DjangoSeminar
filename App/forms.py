from django.forms import ModelForm,Form
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from App.models import korisnici, predmeti, upisi
# from .models import Karta, Projekcija
# from django.contrib.admin.widgets import AdminTimeWidget

# class KartaForm(ModelForm):
#     class Meta:
#         model = Karta
#         fields = ['projekcija','seatNumber']


# class NovaProjekcijaForm(forms.Form):
#     imeFilma = forms.CharField(label='Ime filma', max_length=100)
#     vrijemeFilma = forms.TimeField(label='Vrijeme filma',widget=AdminTimeWidget(format='%H:%M'))
#     brojSjedala = forms.IntegerField(label='Broj sjedala')



# class AzurirajProjekcijuForm(forms.Form):
#     test = forms.IntegerField()
#     projekcije = forms.ChoiceField(choices=Projekcija.objects.all())

class DodajNoviPredmet(ModelForm):
    class Meta:
        model = predmeti
        fields = ['name','kod','program','ects','sem_red','sem_izv','izborni']

class DodajPredmetProfesor(Form):
    korisnik_id = forms.ModelChoiceField(queryset=korisnici.objects.all().filter(role='men'))
    predmet_id = forms.ModelChoiceField(queryset=predmeti.objects.all())
    status = forms.CharField(max_length=64)

class DodajNovogStudenta(UserCreationForm):
    class Meta:
        model = korisnici
        fields = UserCreationForm.Meta.fields + ('status',)

    def save(self, commit=True):
        user = super(DodajNovogStudenta, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        role = 'stu'
        status = self.cleaned_data["status"]
        user.role = role
        user.status = status
        if commit:
            user.save()
        return user

class DodajNovogProfesora(UserCreationForm):
    class Meta:
        model = korisnici
        fields = UserCreationForm.Meta.fields + ('status',)

    def save(self, commit=True):
        user = super(DodajNovogStudenta, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        role = 'men'
        status = self.cleaned_data["status"]
        user.role = role
        user.status = status
        if commit:
            user.save()
        return user

class PromjeniKorisnikForm(ModelForm):
    class Meta:
        model = korisnici
        fields = ['username','password','role','status']