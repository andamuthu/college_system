# Generated by Django 3.0.5 on 2020-05-01 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marks_system', '0008_auto_20200501_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsmarks',
            name='department',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='marks_system.Department'),
        ),
    ]
