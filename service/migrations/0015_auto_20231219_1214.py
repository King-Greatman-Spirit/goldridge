# Generated by Django 3.1 on 2023-12-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_auto_20231219_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservice',
            name='char_id',
            field=models.CharField(blank=True, editable=False, max_length=32, null=True, unique=True),
        ),
    ]
