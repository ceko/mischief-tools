import os
import json
import pytest
from mm_tools.web.warcraft_logs import import_reports, import_report
from mm_tools.web.models import Raid, Boss, BossFight, Character
import datetime
from django.utils.timezone import make_aware

here = os.path.dirname(os.path.dirname(__file__))


def get_reports():
    report = os.path.join(here, 'fixtures/reports.json')

    with open(report, 'r') as f:
        report_contents = f.read()
        return report_contents


def get_report(variant='bwl'):
    report = os.path.join(here, 'fixtures/report.{}.json'.format(variant))

    with open(report, 'r') as f:
        report_contents = f.read()
        return report_contents


@pytest.mark.django_db
def test_load_reports():
    report_contents = get_reports()
    import_reports(json.loads(report_contents))

    zg_raid = Raid.objects.get(warcraft_logs_id='4NJwxZnqjRVhH8BF')

    assert zg_raid.title == "ZG"
    assert zg_raid.zone == 1003
    assert str(zg_raid.started_on) == '2020-05-15 03:16:20.125000+00:00'
    assert str(zg_raid.ended_on) == '2020-05-15 04:38:34.605000+00:00'


@pytest.mark.django_db
@pytest.mark.django_db
def test_load_over_reports():
    report_contents = get_reports()
    json_report_contents = json.loads(report_contents)
    first_report = json_report_contents.pop(0)

    import_reports(json_report_contents)
    import_reports(json_report_contents + [first_report])

    # if this doesn't throw we're good
    Raid.objects.get(warcraft_logs_id=first_report['id'])
    assert Raid.objects.all().count() == len(json_report_contents)+1


@pytest.mark.django_db
def test_load_bwl_report():
    raid = Raid(
        warcraft_logs_id='wacraft-log-id',
        title='test title',
        started_on=make_aware(datetime.datetime.now()),
        ended_on=make_aware(datetime.datetime.now()),
        zone=999
    )
    raid.save()

    import_report(raid, json.loads(get_report()))

    # Grethok the controller is considered a boss, the orb controller in Razorgore
    def run_tests():
        bosses = Boss.objects.all()
        fights = BossFight.objects.all()
        assert len(bosses) == 9
        assert len(fights) == 10
        assert fights[0].attendance.count() == 39
        assert fights[2].attendance.count() == 38

    run_tests()
    # This should not throw an error and all the above assertions should still hold true
    import_report(raid, json.loads(get_report()))
    run_tests()


@pytest.mark.django_db
def test_load_zg_report():
    raid = Raid(
        warcraft_logs_id='wacraft-log-id',
        title='test title',
        started_on=make_aware(datetime.datetime.now()),
        ended_on=make_aware(datetime.datetime.now()),
        zone=999
    )
    raid.save()

    import_report(raid, json.loads(get_report('zg')))

    # Grethok the controller is considered a boss, the orb controller in Razorgore
    def run_tests():
        bosses = Boss.objects.all()
        fights = BossFight.objects.all()
        assert len(bosses) == 9
        assert len(fights) == 9
        assert fights[0].attendance.count() == 19
        assert fights[6].attendance.count() == 20

    run_tests()
    # This should not throw an error and all the above assertions should still hold true
    import_report(raid, json.loads(get_report('zg')))
    run_tests()


@pytest.mark.django_db
def test_load_mc_report():
    raid = Raid(
        warcraft_logs_id='wacraft-log-id',
        title='test title',
        started_on=make_aware(datetime.datetime.now()),
        ended_on=make_aware(datetime.datetime.now()),
        zone=999
    )
    raid.save()

    import_report(raid, json.loads(get_report('mc')))

    def run_tests():
        bosses = Boss.objects.all()
        fights = BossFight.objects.all()
        assert len(bosses) == 10
        assert len(fights) == 10
        assert fights[0].attendance.count() == 40
        assert fights[0].attendance.filter(name='Kerfuffle').exists()
        assert fights[2].attendance.filter(name='Fordrion').exists()

    run_tests()
    # This should not throw an error and all the above assertions should still hold true
    import_report(raid, json.loads(get_report('mc')))
    run_tests()
