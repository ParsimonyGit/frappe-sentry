import * as Sentry from '@sentry/browser';

frappe.ready(function () {
	if (!window.sentry_dsn) {
		frappe.call({
			method: "sentry.utils.get_sentry_dsn",
			callback: function (r) {
				if (r.message) {
					window.localStorage.sentry_dsn = r.message;
				}
			}
		});
	}

	if (window.localStorage.sentry_dsn) {
		Sentry.init({ dsn: window.localStorage.sentry_dsn });

		if (frappe.sid != "Guest") {
			Sentry.configureScope(function (scope) {
				scope.setUser({ email: frappe.user_id });
			});
		}
	}
})