# Generated by Django 3.0.5 on 2020-05-01 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marks_system', '0009_auto_20200501_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsmarks',
            name='department',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='marks_system.Department'),
        ),
    ]
