# Generated by Django 3.0.3 on 2020-03-22 13:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='stocks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), default=list, size=None),
        ),
    ]
