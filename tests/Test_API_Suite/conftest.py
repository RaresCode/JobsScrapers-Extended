import pytest

# Set the location and name of the HTML report
def pytest_configure(config):
    config.option.htmlpath = '.\\Reports\\report_api.html'

# Set the HTML Report title Name
def pytest_html_report_title(report):
    report.title = "Full API Test Run"