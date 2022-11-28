import * as Sentry from '@sentry/browser'
import { CaptureConsole, Offline } from '@sentry/integrations'
import { Integrations } from "@sentry/tracing"

if (frappe.boot.sentry?.dsn) {
	Sentry.init(
		{
			dsn: frappe.boot.sentry_dsn,
			integrations: [
				new Integrations.BrowserTracing({
					beforeNavigate: context => {
						const route = frappe.router.current_route
							// get a shallow copy of the route to avoid modifying cache
							? frappe.get_route().slice()
							: ["app"];

						if (route[0].toLowerCase() === "form") {
							route[2] = "<ID>";
						}

						return {
							...context,
							name: route.join("/")
						}
					}
				}),
				new CaptureConsole({ levels: ['warn', 'error', 'debug'] }),
				new Offline({ maxStoredEvents: 25 })
			],
			tracesSampleRate: 1.0, // adjust value once we're live
		});

	Sentry.configureScope(scope => {
		scope.setUser({ email: frappe.boot.user.email })
		scope.setTag("site", frappe.boot.sentry.site)
		scope.setTag("project", frappe.boot.sentry.project)
		scope.setTag("server_name", frappe.boot.sentry.server_name)
	})
}