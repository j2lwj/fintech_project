# Generated by Django 3.0.4 on 2020-04-15 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_remove_stocks_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='stock_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='stock_name',
            field=models.CharField(max_length=191, unique=True),
        ),
    ]
