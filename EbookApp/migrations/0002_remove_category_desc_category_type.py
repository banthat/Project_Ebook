# Generated by Django 4.1.7 on 2023-02-16 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EbookApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='desc',
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(default='', max_length=50),
        ),
    ]
