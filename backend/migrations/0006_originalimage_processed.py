# Generated by Django 4.2.7 on 2023-12-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_imagesegment_delete_imagesegments'),
    ]

    operations = [
        migrations.AddField(
            model_name='originalimage',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
