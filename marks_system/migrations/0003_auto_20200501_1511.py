# Generated by Django 3.0.5 on 2020-05-01 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marks_system', '0002_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='hod',
            new_name='assign_hod',
        ),
    ]
