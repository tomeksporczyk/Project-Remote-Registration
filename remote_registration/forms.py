from django import forms
from django.contrib.auth.forms import UserChangeForm

from remote_registration.models import *
from remote_registration.validators import *

PROVINCES = (
    ('dolnośląskie', 'dolnośląskie'),
    ('kujawsko-pomorskie', 'kujawsko-pomorskie'),
    ('lubelskie', 'lubelskie'),
    ('lubuskie', 'lubuskie'),
    ('łódzkie', 'łódzkie'),
    ('małopolskie', 'małopolskie'),
    ('mazowieckie', 'mazowieckie'),
    ('opolskie', 'opolskie'),
    ('podkarpackie', 'podkarpackie'),
    ('podlaskie', 'podlaskie'),
    ('pomorskie', 'pomorskie'),
    ('śląskie', 'śląskie'),
    ('świętokrzyskie', 'świętokrzyskie'),
    ('warmińsko-mazurskie', 'warmińsko-mazurskie'),
    ('wielkopolskie', 'wielkopolskie'),
    ('zachodniopomorskie', 'zachodniopomorskie')
)


class AddMedicalInstitutionForm(forms.ModelForm):
    class Meta:
        model = MedicalInstitution
        fields = '__all__'
        labels = {'ward': 'Oddział',
                  'name': 'Nazwa instytucji',
                  'city': 'Miasto',
                  'province': 'Województwo',
                  'address': "Adres"}


class UpdateMedicalInstitutionForm(forms.ModelForm):
    class Meta:
        model = MedicalInstitution
        fields = '__all__'
        labels = {'ward': 'Oddział',
                  'name': 'Nazwa instytucji',
                  'city': 'Miasto',
                  'province': 'Województwo',
                  'address': "Adres"}
        widgets = {'province': forms.Select(choices=PROVINCES)}


class AddProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = '__all__'
        labels = {'name': "Nazwa procedury",
                  'details': "Szczegóły procedury",
                  'duration': "Czas trwania (format: GG:MM:SS)",
                  'medical_institutions': "Placówka wykonawcza"}


class UpdateProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = '__all__'
        labels = {'name': "Nazwa procedury",
                  'details': "Szczegóły procedury",
                  'duration': "Czas trwania (format: GG:MM:SS)",
                  'medical_institutions': "Placówka wykonawcza"}


class AddPersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        labels = {'name': "Imię",
                  'surname': "Nazwisko",
                  'medical_institutions': "Placówka wykonawcza",
                  'procedures': "Procedury"}


class UpdatePersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        labels = {'name': "Imię",
                  'surname': "Nazwisko",
                  'medical_institutions': "Placówka wykonawcza",
                  'procedures': "Procedury"}


class CreateTimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        labels = {'day': 'Dzień tygodnia',
                  'personnel': 'Pracownik',
                  'medical_institution': 'Placówka',
                  'start': 'Czas rozpoczęcia pracy',
                  'end': 'Czas zakończenia pracy'}
        widgets = {'start': forms.TimeInput(),
                   'end': forms.TimeInput()}


class UpdateTimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['day', 'start', 'end']
        labels = {'day': 'Dzień tygodnia',
                  'start': 'Czas rozpoczęcia pracy',
                  'end': 'Czas zakończenia pracy'}
        widgets = {'start': forms.TimeInput(),
                   'end': forms.TimeInput()}


class AddReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = '__all__'
        labels = {'patient': 'Pacjent', 'procedure': 'Badanie'}


class LoginForm(forms.Form):
    user_login = forms.CharField(max_length=64, label='Login')
    user_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Hasło')


class AddUserForm(forms.Form):
    login = forms.CharField(max_length=150, validators=[is_user_unique], label='Login')
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, validators=[is_password_strong], label='Hasło')
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput, label='Powtórz hasło')
    name = forms.CharField(max_length=64, label='Imię')
    surname = forms.CharField(max_length=128, label='Nazwisko')
    email = forms.EmailField(label='Adres e-mail')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Hasła muszą być identyczne')


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Imię', 'last_name': 'Nazwisko', 'email': 'Adres e-mail'}


