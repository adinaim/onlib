# Generated by Django 4.1.3 on 2022-11-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userprofile_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
