from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, PaymentForm, ScheduleForm, TreatmentForm, TestForm, UpdateForm, OTPForm, ExUpdateForm, CommentForm, AdminUpdate, AdminBMAForm, AdminNIDForm, AdminCreateForm, AdminDivisionForm, AdminDistrictForm, AdminThanaForm
from .models import Division, District, Thana, VoterID, Schedule, Treatment, Test, BMA, OTP, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from .serializers import VoterIDSerializers, BMASerializers, OTPSerializers
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from .filters import DoctorFilter, PatientFilter
from django.urls import reverse_lazy, reverse
from random import randint
from django.contrib import messages

# for payment
from django.views.decorators.csrf import csrf_exempt
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket

# Create your views here.
User = get_user_model()
def home(request):
    return render(request, 'users/dashboard/index2.html')
def reg(request):
    return render(request, 'users/dashboard/reg.html')

@login_required
def dashboard(request):
    doctors = User.objects.filter(user_type=2)
    patients = User.objects.filter(user_type=3)
    ctx = {
        'doctors' : doctors,
        'patients' : patients,
    }
    return render(request, 'users/dashboard/index.html', context=ctx)

@login_required
def login_redirect(request):
    return HttpResponseRedirect(reverse('user-profile'))

class UserRegistration(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/user_reg.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate your Account"
        messege = render_to_string('users/active_mail.html', {
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user)
        })
        to_email = form.cleaned_data['email']
        email = EmailMessage(mail_subject, messege, to=[to_email])
        email.send()
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'users/user_update.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if obj.id == self.request.user.id:
            return True

class UserExUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ExUpdateForm
    template_name = 'users/user_updateex.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if obj.id == self.request.user.id:
            return True

class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'users/doctor_update.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if obj.id == self.request.user.id:
            return True

class DoctorExUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ExUpdateForm
    template_name = 'users/doctor_updateex.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if obj.id == self.request.user.id:
            return True


class DoctorRegistration(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/doctor_reg.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = 2
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate your Account"
        messege = render_to_string('users/active_mail.html', {
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user)
        })
        to_email = form.cleaned_data['email']
        email = EmailMessage(mail_subject, messege, to=[to_email])
        email.send()
        return super().form_valid(form)


def load_districts(request):
    division_id = request.GET.get('pm_division') or request.GET.get('ps_division')
    districts = District.objects.filter(division_id=division_id).order_by('name')
    return render(request, 'users/district.html', {'districts' : districts})

def load_thanas(request):
    district_id = request.GET.get('pm_district') or request.GET.get('ps_district')
    thanas = Thana.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'users/thana.html', {'thanas' : thanas})

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    # success_url = reverse_lazy('user-profile', kwargs={'pk':})
    def get_success_url(self):
        nxt = self.request.GET.get("next", None)
        if nxt:
            return "%s" % (nxt)
        if self.request.user.user_type == 1 or self.request.user.user_type == 4 or self.request.user.user_type == 5:
            return reverse_lazy('admind')
        return reverse_lazy('user-profile', kwargs={'pk':self.request.user.id})

@login_required
def admind(request):
    doctor = User.objects.filter(user_type=2).count()
    patient = User.objects.filter(user_type=3).count()
    schedule = Schedule.objects.count()
    treatment = Treatment.objects.count()
    ctx = {
        'doctor' : doctor,
        'patient' : patient,
        'tr' : treatment,
        'sc' : schedule,
    }
    return render(request, 'users/admin/index.html', context=ctx)

