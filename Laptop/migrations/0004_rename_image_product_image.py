# Generated by Django 5.0.2 on 2024-03-14 11:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Laptop", "0003_alter_laptop_full_processor_details"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Image",
            new_name="Product_image",
        ),
    ]
