# Generated by Django 4.2.7 on 2023-12-12 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showdb', '0002_files_alter_clients_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filebond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snumber', models.CharField(max_length=25)),
                ('uuid', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'filebond',
                'managed': False,
            },
        ),
    ]