# Generated by Django 5.1.5 on 2025-01-26 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_releases_publication_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releases',
            name='release_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата выхода'),
        ),
    ]
