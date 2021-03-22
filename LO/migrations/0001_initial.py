# Generated by Django 3.1.6 on 2021-03-22 11:28

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Mahasiswa', '0002_auto_20210223_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=6, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('dept_name', models.CharField(max_length=10)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uts1', models.IntegerField()),
                ('uts2', models.IntegerField()),
                ('uas', models.IntegerField()),
                ('kuis', models.IntegerField()),
                ('tutorial', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LO.course')),
                ('nim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mahasiswa.student')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseKerjasama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kontribusi', models.IntegerField()),
                ('PemecahanMasalah', models.IntegerField()),
                ('Sikap', models.IntegerField()),
                ('FokusTerhadapTugas', models.IntegerField()),
                ('BekerjaDenganOrangLain', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LO.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mahasiswa.student')),
            ],
        ),
        migrations.CreateModel(
            name='LO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lo_a', models.CharField(max_length=1)),
                ('lo_b', models.CharField(max_length=1)),
                ('lo_c', models.CharField(max_length=1)),
                ('lo_d', models.CharField(max_length=1)),
                ('lo_e', models.CharField(max_length=1)),
                ('lo_f', models.CharField(max_length=1)),
                ('lo_g', models.CharField(max_length=1)),
                ('course_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='LO.course')),
            ],
        ),
        migrations.CreateModel(
            name='BobotKomponenScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uts1', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('uts2', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('uas', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('kuis', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('tutorial', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LO.course')),
            ],
        ),
    ]
