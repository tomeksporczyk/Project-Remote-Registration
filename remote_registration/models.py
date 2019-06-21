from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Provinces(models.Model):
    '''todo: zmienic nazwy wojewodztw na wielkie litery'''
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class MedicalInstitution(models.Model):
    '''todo: lepsze rozwiązanie = tabela z województwami, tak jak w przypadku dni tygodnia'''
    ward = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    province = models.ForeignKey(Provinces, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=64)

    def __str__(self):
        return f'Oddział: {self.ward} \nInstytuja: {self.name}'

    def save(self, *args, **kwargs):
        for field_name in ['ward', 'name', 'city', 'address']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super().save(*args, **kwargs)


class Procedure(models.Model):
    name = models.CharField(max_length=128)
    details = models.CharField(max_length=256)
    duration = models.DurationField()
    medical_institutions = models.ManyToManyField(MedicalInstitution)

    def __str__(self):
        return f'Nazwa: {self.name} \n Szczegóły {self.details}'

    def save(self, *args, **kwargs):
        for field_name in ['name', 'details']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super().save(*args, **kwargs)


class Personnel(models.Model):
    '''
     todo: pozwiązać z tabelą User, tworząc randomowe hasło wysyłane przy pomocy maila na podany adres https://docs.djangoproject.com/en/2.2/topics/email/. DODAĆ nową kolumnę: email
     todo: więcej informcji o pracowniku, do celów walidacji przy wprowadzaniu do bazy danych
     '''
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    medical_institutions = models.ManyToManyField(MedicalInstitution, through="TimeTable")
    procedures = models.ManyToManyField(Procedure)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        for field_name in ['name', 'surname']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super().save(*args, **kwargs)


class WeekDays(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.name}'


class TimeTable(models.Model):
    day = models.ForeignKey(WeekDays, on_delete=models.CASCADE, null=True)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)

    def __str__(self):
        return f'Pracownik: {self.personnel.name} {self.personnel.surname} dzień: {self.day}'


class Event(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)


class Referral(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)