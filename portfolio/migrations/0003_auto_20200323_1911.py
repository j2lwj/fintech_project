# Generated by Django 3.0.3 on 2020-03-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20200323_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='stock_id',
            field=models.IntegerField(),
        ),
    ]
