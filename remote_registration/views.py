from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
import dateutil.parser
from django.utils.timezone import make_aware

from remote_registration.models import *
# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, UpdateView, CreateView, DeleteView

from remote_registration.forms import *


class HomeView(View):
    def get(self, request):
        return render(request, 'remote_registration/base.html')


class MedicalInstitutionView(View):
    '''todo: każda instytucja to link do widoku z informacjami o szpitalu (może mapką?) i procedurach lub oddziałach'''
    def get(self, request):
        institutions = MedicalInstitution.objects.all()
        search_box = request.GET.get('search_box', None)
        if search_box is not None and len(search_box) > 0:
            institutions = institutions.filter(name__icontains=search_box)
        context = {'institutions': institutions}
        return render(request, 'remote_registration/all_medical_institution.html', context)


class ProcedureView(View):
    '''todo: każda procedura to link do listy instytucji wykonujących badanie z najbliższymi terminami
    wyszukiwarka procedur'''
    def get(self, request):
        procedures = Procedure.objects.all()
        search_box = request.GET.get('search_box', None)
        if search_box is not None and len(search_box) > 0:
            category = ProcedureCategories.objects.filter(name__icontains=search_box)
            if category.count():
                procedures = procedures.filter(name=category[0].pk)
        context = {'procedures': procedures}
        return render(request, 'remote_registration/all_procedure.html', context)


class ProcedureDetailsView(View):
    def get(self, request, pk):
        procedure = Procedure.objects.get(pk=pk)
        medical_institutions = procedure.medical_institutions.all().distinct()
        today = datetime.now().astimezone(None)
        # print(today)
        interval = procedure.duration
        # institution = MedicalInstitution.objects.get(pk=1)
        # time_tables = procedure.timetable_set.filter(medical_institution=institution.pk)
        # part_a_time_tables = time_tables.filter(name__gte=today.weekday())
        # part_b_time_tables = time_tables.filter(name__lt=today.weekday())
        # time_tables = list(part_a_time_tables) + list(part_b_time_tables)  # table with datetime objects during which procedure is performed
        # institution.available_date = datetime.combine(today.date(), time_tables[0].start).astimezone(None)
        # print(institution.available_date)
        # institution.available_date += interval
        # print(institution.available_date)
        # print(institution.available_date.time())
        for institution in medical_institutions:
            '''
            for every institution creates a property 'available_date' with value set to the
            earliest available appointment date.
            '''
            # weeks_upfront = 0  # weeks counter, starting as present week
            time_tables = procedure.timetable_set.filter(medical_institution=institution.pk)
            part_a_time_tables = time_tables.filter(name__gte=today.weekday())
            part_b_time_tables = time_tables.filter(name__lt=today.weekday())
            time_tables = list(part_a_time_tables) + list(part_b_time_tables)  # table with datetime objects during which procedure is performed
            institutions_appointments = [timestamp.start.astimezone(None) for timestamp in Appointment.objects.filter(medical_institution=institution,
                                                                                                                      details=procedure).filter(start__gte=today)]  # already existing appointments
            appointments_counter = 0
            weeks_upfront = 0
            day = 0
            institution.available_date = datetime.combine(today.date(), time_tables[day].start).astimezone(None)
            while institution.available_date in institutions_appointments or institution.available_date < today:

                institution.available_date = datetime.combine(today.date()+timedelta(days=day)+timedelta(weeks=weeks_upfront),
                                                              time_tables[day].start+interval*appointments_counter).astimezone(None)
                appointments_counter += 1
                # institution.available_date += interval
                # print(institution.available_date)
                if institution.available_date.time() >= time_tables[day].end:
                    print('dupa')
                    if day != len(time_tables)-1:
                        day += 1
                        while institution.available_date.weekday() != time_tables[day].name:
                            institution.available_date += timedelta(days=1)
                    else:
                        day = 0
                        weeks_upfront += 1

            # iterator = len(time_tables)
            # i = 0
            # while i != iterator:
            #     print('iterator', i)
            #     appointment_hour = datetime.combine(today.date()+timedelta(days=i+weeks_upfront*7), time_tables[i].start).astimezone(None)  # first appointment of the day. Value increased on iteration of the day and the week
            #     institution.available_date = appointment_hour  # create a property for institution, set to first available appointment for that day
            #     day_count = 0
            #     while appointment_hour.weekday() != time_tables[i].name:
            #         appointment_hour = datetime.combine(today + timedelta(days=i + day_count), time_tables[i].start).astimezone(None)  # set the weekday of the monthday according to the weekday of time_tables
            #         day_count += 1
            #     while appointment_hour < timezone.now():
            #         appointment_hour += interval  # set the time of the appointment tobe greater than equal to now
            #     end_of_work = datetime.combine(appointment_hour.date(), time_tables[i].end).astimezone(None)
            #     if appointment_hour > end_of_work:
            #         i += 1  # if now is later than works end time go to another day of the time_tables
            #         continue
            #     while appointment_hour < end_of_work-interval:
            #         # set the appointment_hour according to the already existing appointments
            #         if appointment_hour not in institutions_appointments:
            #             institution.available_date = appointment_hour  # if the appointment hour doesn't exist set property's value
            #             break
            #         else:
            #             appointment_hour += interval
            #     if appointment_hour not in institutions_appointments:
            #         i = iterator  # stops the while loop
            #         break
            #     else:  # goes to another week
            #         weeks_upfront += 1
            #         i = 0
        context = {'procedure': procedure, 'medical_institutions': medical_institutions}
        return render(request, 'remote_registration/procedure_details.html', context)


