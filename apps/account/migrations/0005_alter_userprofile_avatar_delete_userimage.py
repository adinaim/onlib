# Generated by Django 4.1.3 on 2022-11-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_userprofile_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='media'),
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
    ]
