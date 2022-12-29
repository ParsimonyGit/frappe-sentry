__version__ = "0.1.0"

import frappe
import frappe.utils.background_jobs
from frappe import log_error as frappe_log_error
from frappe.app import handle_exception as frappe_handle_exception
from frappe.utils.background_jobs import start_worker as frappe_start_worker


def sentry_log_error(title=None, message=None, reference_doctype=None, reference_name=None):
	"""Log error to Frappe Error Log and forward to Sentry"""
	from sentry.sentry.utils import capture_exception

	try:
		capture_exception(title, message, reference_doctype, reference_name)
	except Exception as e:
		print("error capturing exception", e)
	finally:
		frappe_log_error(title, message, reference_doctype, reference_name)


def start_worker_with_sentry_logging(queue=None, quiet=False, rq_username=None, rq_password=None):
	"""Wrapper to start rq worker. Connects to redis and monitors these queues. Includes a Sentry integration"""
	from sentry.sentry.utils import init_sentry

	try:
		init_sentry()
	except Exception as e:
		print("error starting worker", e)
	finally:
		frappe_start_worker(queue, quiet, rq_username, rq_password)


def sentry_handle_exception(e):
	from sentry.sentry.utils import capture_exception

	http_status_code = getattr(e, "http_status_code", 500)
	if http_status_code >= 500:
		try:
			capture_exception()
		except Exception as exc:
			print("error capturing exception", exc)

	return frappe_handle_exception(e)


frappe.log_error = sentry_log_error
frappe.app.handle_exception = sentry_handle_exception
frappe.utils.background_jobs.start_worker = start_worker_with_sentry_logging
