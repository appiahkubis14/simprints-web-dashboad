# Generated by Django 5.1.4 on 2025-04-02 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0010_remove_districts_region_districts_reg_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="districts",
            old_name="reg_name",
            new_name="region",
        ),
        migrations.RenameField(
            model_name="region",
            old_name="region",
            new_name="reg_name",
        ),
    ]
