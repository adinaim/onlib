# Generated by Django 4.1.3 on 2022-11-07 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
