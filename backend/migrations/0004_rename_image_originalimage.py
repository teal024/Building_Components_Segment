# Generated by Django 4.2.7 on 2023-12-04 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_imagesegments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='OriginalImage',
        ),
    ]
