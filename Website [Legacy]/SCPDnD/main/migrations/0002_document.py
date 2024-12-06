# Generated by Django 4.2.2 on 2023-06-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('upload_date', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('file_link', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'document',
                'managed': False,
            },
        ),
    ]