# Generated by Django 3.1 on 2023-11-30 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20231122_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='subservicetype',
            name='abbr',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subservicetype',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
