import datetime
import json

import flask_monitoringdashboard as dashboard
import pytz
from flask import Flask
from flask import request
from flask_restx import Api
from jsonschema import FormatChecker
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.middleware.proxy_fix import ProxyFix


def init_api(title, version, description, dashboard_config_init_kwargs=None):

    app = Flask(__name__)

    # Fix specific for AOS server
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Overwrite dashboard config defaults
    dashboard.config.timezone = pytz.timezone("Europe/Amsterdam")
    dashboard.config.monitor_level = 1
    # Allow user to provide personal config
    if dashboard_config_init_kwargs is not None:
        dashboard.config.init_from(**dashboard_config_init_kwargs)

    dashboard.bind(app)

    # fmt: off
    # Remove monkey patch upon resolvement of PR #402
    # https://github.com/flask-dashboard/Flask-MonitoringDashboard/pull/402
    import flask_monitoringdashboard.core.measurement  # isort:skip # noqa:E402
    from src.dh_api._helpers.monitoring_dashboard_bugfix import evaluate_fixed  # isort:skip # noqa:E402
    flask_monitoringdashboard.core.measurement.evaluate = evaluate_fixed

    # Allow dates not to strictly adhere to ISO8601
    # https://github.com/noirbizarre/flask-restplus/issues/603#issuecomment-472367498
    format_checker = FormatChecker()
    # fmt: on
    @format_checker.checks("date", ValueError)  # noqa: E302
    def lenient_date_check(value):
        """Check if input value is valid date"""
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True

    api = Api(
        app,
        version=version,
        title=title,
        description=description,
        # https://github.com/python-restx/flask-restx/issues/344
        format_checker=format_checker,
    )

    @app.after_request
    def log_500_responses(response):
        """Log request body of last 500 response"""
        try:
            if response.status_code.numerator == 500:
                with open("last_500_request_body.json", "w") as outfile:
                    json.dump(request.get_json(), outfile)
        except Exception as e:
            # Pass for all, as otherwise other 'after_request' functionality will be broken
            with open("last_500_request_body_FAILED.txt", "w") as outfile:
                outfile.write(str(repr(e)))
        return response

    @app.after_request
    def inject_api_version(response):
        """Ensure api_version is appended to HTTP codes 400 and 500 of API endpoints"""
        api_endp = [i for i in api.endpoints if i != "specs"]
        api_urls = [
            rule.rule for rule in app.url_map.iter_rules() if rule.endpoint in api_endp
        ]
        if request.path in api_urls:
            data = response.get_json()
            if "api_version" not in data:
                data["api_version"] = version
                response.set_data(json.dumps(data))
        return response

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        """Improve informativeness of MethodNotAllowed message response"""
        return {
            "message": error.description,
            "valid_methods": error.valid_methods,
            "requested_method": request.method,
        }, 405

    return app, api, dashboard
