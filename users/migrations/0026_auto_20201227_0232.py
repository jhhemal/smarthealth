# Generated by Django 3.1.4 on 2020-12-26 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_user_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('prescription', models.TextField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.ImageField(blank=True, default='sample.jpg', null=True, upload_to=users.models.upload_directory)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
