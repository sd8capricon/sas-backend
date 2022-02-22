# Generated by Django 4.0.2 on 2022-02-22 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('roll_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=20)),
                ('enrolled_students', models.ManyToManyField(null=True, to='api.Student')),
                ('taught_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('student_status', models.BooleanField(null=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.course')),
                ('student_roll_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.student')),
            ],
        ),
    ]