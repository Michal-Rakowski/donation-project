# Generated by Django 3.1.1 on 2020-09-23 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inkind', '0002_remove_customuser_is_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Użytkownik', 'verbose_name_plural': 'Użytkownicy'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'verbose_name': 'Darowizna', 'verbose_name_plural': 'Przekazane Dary'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Organizacja', 'verbose_name_plural': 'Zaufane Organizację'},
        ),
        migrations.AddField(
            model_name='donation',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inkind.institution'),
        ),
    ]
