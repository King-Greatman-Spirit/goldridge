# Generated by Django 3.1 on 2023-12-19 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_auto_20231218_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservice',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
