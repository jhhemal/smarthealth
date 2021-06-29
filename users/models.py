from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def upload_directory(instance, filename):
    return f"report/{instance.treatment.patient.sn}/{filename}"

class Division(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Thana(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'doctor'),
        (3, 'patients'),
        (4, 'doctor admin'),
        (5, 'patient admin'),
    )
    VERIFY_STATUS = (
        ('yes', 'yes'),
        ('no', 'no')
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    BG_CHOICES = (
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    DESIGNATION_CHOICES = (
        ('Professor', 'Professor'), 
	    ('Associate Professor', 'Associate Professor'),
	    ('Assistant Professor', 'Assistant Professor'),
        ('Consultant', 'Consultant'),
	    ('Registras', 'Registras'),
	    ('Assistant Registras', 'Assistant Registras'),
	    ('IMO', 'IMO'),
        ('EMO', 'EMO'),
        ('RMO', 'RMO'),
        ('HMO', 'HMO'),
        ('Other', 'Other')
    )

    username = None
    sn = models.CharField(verbose_name='Serial Number', max_length=12, unique=True, error_messages={'required': 'Your Name is Required'})
    pm_division = models.ForeignKey(Division, verbose_name='Division', related_name='pm_division', on_delete=models.DO_NOTHING, null=True, blank=True)
    pm_district = models.ForeignKey(District, verbose_name='District', related_name='pm_district', on_delete=models.DO_NOTHING, null=True, blank=True)
    pm_thana = models.ForeignKey(Thana, verbose_name='Thana', related_name='pm_thana', on_delete=models.DO_NOTHING, null=True, blank=True)
    ps_division = models.ForeignKey(Division, verbose_name='Division', related_name='ps_division', on_delete=models.DO_NOTHING, null=True, blank=True)
    ps_district = models.ForeignKey(District, verbose_name='District', related_name='ps_district', on_delete=models.DO_NOTHING, null=True, blank=True)
    ps_thana = models.ForeignKey(Thana, verbose_name='Thana', related_name='ps_thana', on_delete=models.DO_NOTHING, null=True, blank=True)
    pm_village = models.CharField(verbose_name='Village',max_length=50, null=True, blank=True)
    ps_village = models.CharField(verbose_name='Village',max_length=50, null=True, blank=True)
    pm_union = models.CharField(verbose_name='Union',max_length=50, null=True, blank=True)
    ps_union = models.CharField(verbose_name='Union',max_length=50, null=True, blank=True)
    pm_ward = models.CharField(verbose_name='Ward',max_length=50, null=True, blank=True)
    ps_ward = models.CharField(verbose_name='Ward',max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='users', null=True, blank=True)
    verified = models.CharField(max_length=10, choices=VERIFY_STATUS, null=True, default='no')
    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=3, blank=True, null=True)
    mobile = models.CharField(verbose_name='Mobile Number', max_length=11, blank=True)
    payment = models.CharField(verbose_name='Payment Number', max_length=11, null=True, blank=True)
    nid = models.CharField(verbose_name='National ID', max_length=10, unique=True, blank=True, null=True)
    bma = models.CharField(verbose_name='BMA Code', max_length=20, unique=True, blank=True, null=True)
    institute = models.CharField(verbose_name='Institute', max_length=100, blank=True, null=True)
    designation = models.CharField(verbose_name='Designation', max_length=50, choices=DESIGNATION_CHOICES, blank=True, null=True)
    specialist = models.ForeignKey(Speciality, verbose_name='Specialist', blank=True, null=True, on_delete=models.CASCADE)
    father_name = models.CharField(verbose_name='Father\'s name', max_length=25, null=True, blank=True)
    mother_name = models.CharField(verbose_name='Mother\'s name', max_length=25, null=True, blank=True)
    father_mobile = models.CharField(verbose_name='Father\'s Mobile', max_length=11, null=True, blank=True)
    mother_mobile = models.CharField(verbose_name='Mother\'s Mobile', max_length=11, null=True, blank=True)
    bg = models.CharField(verbose_name='Blood Group', max_length=11, choices=BG_CHOICES, null=True, blank=True)
    gender = models.CharField(verbose_name='Select Gender', max_length=11, choices=GENDER_CHOICES, null=True, blank=True)


    USERNAME_FIELD = 'sn'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.sn

class Days(models.Model):
    day = models.CharField(verbose_name='Day', max_length=20)

    def __str__(self):
        return self.day

class Schedule(models.Model):
    DAYS = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednessday', 'Wednessday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('bKash', 'bKash'),
        ('Rocket', 'Rocket'),
        ('Nagad', 'Nagad'),
        ('DBBL', 'DBBL'),
        ('Skrill', 'Skrill'),
        ('Aqua', 'Aqua')
    )

    name = models.CharField(verbose_name='Place', max_length=200, null=True)
    wkfrom = models.CharField(verbose_name='Start Day', max_length=15, choices=DAYS, null=True)
    wkto = models.CharField(verbose_name='End day', max_length=15, choices=DAYS, null=True)
    # days = models.CharField(verbose_name='Lol', max_length=20, null=True)
    days = models.ManyToManyField(to=Days, related_name='days', verbose_name='Select Days', null=True)
    pm_method = models.CharField(verbose_name="Payment Method", choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, max_length=6)
    timefrom = models.TimeField(verbose_name='Time From', null=True)
    timeto = models.TimeField(verbose_name='Time To', null=True)
    fee = models.CharField(verbose_name='Consultaiton Fee', max_length=20)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class VoterID(models.Model):
    voter_id = models.CharField(max_length=10)

    def __str__(self):
        return self.voter_id

class BMA(models.Model):
    code = models.CharField(max_length=10)
    institute = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Treatment(models.Model):
    patient = models.ForeignKey(User, related_name='treatment_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='treatment_doctor', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    prescription = models.TextField()

    def __str__(self):
        return self.title

class Test(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True, verbose_name="Report Title")
    reportimg = models.ImageField(upload_to=upload_directory, verbose_name="Upload Report Scanned Image", default='default.jpg', blank=True)
    reportpdf = models.FileField(upload_to=upload_directory, verbose_name="Upload Report Scanned PDF", default='default.pdf', blank=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    report = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Write your comments')
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.report.title}'s Comment"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('bKash', 'bKash'),
        ('Rocket', 'Rocket'),
        ('Nagad', 'Nagad'),
        ('DBBL', 'DBBL'),
        ('Skrill', 'Skrill'),
        ('Aqua', 'Aqua')
    )

    STATUS_OPTION_CHOICES = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending')
    )

    trxnid = models.CharField(max_length=50)
    amount = models.FloatField('Paid Amount', default=0)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHOD_CHOICES, default='bKash')
    payment_date = models.DateField(null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(User, related_name='booking_doctor', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_OPTION_CHOICES, default='Pending', null=True, blank=True)

    def __str__(self):
        return self.trxnid

class OTP(models.Model):
    number = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.number



