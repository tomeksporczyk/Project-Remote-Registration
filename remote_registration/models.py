from django.db import models

# Create your models here.


class MedicalInstitution(models.Model):

    name = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    services = models.ManyToManyField("Procedure")


class Procedure(models.Model):
    name = models.CharField(max_length=128)
    details = models.CharField(max_length=256)
    duration = models.DurationField()



class Personnel(models.Model):
    '''
     todo: pozwiązać z tabelą User, tworząc randomowe hasło wysyłane przy pomocy maila na podany adres https://docs.djangoproject.com/en/2.2/topics/email/. DODAĆ nową kolumnę: email
     '''
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    medical_institutions = models.ManyToManyField(MedicalInstitution, through="TimeTable")
    service = models.ManyToManyField(Procedure)


class WeekDays(models.Model):
    name = models.CharField(max_length=10)


class TimeTable(models.Model):
    day = models.ForeignKey(WeekDays, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()


class Event(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    service = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)