class PatientReferrals(LoginRequiredMixin, View):
    def get(self, request):
        referrals = Referral.objects.filter(patient_id=request.user.pk)
        return render(request, 'remote_registration/all_referral.html', context={'referrals': referrals})


class CreatedReferrals(LoginRequiredMixin, View):
    def get(self, request):
        referrals = Referral.objects.filter(created_by=request.user.pk)
        return render(request, 'remote_registration/created_referrals.html', context={'referrals': referrals})


class AddReferral(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'remote_registration.add_referral'
    def get(self, request):
        form = AddReferralForm
        context = {'form': form, 'submit': 'Dodaj'}
        return render(request, 'remote_registration/referral_add.html', context)

    def post(self,request):
        form = AddReferralForm(request.POST)
        if form.is_valid():
            created_by = request.user
            patient = form.cleaned_data.get('patient')
            procedure = form.cleaned_data.get('procedure')
            details = form.cleaned_data.get('details')
            Referral.objects.create(created_by=created_by, patient=patient, procedure=procedure, details=details)
            return redirect(reverse_lazy('referral-created'))
        else:
            context = {'form': form, 'submit': 'Dodaj'}
            return render(request, 'remote_registration/referral_add.html', context)


def load_procedure_details(request):
    procedure_id = request.GET.get('procedure')
    details = Procedure.objects.filter(name__id=procedure_id).order_by('details')
    return render(request, 'remote_registration/details_dropdown_list_options.html', {'details': details})


class UpdateReferral(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'remote_registration.change_referral'
    form_class = UpdateReferralForm
    model = Referral
    success_url = reverse_lazy('referral-created')
    template_name = 'remote_registration/referral_update.html'


class DeleteReferral(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'remote_registration.delete_referral'
    model = Referral
    template_name = 'remote_registration/uni_form_delete.html'
    success_url = reverse_lazy('referral-created')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Referral, id=id_)


class ChooseInstitutionView(LoginRequiredMixin, View):
    def get(self, request, referral_pk):
        details = Referral.objects.filter(patient=request.user).get(pk=referral_pk).details
        medical_institutions = details.medical_institutions.all().distinct()
        context = {'medical_institutions': medical_institutions}
        return render(request, 'remote_registration/appointment_institution.html', context)


class ChooseDateView(LoginRequiredMixin, View):
    def get(self, request, referral_pk, institution_pk):
        '''
        :return: Table with available datetime appointments.
        '''
        weeks_upfront = abs(int(request.GET.get('weeks_upfront', 0)))
        referral = Referral.objects.get(pk=referral_pk)
        details = referral.details
        medical_institution = MedicalInstitution.objects.get(pk=institution_pk)
        time_tables = TimeTable.objects.filter(procedure=details, medical_institution=medical_institution).order_by('name')
        interval = details.duration
        today = datetime.today().astimezone(None) + timedelta(days=7*weeks_upfront)  # get todays date with local timezone
        part_a_time_tables = time_tables.filter(name__gte=today.weekday())
        part_b_time_tables = time_tables.filter(name__lt=today.weekday())
        time_tables = list(part_a_time_tables) + list(part_b_time_tables)  # create days table with days during which procedure is performed
        current_week = []
        existing_appointments = [timestamp.start.astimezone(None) for timestamp in Appointment.objects.filter(start__gte=today)]  # list with appointments already created
        for i, day in enumerate(time_tables):
            hours_list = []
            appointment_hour = datetime.combine(today+timedelta(days=i), day.start)  # datetime increased on every iterration
            if i == 0 and weeks_upfront == 0:  # sets the datetime to be greater than now
                while appointment_hour.astimezone(None) < timezone.now():
                    appointment_hour += interval
            day_count = 0
            while appointment_hour.weekday() != day.name:  # sets a month date for weekday
                appointment_hour = datetime.combine(today + timedelta(days=(i + day_count)), day.start)
                day_count += 1
            j = 0
            while appointment_hour+j*interval < datetime.combine((appointment_hour.date()), day.end):  # creates list of appointment hours for every day
                if make_aware(appointment_hour+j*interval) in existing_appointments:  # if apointment already exists do not include this datetime
                    j += 1
                    continue
                hours_list.append(appointment_hour+j*interval)
                j += 1
            current_week.append((day, hours_list))
        return render(request, 'remote_registration/appointment_time_table.html', context={'time_tables': current_week,
                                                                                           'weeks_upfront': weeks_upfront,
                                                                                           'referral_pk': referral_pk,
                                                                                           'institution_pk': institution_pk})

    def post(self, request, referral_pk, institution_pk):
        referral = Referral.objects.get(pk=referral_pk)
        patient = request.user
        procedure = referral.procedure
        details = referral.details
        medical_institution = MedicalInstitution.objects.get(pk=institution_pk)
        start = dateutil.parser.parse(request.POST.get('datetime'))
        end = start+details.duration
        Appointment.objects.create(patient=patient,
                                   start=start,
                                   end=end,
                                   procedure=procedure,
                                   details=details,
                                   medical_institution=medical_institution)
        referral.delete()
        return redirect(reverse_lazy('referral'))


class AppointmentsView(View):
    def get(self, request):
        now = datetime.now().astimezone(None)
        user_appointments = Appointment.objects.filter(patient=request.user)
        future_appointments = user_appointments.filter(start__gte=now)
        past_appointments = user_appointments.filter(start__lt=now)
        context = {'future_appointments': future_appointments, 'past_appointments': past_appointments}
        return render(request, 'remote_registration/all_appointment.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'remote_registration/login_form.html', context={'form': LoginForm(),
                                                                             'submit': 'Zaloguj'})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_login')
            user_password = form.cleaned_data.get('user_password')
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                login(request, user)
                next_ = request.GET.get('next')
                if next_ is not None:
                    return redirect(next_)
                else:
                    return redirect(reverse_lazy('home'))
            else:
                message = 'Niepoprawne dane logowania'
                return render(request, 'remote_registration/uni_form.html', context={'form': LoginForm(),
                                                                                     'submit': 'Zaloguj',
                                                                                     'message': message})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class AddUserView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {'form': form, 'submit': 'Zarejestruj się'}
        return render(request, 'remote_registration/uni_form.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home'))
        else:
            context = {'form': form, 'submit': 'Zarejestruj się'}
            return render(request, 'remote_registration/uni_form.html', context)


class UpdateUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateUserForm(instance=request.user)
        context = {'form': form, 'submit': 'Zapisz zmiany'}
        return render(request, 'remote_registration/uni_form.html', context)

    def post(self, request):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('user_details'))
        else:
            context = {'form': form, 'submit': 'Zapisz zmiany'}
            return render(request, 'remote_registration/uni_form.html', context)


class UserDetailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'remote_registration/user_details.html')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        context = {'form': form, 'submit': 'Zapisz zmiany'}
        return render(request, 'remote_registration/uni_form.html', context)

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse_lazy('user_details'))
        else:
            context = {'form': form, 'submit': 'Zapisz zmiany'}
            return render(request, 'remote_registration/uni_form.html', context)

#
# class AddMedicalInstitution(PermissionRequiredMixin, LoginRequiredMixin, FormView):
#     permission_required = 'remote_registration.add_medicalinstitution'
#     form_class = AddMedicalInstitutionForm
#     template_name = "remote_registration/uni_form_add.html"
#     success_url = reverse_lazy('institution')
#
#     def form_valid(self, form):
#         name = form.cleaned_data.get('name').upper()
#         city = form.cleaned_data.get('city').upper()
#         address = form.cleaned_data.get('address').upper()
#         ward = form.cleaned_data.get('ward').upper()
#         institution = MedicalInstitution.objects.filter(name=name,
#                                                         city=city,
#                                                         address=address,
#                                                         ward=ward)
#         if institution.count() == 0:
#             form.save()
#             return super().form_valid(form)
#         self.success_url = reverse_lazy('add_institution')
#         return super().form_valid(form)
#
#
# class UpdateMedicalInstitution(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
#     permission_required = 'remote_registration.change_medicalinstitution'
#     form_class = UpdateMedicalInstitutionForm
#     model = MedicalInstitution
#     success_url = reverse_lazy('institution')
#     template_name = 'remote_registration/uni_form_update.html'
#
#
# class DeleteMedicalInstitution(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
#     permission_required = 'remote_registration.delete_medicalinstitution'
#     model = MedicalInstitution
#     template_name = 'remote_registration/uni_form_delete.html'
#     success_url = reverse_lazy('institution')
#
#     def get_object(self):
#         id_ = self.kwargs.get('pk')
#         return get_object_or_404(MedicalInstitution, id=id_)

