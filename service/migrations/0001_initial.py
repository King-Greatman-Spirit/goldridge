# Generated by Django 3.1 on 2023-11-03 09:48

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('service_description', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(upload_to='photos/services')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=100)),
                ('client_full_name', models.CharField(default=True, max_length=100)),
                ('client_location', models.CharField(default=True, max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('service', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='company', chained_model_field='company', default=None, on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='ServiceProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=50)),
                ('process_description', models.TextField(max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/service_process')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('service', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='company', chained_model_field='company', default=None, on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
            options={
                'verbose_name': 'ServiceProcess',
                'verbose_name_plural': 'Service Processes',
            },
        ),
    ]