def activate(request, uidb64, token):
    # try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    #     user = None
    v = default_token_generator.check_token(user, token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class PatientDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/dashboard/patient.html'

    def get_context_data(self, **kwargs):
        kwargs['prescriptions'] = Treatment.objects.filter(patient_id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

class DoctorDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/dashboard/doctor.html'

    def get_context_data(self, **kwargs):
        kwargs['schedules'] = Schedule.objects.filter(doctor_id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

@login_required
def search(request):
    doctor = User.objects.filter(user_type='2')
    docFilter = DoctorFilter(request.GET, queryset=doctor)
    doctor = docFilter.qs
    ctx = {
        'doctor' : doctor,
        'docFilter': docFilter
        }
    return render(request, 'users/dashboard/search.html', context=ctx)


class BookingCreateView(CreateView):
    form_class = PaymentForm
    template_name = 'users/dashboard/booking.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        kwargs['doctor'] = User.objects.get(id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.patient = self.request.user
        form.instance.doctor = User.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class VoterIDAPI(ListAPIView):
    serializer_class = VoterIDSerializers
    queryset = VoterID.objects.all()

class BmaAPI(ListAPIView):
    serializer_class = BMASerializers
    queryset = BMA.objects.all()

class OtpAPI(ListAPIView):
    serializer_class = OTPSerializers
    queryset = OTP.objects.all()

class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """ THis is profile class """
    model = User
    template_name = 'users/dashboard/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        kwargs['schedules'] = Schedule.objects.filter(doctor_id=self.kwargs['pk'])
        kwargs['prescriptions'] = Treatment.objects.filter(patient_id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def test_func(self):
        obj = self.get_object()
        if obj.id == self.request.user.id:
            return True



class ScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name ='users/dashboard/schedule.html'

    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def test_func(self):
        if self.request.user.user_type == 1 or self.request.user.user_type == 2:
            return True
    
    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)
        
class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name ='users/dashboard/schedule_update.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk': self.request.user.id})

    def test_func(self):
        if self.request.user.user_type == 1 or self.request.user.user_type == 2:
            return True

    def form_invalid(self, form):
        if self.request.user.user_type == 2:
            form.instance.doctor = self.request.user
        return super().form_valid(form)

class TreatmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'users/dashboard/treatment.html'

    def get_success_url(self):
        return reverse('treatment-details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.patient = User.objects.get(id=self.kwargs['pk'])
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.user_type == 1 or self.request.user.user_type == 2:
            return True

class TreatmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'users/dashboard/treatment.html'

    def get_success_url(self):
        return reverse('treatment-details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.patient = User.objects.get(id=self.kwargs['pk'])
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.user_type == 1 or self.request.user.user_type == 2:
            return True

def searchpatient(request):
    patient = User.objects.filter(user_type=3)
    pFilter = PatientFilter(request.GET, queryset=patient)
    patient = pFilter.qs
    ctx = {
        'patient' : patient,
        'pFilter': pFilter,
        }
    return render(request, 'users/dashboard/search_patient.html', context=ctx)


# class PatientProfile()
class PrescriptionView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = Treatment
    template_name = 'users/dashboard/treatment_detail.html'
    context_object_name = 'pr'
    form_class = TestForm

    def test_func(self):
        obj = self.get_object()
        if self.request.user.user_type == 1 or self.request.user.user_type == 2 or obj.patient.id == self.request.user.id:
            return True

    def get_success_url(self):
        return reverse('treatment-details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TestForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.treatment = self.object
        form.save()
        return super().form_valid(form)

class ReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'users/dashboard/test_create.html'

    def get_success_url(self):
        return reverse('treatment-details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.treatment = Treatment.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        obj = Treatment.objects.get(id=self.kwargs['pk'])
        if obj.patient.id == self.request.user.id:
            return True
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = Treatment.objects.get(id=self.kwargs['pk'])
        context['t'] = t
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'users/dashboard/comment_create.html'

    def get_success_url(self):
        t = Test.objects.get(id=self.kwargs['pk'])
        trt = t.treatment
        return reverse('treatment-details', kwargs={'pk': trt.id})

    def form_valid(self, form):
        form.instance.report = Test.objects.get(id=self.kwargs['pk'])
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = Test.objects.get(id=self.kwargs['pk'])
        context['t'] = t.treatment
        return context

class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'users/dashboard/test_update.html'

    def get_success_url(self):
        return reverse('treatment-details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.treatment = Treatment.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        obj = Treatment.objects.get(id=self.kwargs['pk'])
        if obj.patient.id == self.request.user.id or self.request.user == obj.doctor:
            return True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = Treatment.objects.get(id=self.kwargs['pk'])
        context['t'] = t
        return context

class CreateOTPView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = OTP
    form_class = OTPForm
    template_name = 'users/dashboard/otp.html'

    def form_valid(self, form):
        otp = randint(1000, 10000)
        form.instance.number = otp
        form.instance.user = self.request.user
        user = self.request.user
        mail_subject = "OTP confirmation to Update Account"
        messege = render_to_string('users/otp_mail.html', {
            'user' : user,
            'otp' : otp
        })
        to_email = self.request.user.email
        email = EmailMessage(mail_subject, messege, to=[to_email])
        email.send()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('otp-check')

    def test_func(self):
        return True

class CreateDoctorOTPView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = OTP
    form_class = OTPForm
    template_name = 'users/dashboard/otp.html'

    def form_valid(self, form):
        otp = randint(1000, 10000)
        form.instance.number = otp
        form.instance.user = self.request.user
        user = User.objects.get(id=self.kwargs['pk'])
        mail_subject = "OTP confirmation to Update Account"
        messege = render_to_string('users/otp_mail.html', {
            'user' : user,
            'otp' : otp
        })
        to_email = user.email
        email = EmailMessage(mail_subject, messege, to=[to_email])
        email.send()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('otp-check-doctor', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return True


@login_required
def alldoctor(request):
    ctx = {
        'doctors' : User.objects.filter(user_type=2)
    }
    return render(request, 'users/admin/doctors.html', context=ctx)

@login_required
def allbma(request):
    ctx = {
        'bmas' : BMA.objects.all()
    }
    return render(request, 'users/admin/bma_list.html', context=ctx)

@login_required
def alldivision(request):
    ctx = {
        'divisions' : Division.objects.all()
    }
    return render(request, 'users/admin/division_list.html', context=ctx)

@login_required
def alldistrict(request):
    ctx = {
        'districts' : District.objects.all()
    }
    return render(request, 'users/admin/district_list.html', context=ctx)

@login_required
def allthana(request):
    ctx = {
        'thanas' : Thana.objects.all()
    }
    return render(request, 'users/admin/thana_list.html', context=ctx)

@login_required
def alladmin(request):
    ctx = {
        'admins' : User.objects.filter(user_type=4) | User.objects.filter(user_type=5)
    }
    return render(request, 'users/admin/admin_list.html', context=ctx)

@login_required
def allnid(request):
    ctx = {
        'nids' : VoterID.objects.all()
    }
    return render(request, 'users/admin/nid_list.html', context=ctx)

class DoctorUpdateAdmin(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminUpdate
    template_name = 'users/admin/doctor_update.html'
    success_url = reverse_lazy('admind')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('admind')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class BMACreate(LoginRequiredMixin, CreateView):
    model = BMA
    form_class = AdminBMAForm
    template_name = 'users/admin/bma.html'
    success_url = reverse_lazy('admind')

class DivisionCreate(LoginRequiredMixin, CreateView):
    model = Division
    form_class = AdminDivisionForm
    template_name = 'users/admin/division.html'
    success_url = reverse_lazy('admind')

class DistrictCreate(LoginRequiredMixin, CreateView):
    model = District
    form_class = AdminDistrictForm
    template_name = 'users/admin/district.html'
    success_url = reverse_lazy('admind')

class ThanaCreate(LoginRequiredMixin, CreateView):
    model = Thana
    form_class = AdminThanaForm
    template_name = 'users/admin/thana.html'
    success_url = reverse_lazy('admind')

class BMAUpdate(LoginRequiredMixin, UpdateView):
    model = BMA
    form_class = AdminBMAForm
    template_name = 'users/admin/bma_update.html'
    success_url = reverse_lazy('admind')

class NIDCreate(LoginRequiredMixin, CreateView):
    model = VoterID
    form_class = AdminNIDForm
    template_name = 'users/admin/nid.html'
    success_url = reverse_lazy('admind')

class AdminCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminCreateForm
    template_name = 'users/admin/admin_create.html'
    success_url = reverse_lazy('admind')

class NIDUpdate(LoginRequiredMixin, UpdateView):
    model = VoterID
    form_class = AdminNIDForm
    template_name = 'users/admin/nid_update.html'
    success_url = reverse_lazy('admind')

class DoctorUpdateAdmin(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminUpdate
    template_name = 'users/admin/doctor_update.html'
    success_url = reverse_lazy('admind')

class PatientUpdateAdmin(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminUpdate
    template_name = 'users/admin/patient_update.html'
    success_url = reverse_lazy('admind')

@login_required
def allpatient(request):
    ctx = {
        'patients' : User.objects.filter(user_type=3)
    }
    return render(request, 'users/admin/patients.html', context=ctx)

@login_required
def check_otp(request):
    return render(request, 'users/dashboard/check_otp.html')

@login_required
def check_otp_doctor(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'users/dashboard/check_otp_doctor.html', context={'user' : user})

@login_required
def payment(request):
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='xebec5fecfeb01b53c', sslc_store_pass='xebec5fecfeb01b53c@ssl')
    status_url = request.build_absolute_uri(reverse('payment-status'))
    # print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    schedule_qs = Schedule.objects.filter()

    mypayment.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='health', product_name='doctor-apointment', num_of_item=1, shipping_method='Billing', product_profile='None')
    user = request.user
    mypayment.set_customer_info(name=f"{user.first_name} {user.last_name}", email=user.email, address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone=user.mobile)

    mypayment.set_shipping_info(shipping_to=f"{user.first_name} {user.last_name}", address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')

    response_data = mypayment.init_payment()
    print(response_data)

    return redirect(response_data['GatewayPageURL'])
    # return render(request, 'users/dashboard/payment.html')

@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        val_id = payment_data['val_id']
        tran_id = payment_data['tran_id']
        bank_tran_id = payment_data['bank_tran_id']

    if status == 'VALID':
        messages.success(request, f"Your payment completed Succesfully.")
    elif status == 'FAILED':
        messages.warning(request, f"Your payment failed! Please Try again.")
    return render(request, "users/dashboard/complete.html")