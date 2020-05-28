import json
from mm_tools.web.models import Raid, Character, Boss, BossFight
from datetime import datetime, timedelta, timezone
from django.utils.timezone import make_aware


def import_reports(reports):
    report_ids = [r['id'] for r in reports]
    existing_report_ids = Raid.objects.filter(
        warcraft_logs_id__in=report_ids
    ).values_list('warcraft_logs_id', flat=True)

    new_reports = []
    for report in reports:
        if report['id'] in existing_report_ids:
            continue

        start = datetime.utcfromtimestamp(
            report['start']/1000).replace(tzinfo=timezone.utc)

        end = datetime.utcfromtimestamp(
            report['end']/1000).replace(tzinfo=timezone.utc)
        new_reports.append(
            Raid(
                warcraft_logs_id=report['id'],
                title=report['title'],
                started_on=start,
                ended_on=end,
                zone=report['zone']
            )
        )

    Raid.objects.bulk_create(new_reports)


def import_report(raid, report):
    characters = import_characters(report['exportedCharacters'])
    bosses = import_bosses(report['enemies'])
    fights = import_fights(raid, bosses, report['fights'])
    attendance = import_attendance(characters, fights, report['friendlies'])


def import_attendance(characters, fights, records):
    character_dict = {c.name: c for c in characters}
    fight_dict = {f.fight_index: f for f in fights}

    # fight id: characters
    fight_attendance = {f.fight_index: [] for f in fights}

    for record in records:
        character = character_dict.get(record['name'])
        if not character:
            continue

        for fight in record['fights']:
            if fight['id'] in fight_attendance:
                fight_attendance[fight['id']].append(character)

    for idx, fight in fight_dict.items():
        attendance = fight_attendance[idx]
        fight.attendance.set(attendance)

    return fight_dict


def import_bosses(records):
    bosses = [r for r in records if r['type'] == 'Boss']
    boss_ids = [i['guid'] for i in bosses]
    existing_ids = Boss.objects.filter(
        warcraft_logs_id__in=boss_ids
    ).values_list('warcraft_logs_id', flat=True)

    new_records = []
    guids = []
    for record in bosses:
        if str(record['guid']) in existing_ids:
            continue

        if record['guid'] in guids:
            continue

        guids.append(record['guid'])

        new_records.append(
            Boss(
                warcraft_logs_id=record['guid'],
                name=record['name']
            )
        )

    Boss.objects.bulk_create(new_records)
    return Boss.objects.filter(warcraft_logs_id__in=boss_ids)


def import_fights(raid, bosses, records):
    boss_fights = [f for f in records if 'boss' in f and f['boss'] > 0]
    boss_indexes = [i['id'] for i in boss_fights]
    existing_ids = BossFight.objects.filter(
        fight_index__in=boss_indexes,
        raid=raid
    ).values_list('fight_index', flat=True)

    new_records = []
    for record in boss_fights:
        if record['id'] in existing_ids:
            continue
        boss = [b for b in bosses if b.name == record['name']]
        if boss:
            new_records.append(
                BossFight(
                    boss=[b for b in bosses if b.name == record['name']][0],
                    fight_index=record['id'],
                    raid=raid,
                    kill=record['kill'],
                    started_on=(
                        raid.started_on +
                        timedelta(milliseconds=record['start_time'])
                    ),
                    ended_on=(
                        raid.started_on +
                        timedelta(milliseconds=record['end_time'])
                    )
                )
            )
        else:
            print(record)

    BossFight.objects.bulk_create(new_records)

    return BossFight.objects.filter(
        fight_index__in=boss_indexes,
        raid=raid
    )


def import_characters(records):
    ids = [i['id'] for i in records]
    existing_ids = Character.objects.filter(
        warcraft_logs_id__in=ids
    ).values_list('warcraft_logs_id', flat=True)

    new_records = []

    for record in records:
        if str(record['id']) in existing_ids:
            continue

        new_records.append(
            Character(
                warcraft_logs_id=record['id'],
                name=record['name']
            )
        )

    Character.objects.bulk_create(new_records)
    return Character.objects.filter(warcraft_logs_id__in=ids)
