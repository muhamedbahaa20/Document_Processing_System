# Generated by Django 5.1.1 on 2025-01-03 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaprocessor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='file_name',
            field=models.CharField(max_length=10, null=True),
        ),
    ]