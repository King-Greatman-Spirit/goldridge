# Generated by Django 3.1 on 2023-11-03 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('website_address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=50)),
                ('address_line_1', models.CharField(max_length=50)),
                ('address_line_2', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=12)),
                ('country', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('logo', models.ImageField(upload_to='photos/logos')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_client', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='CompanyOverview',
            fields=[
                ('mission', models.TextField(blank=True, max_length=500)),
                ('vision', models.TextField(blank=True, max_length=500)),
                ('goal', models.TextField(blank=True, max_length=500)),
                ('business_overview', models.TextField(blank=True, max_length=500)),
                ('competive_advantage', models.TextField(blank=True, max_length=500)),
                ('id', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
    ]
