import flask_monitoringdashboard.core.measurement


def evaluate_fixed(route_handler, args, kwargs):
    """Replaces flask_monitoringdashboard.core.measurement.evaluate

    Incorporates pending PR #402
    https://github.com/flask-dashboard/Flask-MonitoringDashboard/pull/402
    """
    try:
        result = route_handler(*args, **kwargs)
        status_code = (
            flask_monitoringdashboard.core.measurement.status_code_from_response(result)
        )

        return result, status_code, None

    except Exception as e:
        try:
            status_code = e.code
        except AttributeError:
            status_code = 500
        return None, status_code, e
