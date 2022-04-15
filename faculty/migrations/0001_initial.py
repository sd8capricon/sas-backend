# Generated by Django 4.0.3 on 2022-04-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('teacher_id', models.IntegerField(primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(choices=[('Admin', 'Admin'), ('Faculty', 'Faculty')], default='Faculty', max_length=7)),
            ],
        ),
    ]
