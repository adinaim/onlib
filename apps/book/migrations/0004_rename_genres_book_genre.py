# Generated by Django 4.1.3 on 2022-11-08 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_rename_genre_book_genres_alter_book_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='genres',
            new_name='genre',
        ),
    ]
