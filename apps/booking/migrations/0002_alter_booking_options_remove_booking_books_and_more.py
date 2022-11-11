# Generated by Django 4.1.3 on 2022-11-08 08:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_remove_book_status_book_is_available_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['created_at'], 'verbose_name': 'Бронь', 'verbose_name_plural': 'Брони'},
        ),
        migrations.RemoveField(
            model_name='booking',
            name='books',
        ),
        migrations.AddField(
            model_name='booking',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_book', to='book.book'),
        ),
        migrations.AddField(
            model_name='booking',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 11, 8, 8, 39, 58, 981389, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 22, 14, 39, 48, 678372)),
        ),
        migrations.AddField(
            model_name='booking',
            name='date_max_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 22, 14, 39, 48, 678382)),
        ),
        migrations.AddField(
            model_name='booking',
            name='rent_status',
            field=models.CharField(choices=[(1, 'Взял_а'), (0, 'Вернул_а'), (-1, 'Должен_на')], default=1, max_length=10),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
