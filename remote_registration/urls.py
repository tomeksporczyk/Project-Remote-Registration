
from django.urls import path

from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("institution/", MedicalInstitutionView.as_view(), name='institution'),
    path("institution/<int:pk>", MedicalInstitutionDetailsView.as_view(), name='institution_details'),
    path("procedure/", ProcedureView.as_view(), name='procedure'),
    path("procedure/<int:pk>", ProcedureDetailsView.as_view(), name='procedure_details'),
    path("appointments/", AppointmentsView.as_view(), name='appointments'),
    path("referral/", PatientReferrals.as_view(), name='referral'),
    path("referral-created/", CreatedReferrals.as_view(), name='referral-created'),
    path("referral/add", AddReferral.as_view(), name='add_referral'),
    path("referral/update/<int:pk>", UpdateReferral.as_view(), name='update_referral'),
    path("referral/delete/<int:pk>", DeleteReferral.as_view(), name='delete_referral'),
    path("appointment/<int:referral_pk>/", ChooseInstitutionView.as_view(), name='appointment_institution'),
    path("appointment/<int:referral_pk>/<int:institution_pk>", ChooseDateView.as_view(), name='appointment_date'),
    path('ajax/load-details/', load_procedure_details, name='ajax_load_details'),
    # path("institution/add", AddMedicalInstitution.as_view(), name='add_institution'),
    # path("institution/update/<int:pk>", UpdateMedicalInstitution.as_view(), name='update_institution'),
    # path("institution/delete/<int:pk>", DeleteMedicalInstitution.as_view(), name='delete_institution'),
    # path("procedure/add", AddProcedure.as_view(), name='add_procedure'),
    # path("procedure/category/add", AddProcedureCategory.as_view(), name='add_procedure_category'),
    # path("procedure/category/delete/<int:pk>", DeleteProcedureCategory.as_view(), name='delete_procedure_category'),
    # path("procedure/update/<int:pk>", UpdateProcedure.as_view(), name='update_procedure'),
    # path("procedure/delete/<int:pk>", DeleteProcedure.as_view(), name='delete_procedure'),
    # path("personnel/", PersonnelView.as_view(), name='personnel'),
    # path("personnel/add", AddPersonnel.as_view(), name='add_personnel'),
    # path("personnel/update/<int:pk>", UpdatePersonnel.as_view(), name='update_personnel'),
    # path("personnel/delete/<int:pk>", DeletePersonnel.as_view(), name='delete_personnel'),
    # path("timetable/", TimeTableView.as_view(), name='time_table'),
    # path("timetable/add", CreateTimeTable.as_view(), name='add_time_table'),
    # path("timetable/update/<int:pk>", UpdateTimeTable.as_view(), name='update_time_table'),
    # path("timetable/delete/<int:pk>", DeleteTimeTable.as_view(), name='delete_time_table'),
]

urlpatterns += staticfiles_urlpatterns()