# Generated by Django 4.1.3 on 2022-11-08 05:00

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('order_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('books', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=80), size=None)),
                ('user', models.ManyToManyField(related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
