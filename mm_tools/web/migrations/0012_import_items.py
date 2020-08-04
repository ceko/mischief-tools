from django.db import migrations
import os
import csv


def import_items(apps, schema_editor):
    csv_path = os.path.join(os.path.dirname(__file__), 'loot-phase-5.csv')

    item_model = apps.get_model('mm_tools_web', 'Item')
    items = []
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            items.append(item_model(
                zone=row[0],
                name=row[1],
                type=row[2],
                slot=row[3]
            ))
    item_model.objects.bulk_create(items)


def delete_items(apps, schema_editor):
    item_model = apps.get_model('mm_tools_web', 'Item')
    item_model.objects.filter(
        zone__in=['AQ40', 'AQ20']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mm_tools_web', '0011_auto_20200804_1027'),
    ]

    operations = [
        migrations.RunPython(import_items, delete_items),
    ]
