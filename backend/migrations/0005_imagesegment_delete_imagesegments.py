# Generated by Django 4.2.7 on 2023-12-04 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_rename_image_originalimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSegment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segment_source', models.ImageField(upload_to='segments/')),
                ('original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imageSegments', to='backend.originalimage')),
            ],
        ),
        migrations.DeleteModel(
            name='ImageSegments',
        ),
    ]
