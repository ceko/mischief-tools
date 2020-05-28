from .api import get_reports, get_report
from ..models import Config, Raid
from .reports import import_reports, import_report
import json
import logging
import datetime
# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_new_reports():
    last_run = int(Config.get('last_processed_report_time', 0))
    logging.info("fetching reports since timestamp: {}".format(last_run))

    reports = json.loads(get_reports(last_run))
    reports.reverse()

    logging.info("processing {} reports".format(len(reports)))
    for report_summary in reports:
        logging.info("processing report summary for id: {}".format(
            report_summary['id']))
        import_reports([report_summary])
        report = json.loads(get_report(report_summary['id']))
        raid = Raid.objects.get(warcraft_logs_id=report_summary['id'])
        logging.info("processing report for id: {}".format(
            report_summary['id']))
        import_report(raid, report)

        logging.info(
            "updating last processed report to: {}".format(report['start']))

        # TODO: If the report['end'] is in the past, we can use that, using the report['start']
        # here will continue to reprocess the last report over and over again.

        end = report['end']
        if datetime.datetime.now().timestamp() * 1000 - end > 1000*60*60:
            logging.info(
                'report ended over an hour ago, will not attempt to reprocess')
            Config.set('last_processed_report_time', end)
        else:
            logging.info('report is a candidate for reprocessing')
            Config.set('last_processed_report_time', report['start'])
