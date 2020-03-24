# Generated by Django 3.0.3 on 2020-03-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='stock_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='stock_name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='ticker',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
