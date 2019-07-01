from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Q


class Provinces(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class MedicalInstitution(models.Model):
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


class ProcedureCategories(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        for field_name in ['name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super().save(*args, **kwargs)


class Procedure(models.Model):
    name = models.ForeignKey(ProcedureCategories, on_delete=models.CASCADE)
    details = models.CharField(max_length=256)
    duration = models.DurationField()
    medical_institutions = models.ManyToManyField(MedicalInstitution, through="TimeTable")

    def __str__(self):

        return f'Nazwa: {self.name} Szczegóły {self.details}'

    def save(self, *args, **kwargs):
        for field_name in ['details']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super().save(*args, **kwargs)


class TimeTable(models.Model):
    WEEKDAYS = (
        (0, 'Poniedziałek'),
        (1, 'Wtorek'),
        (2, 'Środa'),
        (3, 'Czwartek'),
        (4, 'Piątek'),
        (5, 'Sobota'),
        (6, 'Niedziela')
    )
    name = models.IntegerField(choices=WEEKDAYS)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return self.WEEKDAYS[self.name][1]


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    User model. Describes both, customer user and additionaly
    is a base for workshop instance (:model:`workshop.Workshop`)
    """
    username = None
    email = models.EmailField('user email', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    phone_number = models.CharField(verbose_name='phone number', max_length=17)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Referral(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_referrals')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    procedure = models.ForeignKey(ProcedureCategories, on_delete=models.CASCADE)
    details = models.ForeignKey(Procedure, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pacjent: {self.patient.first_name} {self.patient.last_name} Badanie: {self.procedure} {self.details}"


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    procedure = models.ForeignKey(ProcedureCategories, on_delete=models.CASCADE)
    details = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)

    @classmethod
    def sign_for_datetime(cls, patient, date_time, medical_institution, procedure):
        time_table = TimeTable.objects.filter(day=date_time.weekday(), procedure=procedure, medical_institution=medical_institution)
        start_date_time = date_time
        end_date_time = date_time + timedelta(hours=procedure.duration)
        if cls.objects.filter(medical_institution=medical_institution, procedure=procedure).filter(
            Q(start__gte=start_date_time, end__lt=end_date_time),
            Q(start__lte=start_date_time, end__gt=end_date_time),
            Q(end__gte=start_date_time, end__lte=end_date_time),
            Q(start__gte=start_date_time, start__lte=end_date_time),
        ).count():
            raise ValueError('Zajęta data')
        elif time_table.start < start_date_time and time_table.end < end_date_time:
            raise ValueError('Poza godzinami przyjęć')
        else:
            return cls.objects.create(patient=patient, medical_institution=medical_institution, procedure=procedure)

#
# class Personnel(models.Model):
#
#     name = models.CharField(max_length=128)
#     surname = models.CharField(max_length=128)
#     medical_institutions = models.ManyToManyField(MedicalInstitution, through="TimeTable")
#     procedures = models.ManyToManyField(ProcedureCategories)
#
#     def __str__(self):
#         return f'{self.name} {self.surname}'
#
#     def save(self, *args, **kwargs):
#         for field_name in ['name', 'surname']:
#             val = getattr(self, field_name, False)
#             if val:
#                 setattr(self, field_name, val.upper())
#         super().save(*args, **kwargs)
