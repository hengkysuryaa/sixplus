# Generated by Django 3.1.6 on 2021-05-07 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LO', '0015_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='takes',
            name='final_score',
            field=models.CharField(default='-', max_length=3),
        ),
    ]