# class AddProcedureCategory(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
#     permission_required = 'remote_registration.add_procedurecategories'
#     model = ProcedureCategories
#     form_class = AddProcedureCategoryForm
#     success_url = reverse_lazy('procedure')
#     template_name = 'remote_registration/uni_form_add.html'
#
#
# class DeleteProcedureCategory(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
#     permission_required = 'remote_registration.delete_procedurecategories'
#     model = ProcedureCategories
#     template_name = 'remote_registration/uni_form_delete.html'
#     success_url = reverse_lazy('procedure')
#
#     def get_object(self):
#         id_ = self.kwargs.get('pk')
#         return get_object_or_404(ProcedureCategories, id=id_)

#
# class AddProcedure(PermissionRequiredMixin, LoginRequiredMixin, FormView):
#     permission_required = 'remote_registration.add_procedure'
#     form_class = AddProcedureForm
#     template_name = 'remote_registration/uni_form_add.html'
#     success_url = reverse_lazy('procedure')
#
#     def form_valid(self, form):
#         name = form.cleaned_data.get('name')
#         details = form.cleaned_data.get('details').upper()
#         duration = form.cleaned_data.get('duration')
#         procedure = Procedure.objects.filter(name=name,
#                                              details=details,
#                                              duration=duration,
#                                              )
#         if procedure.count() == 0:
#             form.save()
#             return super().form_valid(form)
#         self.success_url = reverse_lazy('add_procedure')
#         return super().form_valid(form)

