from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from remote_registration.models import *


class AddReferralForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=User.objects.all(), label='Pacjent')
    procedure = forms.ModelChoiceField(queryset=ProcedureCategories.objects.all(), label='Badanie')
    details = forms.ModelChoiceField(queryset=Procedure.objects.all(), label='Szczegóły badania')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['details'].queryset = Procedure.objects.none()

        if 'procedure' in self.data:
            try:
                procedure_id = int(self.data.get('procedure'))
                self.fields['details'].queryset = Procedure.objects.filter(name__id=procedure_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class UpdateReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['procedure', 'details']
        labels = {'procedure': 'Badanie', 'details': 'Szczegóły'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['details'].queryset = Procedure.objects.none()

        if 'procedure' in self.data:
            try:
                procedure_id = int(self.data.get('procedure'))
                self.fields['details'].queryset = Procedure.objects.filter(name__id=procedure_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['details'].queryset = self.instance.procedure.procedure_set


class LoginForm(forms.Form):
    user_login = forms.CharField(max_length=64, label='E-mail')
    user_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Hasło')


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UpdateUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Imię', 'last_name': 'Nazwisko', 'email': 'Adres e-mail'}

#
# class AddUserForm(forms.Form):
#     login = forms.CharField(max_length=150, validators=[is_user_unique], label='Login')
#     password = forms.CharField(max_length=64, widget=forms.PasswordInput, validators=[is_password_strong], label='Hasło')
#     password2 = forms.CharField(max_length=64, widget=forms.PasswordInput, label='Powtórz hasło')
#     name = forms.CharField(max_length=64, label='Imię')
#     surname = forms.CharField(max_length=128, label='Nazwisko')
#     email = forms.EmailField(label='Adres e-mail')
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         password2 = cleaned_data.get('password2')
#         if password != password2:
#             raise ValidationError('Hasła muszą być identyczne')
#
# class AddMedicalInstitutionForm(forms.ModelForm):
#     class Meta:
#         model = MedicalInstitution
#         fields = '__all__'
#         labels = {'ward': 'Oddział',
#                   'name': 'Nazwa instytucji',
#                   'city': 'Miasto',
#                   'province': 'Województwo',
#                   'address': "Adres"}
#
#
# class UpdateMedicalInstitutionForm(forms.ModelForm):
#     class Meta:
#         model = MedicalInstitution
#         fields = '__all__'
#         labels = {'ward': 'Oddział',
#                   'name': 'Nazwa instytucji',
#                   'city': 'Miasto',
#                   'province': 'Województwo',
#                   'address': "Adres"}
#
#
# class AddProcedureCategoryForm(forms.ModelForm):
#     class Meta:
#         model = ProcedureCategories
#         fields = '__all__'
#         labels = {'name': 'Nazwa procedury'}
#
#
# class AddProcedureForm(forms.ModelForm):
#     class Meta:
#         model = Procedure
#         fields = '__all__'
#         labels = {'name': "Nazwa procedury",
#                   'details': "Szczegóły procedury",
#                   'duration': "Czas trwania (format: GG:MM:SS)",
#                   'medical_institutions': "Placówka wykonawcza"}
#
#
# class UpdateProcedureForm(forms.ModelForm):
#     class Meta:
#         model = Procedure
#         fields = '__all__'
#         labels = {'name': "Nazwa procedury",
#                   'details': "Szczegóły procedury",
#                   'duration': "Czas trwania (format: GG:MM:SS)",
#                   'medical_institutions': "Placówka wykonawcza"}
#
#
# # class AddPersonnelForm(forms.ModelForm):
# #     class Meta:
# #         model = Personnel
# #         fields = '__all__'
# #         labels = {'name': "Imię",
# #                   'surname': "Nazwisko",
# #                   'medical_institutions': "Placówka wykonawcza",
# #                   'procedures': "Procedury"}
# #
# #
# # class UpdatePersonnelForm(forms.ModelForm):
# #     class Meta:
# #         model = Personnel
# #         fields = '__all__'
# #         labels = {'name': "Imię",
# #                   'surname': "Nazwisko",
# #                   'medical_institutions': "Placówka wykonawcza",
# #                   'procedures': "Procedury"}
# #
#
# class CreateTimeTableForm(forms.ModelForm):
#     class Meta:
#         model = TimeTable
#         fields = '__all__'
#         labels = {'day': 'Dzień tygodnia',
#                   'medical_institution': 'Placówka',
#                   'start': 'Czas rozpoczęcia pracy',
#                   'end': 'Czas zakończenia pracy'}
#         widgets = {'start': forms.TimeInput(),
#                    'end': forms.TimeInput()}
#
#
# class UpdateTimeTableForm(forms.ModelForm):
#     class Meta:
#         model = TimeTable
#         fields = ['day', 'start', 'end']
#         labels = {'day': 'Dzień tygodnia',
#                   'start': 'Czas rozpoczęcia pracy',
#                   'end': 'Czas zakończenia pracy'}
#         widgets = {'start': forms.TimeInput(),
#                    'end': forms.TimeInput()}