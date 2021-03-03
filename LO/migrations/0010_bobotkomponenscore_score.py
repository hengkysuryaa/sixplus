# Generated by Django 3.1.6 on 2021-02-26 08:25

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mahasiswa', '0002_auto_20210223_1130'),
        ('LO', '0009_auto_20210223_1130'),
    ]

    operations = [
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
                ('nim', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Mahasiswa.student')),
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
