import * as Sentry from '@sentry/browser';
import { Integrations } from "@sentry/tracing";

if (frappe.boot.sentry_dsn) {

	Sentry.init(
		{
			dsn: frappe.boot.sentry_dsn,
			integrations: [new Integrations.BrowserTracing({
				beforeNavigate: context => {
					return {
						...context,
						name: frappe._cur_route
					}
				}
			})],
			tracesSampleRate: 1.0, // adjust value once we're live
		});



	Sentry.configureScope(function (scope) {
		scope.setUser({ email: frappe.boot.user.email });
	});
}