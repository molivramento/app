# Generated by Django 4.1.5 on 2023-04-20 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='expires_at',
        ),
    ]
