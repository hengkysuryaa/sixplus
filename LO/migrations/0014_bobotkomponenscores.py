# Generated by Django 3.1.6 on 2021-04-22 13:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LO', '0013_auto_20210422_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='BobotKomponenScores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bobot', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), size=None)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LO.section')),
            ],
        ),
    ]
