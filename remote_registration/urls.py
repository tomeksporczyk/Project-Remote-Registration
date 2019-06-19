
from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("institution/", MedicalInstitutionView.as_view(), name='institution'),
    path("institution/add", AddMedicalInstitution.as_view(), name='add_institution'),
    path("institution/update/<int:pk>", UpdateMedicalInstitution.as_view(), name='update_institution'),
    path("institution/delete/<int:pk>", DeleteMedicalInstitution.as_view(), name='delete_institution'),
    path("procedure/", ProcedureView.as_view(), name='procedure'),
    path("procedure/add", AddProcedure.as_view(), name='add_procedure'),
    path("procedure/update/<int:pk>", UpdateProcedure.as_view(), name='update_procedure'),
    path("procedure/delete/<int:pk>", DeleteProcedure.as_view(), name='delete_procedure'),
    path("personnel/", PersonnelView.as_view(), name='personnel'),
    path("personnel/add", AddPersonnel.as_view(), name='add_personnel'),
    path("personnel/update/<int:pk>", UpdatePersonnel.as_view(), name='update_personnel'),
    path("personnel/delete/<int:pk>", DeletePersonnel.as_view(), name='delete_personnel'),
    path("timetable/", TimeTableView.as_view(), name='time_table'),
    path("timetable/add", CreateTimeTable.as_view(), name='add_time_table'),
    path("timetable/update/<int:pk>", UpdateTimeTable.as_view(), name='update_time_table'),
    path("timetable/delete/<int:pk>", DeleteTimeTable.as_view(), name='delete_time_table'),

]