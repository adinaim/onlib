# Generated by Django 4.1.3 on 2022-11-09 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_date_ended_alter_booking_date_max_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 23, 15, 20, 20, 995068)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_max_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 23, 15, 20, 20, 995078)),
        ),
    ]
