# Generated by Django 4.2.17 on 2024-12-24 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0009_alter_qrcode_options"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="event",
            name="unique_event_name_per_timerange_per_club",
        ),
        migrations.RenameField(
            model_name="event",
            old_name="event_end",
            new_name="end_at",
        ),
        migrations.RenameField(
            model_name="event",
            old_name="event_start",
            new_name="start_at",
        ),
        migrations.AddConstraint(
            model_name="event",
            constraint=models.UniqueConstraint(
                fields=("start_at", "end_at", "club", "name"),
                name="unique_event_name_per_timerange_per_club",
            ),
        ),
    ]
