# Generated by Django 5.1.4 on 2025-04-02 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0011_rename_reg_name_districts_region_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="districts",
            name="district_2",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
