# Generated by Django 5.1.7 on 2025-05-20 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('patient', 'Patient'), ('kine', 'Kinésithérapeute'), ('vendor', 'Vendeur'), ('admin', 'Administrateur')], default='patient', max_length=20),
        ),
    ]
