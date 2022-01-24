# Generated by Django 3.2 on 2022-01-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybooksite', '0011_auto_20220111_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='book',
        ),
        migrations.AddField(
            model_name='category',
            name='book',
            field=models.ManyToManyField(blank=True, null=True, to='mybooksite.Book'),
        ),
    ]
