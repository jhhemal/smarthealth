# Generated by Django 3.1.4 on 2020-12-28 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20201228_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatment',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
