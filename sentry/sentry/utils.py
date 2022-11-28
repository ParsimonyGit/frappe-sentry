import frappe
import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration


def init_sentry():
	sentry_details = get_sentry_details()
	if not sentry_details or not sentry_details.dsn:
		return

	if sentry_enabled():
		sentry_sdk.init(sentry_details.dsn, integrations=[RqIntegration()])


def capture_exception(title=None, message=None, reference_doctype=None, reference_name=None):
	init_sentry()

	with sentry_sdk.configure_scope() as scope:
		scope.user = {"email": frappe.session.user}
		scope.set_tag("site", frappe.conf.get("sentry_site", frappe.local.site))
		scope.set_tag("project", frappe.conf.get("sentry_project", frappe.local.site))
		scope.set_tag(
			"server_name", frappe.conf.get("sentry_server_name", frappe.local.site)
		)

		if reference_doctype and reference_name:
			scope.set_tag("reference_doctype", reference_doctype)
			scope.set_tag("reference_name", reference_name)

	sentry_sdk.capture_exception()


@frappe.whitelist(allow_guest=True)
def get_sentry_details():
	if sentry_enabled():
		return frappe._dict(
			{
				"dsn": frappe.conf.get("sentry_dsn"),
				"site": frappe.conf.get("sentry_site", frappe.local.site),
				"project": frappe.conf.get("sentry_project", frappe.local.site),
				"server_name": frappe.conf.get("sentry_server_name", frappe.local.site),
			}
		)


def sentry_enabled():
	enabled = True
	if frappe.conf.get("developer_mode"):
		# You can set this in site_config.json to enable sentry in developer mode
		# ... enable_sentry_developer_mode: 1 ...
		enabled = frappe.conf.get("enable_sentry_developer_mode", False)

	return enabled
