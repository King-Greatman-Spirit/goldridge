# Generated by Django 3.1 on 2023-11-30 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20231130_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subservice',
            options={'ordering': ['-approval', 'created_date'], 'verbose_name': 'SubService', 'verbose_name_plural': 'SubServices'},
        ),
    ]
