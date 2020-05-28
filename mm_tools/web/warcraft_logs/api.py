import requests
from django.conf import settings

REPORTS_URL_TEMPLATE = 'https://classic.warcraftlogs.com:443/v1/reports/guild/mischief/pagle/us?api_key={}&start={}'
REPORT_URL_TEMPLATE = 'https://classic.warcraftlogs.com:443/v1/report/fights/{}?api_key={}'


def get_reports(since):
    return requests.get(REPORTS_URL_TEMPLATE.format(
        settings.WARCRAFT_LOGS_API_KEY,
        since
    )).text


def get_report(code):
    return requests.get(REPORT_URL_TEMPLATE.format(
        code,
        settings.WARCRAFT_LOGS_API_KEY
    )).text
