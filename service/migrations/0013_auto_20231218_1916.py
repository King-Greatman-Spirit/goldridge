# Generated by Django 3.1 on 2023-12-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_auto_20231218_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservice',
            name='char_id',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]
