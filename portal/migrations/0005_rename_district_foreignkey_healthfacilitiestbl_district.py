# Generated by Django 5.1.4 on 2025-03-31 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0004_rename_community_communitytbl_community_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="healthfacilitiestbl",
            old_name="district_foreignkey",
            new_name="district",
        ),
    ]
