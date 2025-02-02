# Generated by Django 4.2.16 on 2024-11-19 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpreference',
            name='preferred_contact_method',
            field=models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], default='email', max_length=20),
        ),
        migrations.AddField(
            model_name='customerpreference',
            name='receive_notifications',
            field=models.BooleanField(default=True),
        ),
    ]
