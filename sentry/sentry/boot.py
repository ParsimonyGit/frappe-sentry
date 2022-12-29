import frappe

from sentry.sentry.utils import get_sentry_details


def boot_session(bootinfo):
	sentry_details = get_sentry_details()
	bootinfo.sentry = sentry_details
