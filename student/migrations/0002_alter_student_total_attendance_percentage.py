# Generated by Django 4.0.3 on 2022-04-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='total_attendance_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
