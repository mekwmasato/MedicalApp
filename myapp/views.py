from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from accounts.models import DoctorPatientRelationship
from accounts.forms import PatientSelectionForm


User = get_user_model()

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_doctor:
            relationships = DoctorPatientRelationship.objects.filter(doctor=self.request.user)
            registered_patients = [relationship.patient for relationship in relationships]
            form = PatientSelectionForm()
            context.update({'is_doctor': True, 'registered_patients': registered_patients, 'form': form})
        else:
            context.update({'is_doctor': False})
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_doctor:
            return redirect('index')
        form = PatientSelectionForm(request.POST)
        if form.is_valid():
            selected_patients = form.cleaned_data['patients']
            for patient in selected_patients:
                DoctorPatientRelationship.objects.get_or_create(doctor=request.user, patient=patient)
            return redirect('index')
        relationships = DoctorPatientRelationship.objects.filter(doctor=request.user)
        registered_patients = [relationship.patient for relationship in relationships]
        context = {'is_doctor': True, 'registered_patients': registered_patients, 'form': form}
        return self.render_to_response(context)