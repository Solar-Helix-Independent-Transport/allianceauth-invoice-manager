# Generated by Django 4.0.2 on 2022-08-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_nooverduefilter'),
    ]

    operations = [
        migrations.AddField(
            model_name='nooverduefilter',
            name='swap_logic',
            field=models.BooleanField(default=False),
        ),
    ]
