# Generated by Django 5.1.1 on 2024-10-06 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='public_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]