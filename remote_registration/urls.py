
from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("institution/add", AddMedicalInstitution.as_view(), name='add_institution'),
    path("institution/update/<int:pk>", UpdateMedicalInstitution.as_view(), name='update_institution'),
    path("institution/delete/<int:pk>", DeleteMedicalInstitution.as_view(), name='delete_institution'),
    path("procedure/add", AddProcedure.as_view(), name='add_procedure'),
    path("procedure/update/<int:pk>", UpdateProcedure.as_view(), name='update_procedure'),
    path("procedure/delete/<int:pk>", DeleteProcedure.as_view(), name='delete_procedure'),
    path("personnel/add", AddPersonnel.as_view(), name='add_personnel'),
    path("timetable/add", CreateTimeTable.as_view(), name='add_time_table'),
    path("timetable/update/<int:pk>", UpdateTimeTable.as_view(), name='update_time_table'),
    path("timetable/delete/<int:pk>", DeleteTimeTable.as_view(), name='delete_time_table'),

]