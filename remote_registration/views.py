from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, CreateView, DeleteView

from remote_registration.forms import *


class HomeView(View):
    def get(self, request):
        return render(request, 'remote_registration/base.html')


class AddMedicalInstitution(FormView):
    form_class = AddMedicalInstitutionForm
    template_name = "remote_registration/uni_form_add.html"
    success_url = reverse_lazy('institution')

    def form_valid(self, form):
        name = form.cleaned_data.get('name').upper()
        city = form.cleaned_data.get('city').upper()
        address = form.cleaned_data.get('address').upper()
        ward = form.cleaned_data.get('ward').upper()
        institution = MedicalInstitution.objects.filter(name=name,
                                                        city=city,
                                                        address=address,
                                                        ward=ward)
        print(institution.count())
        if institution.count() == 0:
            form.save()
            return super().form_valid(form)
        self.success_url = reverse_lazy('add_institution')
        return super().form_valid(form)


class UpdateMedicalInstitution(UpdateView):
    '''todo: województwo w formularzu nie jest importowane z bazy danych (zawsze jest śląskie)'''
    form_class = UpdateMedicalInstitutionForm
    model = MedicalInstitution
    success_url = reverse_lazy('institution')
    template_name = 'remote_registration/uni_form_update.html'


class DeleteMedicalInstitution(DeleteView):
    model = MedicalInstitution
    template_name = 'remote_registration/uni_form_delete.html'
    success_url = reverse_lazy('institution')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(MedicalInstitution, id=id_)


class AddProcedure(FormView):
    form_class = AddProcedureForm
    template_name = 'remote_registration/uni_form_add.html'
    success_url = reverse_lazy('procedure')

    def form_valid(self, form):
        name = form.cleaned_data.get('name').upper()
        details = form.cleaned_data.get('details').upper()
        duration = form.cleaned_data.get('duration')
        procedure = Procedure.objects.filter(name=name,
                                             details=details,
                                             duration=duration,
                                             )
        if procedure.count() == 0:
            form.save()
            return super().form_valid(form)
        self.success_url = reverse_lazy('add_procedure')
        return super().form_valid(form)


class UpdateProcedure(UpdateView):
    form_class = UpdateProcedureForm
    model = Procedure
    success_url = reverse_lazy('procedure')
    template_name = 'remote_registration/uni_form_update.html'


class DeleteProcedure(DeleteView):
    model = Procedure
    template_name = 'remote_registration/uni_form_delete.html'
    success_url = reverse_lazy('procedure')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Procedure, id=id_)


class AddPersonnel(FormView):
    form_class = AddPersonnelForm
    template_name = 'remote_registration/uni_form_add.html'

    def form_valid(self, form):
        name = form.cleaned_data.get('name').upper()
        surname = form.cleaned_data.get('surname').upper()
        personnel = Personnel.objects.filter(name=name,
                                             surname=surname)
        if personnel.count() == 0:
            form.save()
            personnel = Personnel.objects.get(name=name, surname=surname)
            timetable = personnel.timetable_set.all()[0].pk
            self.success_url = reverse_lazy('update_time_table', kwargs={'pk': timetable})
            return super().form_valid(form)
        self.success_url = reverse_lazy('add_personnel')
        return super().form_valid(form)


class UpdatePersonnel(UpdateView):
    '''todo: procedury i placówka defaultowo powinny być zaznaczone zgodnie z bazą danych'''
    form_class = UpdatePersonnelForm
    model = Personnel
    success_url = reverse_lazy('personnel')
    template_name = 'remote_registration/uni_form_update.html'


class DeletePersonnel(DeleteView):
    model = Personnel
    template_name = 'remote_registration/uni_form_delete.html'
    success_url = reverse_lazy('personnel')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Personnel, id=id_)


class CreateTimeTable(CreateView):
    form_class = CreateTimeTableForm
    model = TimeTable
    success_url = reverse_lazy('time_table')
    template_name = 'remote_registration/uni_form_add.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start'].widget = forms.TimeInput()
        return form


class UpdateTimeTable(UpdateView):
    form_class = UpdateTimeTableForm
    model = TimeTable
    success_url = reverse_lazy('time_table')
    template_name = 'remote_registration/uni_form_update.html'


class DeleteTimeTable(DeleteView):
    model = TimeTable
    template_name = 'remote_registration/uni_form_delete.html'
    success_url = reverse_lazy('time_table')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(TimeTable, id=id_)

#
# class AddEvent(View):
#     def get(self, request):
#         return render(request, 'remote_registration/uni_form_add.html')


class MedicalInstitutionView(View):
    def get(self, request):
        institutions = MedicalInstitution.objects.all()
        context = {'institutions': institutions}
        return render(request, 'remote_registration/all_medical_institution.html', context)


class ProcedureView(View):
    def get(self, request):
        procedures = Procedure.objects.all()
        context = {'procedures': procedures}
        return render(request, 'remote_registration/all_procedure.html', context)


class PersonnelView(View):
    def get(self, request):
        personnel = Personnel.objects.all().order_by('pk')
        context = {'personnel': personnel}
        return render(request, 'remote_registration/all_personnel.html', context)


class TimeTableView(View):
    def get(self, request):
        time_table = TimeTable.objects.all().order_by('personnel')
        context = {'time_table': time_table}
        return render(request, 'remote_registration/all_time_table.html', context)


class AddReferral(View):
    pass


class LoginView(View):
    def get(self, request):
        return render(request, 'remote_registration/uni_form.html', context={'form': LoginForm(),
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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class AddUserView(View):
    def get(self, request):
        form = UserCreationForm()
        context = {'form': form, 'submit': 'Zarejestruj się'}
        return render(request, 'remote_registration/uni_form.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home'))
        else:
            context = {'form': form, 'submit': 'Zarejestruj się'}
            return render(request, 'remote_registration/uni_form.html', context)


class UpdateUserView(View):
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


class UserDetailView(View):
    def get(self, request):
        return render(request, 'remote_registration/user_details.html')


class ChangePasswordView(View):
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

