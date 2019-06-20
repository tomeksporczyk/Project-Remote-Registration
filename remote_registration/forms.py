from django import forms

from remote_registration.models import *

PROVINCES = (
    ('dolnośląskie', 'dolnośląskie'),
    ('kujawsko-pomorskie', 'kujawsko-pomorskie'),
    ('lubelskie', 'lubelskie'),
    ('lubuskie', 'lubuskie'),
    ('łódzkie', 'łódzkie'),
    ('małopolskie', 'małopolskie'),
    ('małopolskie', 'dolnośląskie'),
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
        widgets = {'province': forms.Select(choices=PROVINCES)}


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


class LoginForm(forms.Form):
    user_login = forms.CharField(max_length=64, label='login')
    user_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='hasło')

