from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Division, District, Thana, Payment, Schedule, Treatment, Test, OTP, Comment, VoterID, BMA, Days
User = get_user_model()
from tinymce.widgets import TinyMCE

class DateInput(forms.DateInput):
    input_type = 'date'

class AdminUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class AdminBMAForm(forms.ModelForm):
    class Meta:
        model = BMA
        fields = '__all__'
    
class AdminDistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'
class AdminDivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = '__all__'
class AdminThanaForm(forms.ModelForm):
    class Meta:
        model = Thana
        fields = '__all__'

class AdminNIDForm(forms.ModelForm):
    class Meta:
        model = VoterID
        fields = '__all__'

class AdminCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['sn', 'first_name', 'last_name', 'email', 'mobile', 'user_type', 'password1', 'password2']



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'sn', 'birthday', 'nid', 'verified', 'mobile', 'bma', 'institute', 'image', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'bg', 'gender', 'pm_division', 'pm_district', 'pm_thana', 'ps_division', 'ps_district', 'ps_thana', 'pm_union', 'ps_union', 'pm_ward', 'ps_ward', 'pm_village', 'ps_village', 'payment', 'specialist', 'designation', 'password1', 'password2']

        widgets = {
            'birthday' : DateInput(),
            'sn' : forms.TextInput(attrs={
                'placeholder' : 'Auto generated',
                'readonly' : True
            }),
            'verified' : forms.TextInput(attrs={
                'hidden' : True
            }),
            'institute' : forms.TextInput(attrs={
                'hidden' : True
            }),
            'pm_ward' : forms.NumberInput(attrs={}),
            'ps_ward' : forms.NumberInput(attrs={}),
        }
        labels = {
            'verified' : "",
            'institute' : "",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pm_district'].queryset = Division.objects.none()
        self.fields['pm_thana'].queryset = District.objects.none()
        self.fields['ps_district'].queryset = Division.objects.none()
        self.fields['ps_thana'].queryset = District.objects.none()
        self.fields['verified'].required = False
        self.fields['institute'].required = False

        if 'pm_division' in self.data:
            try:
                division_id = int(self.data.get('pm_division'))
                self.fields['pm_district'].queryset = District.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['pm_district'].queryset = self.instance.pm_division.pm_distric_set.order_by('name')

        if 'pm_district' in self.data:
            try:
                district_id = int(self.data.get('pm_district'))
                self.fields['pm_thana'].queryset = Thana.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['pm_thana'].queryset = self.instance.pm_district.pm_thana_set.order_by('name')
        
        if 'ps_division' in self.data:
            try:
                division_id = int(self.data.get('ps_division'))
                self.fields['ps_district'].queryset = District.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ps_district'].queryset = self.instance.ps_division.ps_division_set.order_by('name')

        if 'ps_district' in self.data:
            try:
                district_id = int(self.data.get('ps_district'))
                self.fields['ps_thana'].queryset = Thana.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ps_thana'].queryset = self.instance.ps_district.ps_thana_set.order_by('name')

class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'sn', 'birthday', 'nid', 'mobile', 'bma', 'institute', 'image', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'bg', 'gender', 'pm_division', 'pm_district', 'pm_thana', 'ps_division', 'ps_district', 'ps_thana', 'pm_union', 'ps_union', 'pm_ward', 'ps_ward', 'pm_village', 'ps_village', 'payment', 'specialist', 'designation',]

        widgets = {
            'birthday' : DateInput(attrs={
                'readonly' : True
            }),
            'first_name' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'last_name' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'nid' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'email' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'bma' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'mobile' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'institute' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'specialist' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'designation' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'sn' : forms.TextInput(attrs={
                'placeholder' : 'Auto generated',
                'readonly' : True
            }),
            # 'verified' : forms.TextInput(attrs={
            #     'hidden' : True
            # }),
            'institute' : forms.TextInput(attrs={
                'hidden' : True
            }),
        }
        labels = {
            # 'verified' : "",
            'institute' : "",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pm_district'].queryset = Division.objects.none()
        # self.fields['pm_thana'].queryset = District.objects.none()
        # self.fields['ps_district'].queryset = Division.objects.none()
        # self.fields['ps_thana'].queryset = District.objects.none()
        # self.fields['verified'].required = False
        self.fields['institute'].required = False

class ExUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'sn', 'birthday', 'nid', 'mobile', 'bma', 'institute', 'image', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'bg', 'gender', 'pm_division', 'pm_district', 'pm_thana', 'ps_division', 'ps_district', 'ps_thana', 'pm_union', 'ps_union', 'pm_ward', 'ps_ward', 'pm_village', 'ps_village', 'payment', 'specialist', 'designation',]

        widgets = {
            'birthday' : DateInput(attrs={
            }),
            'nid' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'bma' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'institute' : forms.TextInput(attrs={
                'readonly' : True
            }),
            'sn' : forms.TextInput(attrs={
                'placeholder' : 'Auto generated',
                'readonly' : True
            }),
            # 'verified' : forms.TextInput(attrs={
            #     'hidden' : True
            # }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pm_district'].queryset = Division.objects.none()
        # self.fields['pm_thana'].queryset = District.objects.none()
        # self.fields['ps_district'].queryset = Division.objects.none()
        # self.fields['ps_thana'].queryset = District.objects.none()
        # self.fields['verified'].required = False
        self.fields['institute'].required = False

       

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['doctor', 'trxnid', 'payment_method', 'amount', 'payment_date', 'status']

        widgets = {
            'trxnid' : forms.TextInput(attrs={
                'placeholder' : 'Enter your TransactionID here.'
            }),
            'amount' : forms.NumberInput(attrs={
                'placeholder' : 'Enter the amount you have paid'
            }),
            'payment_date' : forms.TextInput(attrs={
                'type' : 'date'
            })
        }
        labels = {
            'booking' : 'Select the Booking',
            'trxnid' : 'TRansaction ID',
            'payment_method' : 'Select Payment method',
            'payment_date' : 'Select Payment date'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label = 'Payment Method'
        self.fields['status'].empty_label = 'Select Status'
        self.fields['payment_method'].required = False
        # self.fields['doctor'].empty_label = 'Select Doctor'
        # self.fields['doctor'].required = False
        
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'days', 'timefrom', 'timeto', 'fee', 'pm_method']


        widgets = {
            'timefrom' : forms.TextInput(attrs={
                'type' : 'time',
            }),
            'timeto' : forms.TextInput(attrs={
                'type' : 'time',
            }),
            'days' : forms.CheckboxSelectMultiple(),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['title', 'prescription']

        widgets = {
            'prescription' : TinyMCE(),
        }
        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'reportimg', 'reportpdf']

        widgets = {
            'reportimg' : forms.FileInput(),
            'reportpdf' : forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['reportimg'].required = True

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ['number']

        labels = {
            'number' : "",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment' : TinyMCE(),
        }

class DaysForm(forms.ModelForm):
    class Meta:
        model = Days
        fields = ['day']
