# Generated by Django 4.0.2 on 2022-03-06 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_percentage_attendance_student_total_attendance_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='taught_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.teacher'),
        ),
    ]
