# Generated by Django 4.2.7 on 2023-12-04 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_rename_batch_uploadbatch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSegments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImageSegments', models.ImageField(upload_to='segments/')),
                ('original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imageSegments', to='backend.image')),
            ],
        ),
    ]
