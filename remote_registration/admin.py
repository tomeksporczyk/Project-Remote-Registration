from django.contrib import admin

# Register your models here.
from remote_registration.models import *

admin.site.register(MedicalInstitution)
admin.site.register(ProcedureCategories)
admin.site.register(Procedure)
admin.site.register(TimeTable)
admin.site.register(Referral)
admin.site.register(Appointment)
admin.site.register(User)