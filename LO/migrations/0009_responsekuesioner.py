# Generated by Django 3.1.6 on 2021-04-10 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LO', '0008_merge_20210408_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseKuesioner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kuesioner1', models.IntegerField()),
                ('Kuesioner2', models.IntegerField()),
                ('Kuesioner3', models.IntegerField()),
                ('Kuesioner4', models.IntegerField()),
                ('Kuesioner5', models.IntegerField()),
                ('Kuesioner6', models.IntegerField()),
                ('Kuesioner7', models.IntegerField()),
                ('Kuesioner8', models.IntegerField()),
                ('Kuesioner9', models.IntegerField()),
                ('Kuesioner10', models.IntegerField()),
                ('Kuesioner11', models.IntegerField()),
                ('Kuesioner12', models.IntegerField()),
                ('takes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LO.takes')),
            ],
        ),
    ]
