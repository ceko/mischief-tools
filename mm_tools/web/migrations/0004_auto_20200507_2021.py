# Generated by Django 3.0.6 on 2020-05-07 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mm_tools_web', '0003_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priority',
            options={'permissions': [('can_export_priorities', 'Can export priorities')]},
        ),
    ]
