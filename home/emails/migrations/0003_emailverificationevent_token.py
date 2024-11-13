# Generated by Django 5.1.1 on 2024-11-06 07:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverificationevent',
            name='token',
            field=models.UUIDField(default=uuid.uuid1),
        ),
    ]
