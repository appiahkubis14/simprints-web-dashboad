# Generated by Django 5.1.4 on 2025-03-31 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0003_alter_districts_reg_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="communitytbl",
            old_name="Community",
            new_name="community",
        ),
        migrations.AddField(
            model_name="communitytbl",
            name="community_leader_contact",
            field=models.CharField(blank=True, default="Not available", max_length=24),
        ),
        migrations.AddField(
            model_name="communitytbl",
            name="community_leader_name",
            field=models.CharField(blank=True, max_length=24),
        ),
    ]
