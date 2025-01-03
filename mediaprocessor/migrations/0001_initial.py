# Generated by Django 5.1.1 on 2025-01-02 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('file_type', models.CharField(choices=[('image', 'Image'), ('pdf', 'PDF')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
