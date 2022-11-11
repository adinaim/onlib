# Generated by Django 4.1.3 on 2022-11-08 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_rename_genres_book_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
        migrations.AddField(
            model_name='book',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
