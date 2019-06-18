from django import forms

from remote_registration.models import MedicalInstitution


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
        labels = {'ward': 'Oddział',
                  'name': 'Nazwa instytucji',
                  'city': 'Miasto',
                  'province': 'Województwo',
                  'address': "Adres"}
        widgets = {'province': forms.Select(choices=PROVINCES)}

        fields = '__all__'


