# Generated by Django 3.1.1 on 2020-09-17 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inkind', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
    ]