#
#
# class UpdateProcedure(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
#     permission_required = 'remote_registration.change_procedure'
#     form_class = UpdateProcedureForm
#     model = Procedure
#     success_url = reverse_lazy('procedure')
#     template_name = 'remote_registration/uni_form_update.html'
#
#
# class DeleteProcedure(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
#     permission_required = 'remote_registration.delete_procedure'
#     model = Procedure
#     template_name = 'remote_registration/uni_form_delete.html'
#     success_url = reverse_lazy('procedure')
#
#     def get_object(self):
#         id_ = self.kwargs.get('pk')
#         return get_object_or_404(Procedure, id=id_)
#
#
# # class PersonnelView(View):
# #     def get(self, request):
# #         personnel = Personnel.objects.all().order_by('pk')
# #         context = {'personnel': personnel}
# #         return render(request, 'remote_registration/all_personnel.html', context)
#
# #
# # class AddPersonnel(PermissionRequiredMixin, LoginRequiredMixin, FormView):
# #     permission_required = 'remote_registration.add_personnel'
# #     form_class = AddPersonnelForm
# #     template_name = 'remote_registration/uni_form_add.html'
# #
# #     def form_valid(self, form):
# #         name = form.cleaned_data.get('name').upper()
# #         surname = form.cleaned_data.get('surname').upper()
# #         personnel = Personnel.objects.filter(name=name,
# #                                              surname=surname)
# #         if personnel.count() == 0:
# #             form.save()
# #             personnel = Personnel.objects.get(name=name, surname=surname)
# #             timetable = personnel.timetable_set.all()[0].pk
# #             self.success_url = reverse_lazy('update_time_table', kwargs={'pk': timetable})
# #             return super().form_valid(form)
# #         self.success_url = reverse_lazy('add_personnel')
# #         return super().form_valid(form)
#
# #
# # class UpdatePersonnel(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
# #     permission_required = 'remote_registration.change_personnel'
# #     form_class = UpdatePersonnelForm
# #     model = Personnel
# #     success_url = reverse_lazy('personnel')
# #     template_name = 'remote_registration/uni_form_update.html'
# #
# #
# # class DeletePersonnel(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
# #     permission_required = 'remote_registration.delete_personnel'
# #     model = Personnel
# #     template_name = 'remote_registration/uni_form_delete.html'
# #     success_url = reverse_lazy('personnel')
# #
# #     def get_object(self):
# #         id_ = self.kwargs.get('pk')
# #         return get_object_or_404(Personnel, id=id_)

#
# class TimeTableView(PermissionRequiredMixin, LoginRequiredMixin, View):
#     permission_required = 'remote_registration.view_timetable'
#     def get(self, request):
#         time_table = TimeTable.objects.all()
#         context = {'time_table': time_table}
#         return render(request, 'remote_registration/all_time_table.html', context)
#
#
# class CreateTimeTable(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
#     permission_required = 'remote_registration.add_timetable'
#     form_class = CreateTimeTableForm
#     model = TimeTable
#     success_url = reverse_lazy('time_table')
#     template_name = 'remote_registration/uni_form_add.html'
#
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['start'].widget = forms.TimeInput()
#         return form
#
#
# class UpdateTimeTable(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
#     permission_required = 'remote_registration.change_timetable'
#     form_class = UpdateTimeTableForm
#     model = TimeTable
#     success_url = reverse_lazy('time_table')
#     template_name = 'remote_registration/uni_form_update.html'
#
#
# class DeleteTimeTable(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
#     permission_required = 'remote_registration.delete_timetable'
#     model = TimeTable
#     template_name = 'remote_registration/uni_form_delete.html'
#     success_url = reverse_lazy('time_table')
#
#     def get_object(self):
#         id_ = self.kwargs.get('pk')
#         return get_object_or_404(TimeTable, id=id_)