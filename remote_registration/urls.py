
from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("institution/add", AddMedicalInstitution.as_view(), name='add_institution'),
    path("procedure/add", AddProcedure.as_view(), name='add_procedure'),

]