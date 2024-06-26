# Generated by Django 5.0.6 on 2024-05-28 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_team_members_alter_tournament_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='registration_deadline',
            field=models.DateField(default=datetime.datetime(2024, 6, 4, 9, 34, 50, 572014, tzinfo=datetime.timezone.utc)),
        ),
    ]
