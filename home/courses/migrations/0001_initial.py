# Generated by Django 5.1.1 on 2024-10-02 03:23

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to=courses.models.handle_upload)),
                ('access', models.CharField(choices=[('any', 'Anyone'), ('email', 'Email required')], default='any', max_length=15)),
                ('status', models.CharField(choices=[('pub', 'Published'), ('cs', 'Comming soon'), ('dr', 'Draft')], default='dr', max_length=15)),
            ],
        ),
    ]