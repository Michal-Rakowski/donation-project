# Generated by Django 3.1.1 on 2020-09-26 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkind', '0003_auto_20200924_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='status_change',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with such email already exists.'}, max_length=255, unique=True, verbose_name='Email adres'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='Imie'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='Nazwisko'),
        ),
    ]
