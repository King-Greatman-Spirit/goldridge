# Generated by Django 3.1 on 2023-11-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20231122_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservice',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subservice',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
    ]
