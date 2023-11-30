# Generated by Django 4.2.7 on 2023-11-21 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org', models.CharField(max_length=70)),
                ('order_key', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'clients',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DecimalNumbers',
            fields=[
                ('mkcb', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('field_name', models.CharField(blank=True, db_column='_name', max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'decimal_numbers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
                ('user_name', models.CharField(blank=True, max_length=32, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='showdb.clients')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('serial_number', models.IntegerField(primary_key=True, serialize=False)),
                ('mkcb', models.CharField(max_length=25)),
                ('date_out', models.DateField(blank=True, null=True)),
                ('location', models.CharField(max_length=255)),
                ('description_field', models.CharField(blank=True, db_column='description_', max_length=50, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='showdb.clients')),
            ],
            options={
                'db_table': 'stations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('serial_number', models.IntegerField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=80)),
                ('mkcb', models.CharField(max_length=25)),
                ('date_out', models.DateField(blank=True, null=True)),
                ('location', models.CharField(max_length=255)),
                ('description_field', models.CharField(blank=True, db_column='description_', max_length=50, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='showdb.clients')),
                ('station_number', models.ForeignKey(blank=True, db_column='station_number', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='showdb.stations')),
            ],
            options={
                'db_table': 'devices',
                'managed': True,
            },
        ),
    ]
