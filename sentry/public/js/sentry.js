import * as Sentry from "@sentry/browser";
import { CaptureConsole } from "@sentry/integrations";

if (frappe.boot.sentry?.dsn) {
	Sentry.init({
		dsn: frappe.boot.sentry.dsn,
		transport: Sentry.makeBrowserOfflineTransport(Sentry.makeFetchTransport),
		transportOptions: { maxQueueSize: 25 },
		integrations: [
			new Sentry.BrowserTracing({
				beforeNavigate: (context) => {
					const route = frappe.router.current_route
						? frappe.get_route().slice() // get a shallow copy of the route to avoid modifying cache
						: ["app"];

					if (route[0].toLowerCase() === "form") {
						route[2] = "<ID>";
					}

					return {
						...context,
						name: route.join("/"),
					};
				},
			}),
			new CaptureConsole({ levels: ["warn", "error", "debug"] }),
		],
		tracesSampleRate: 0.5,
		profilesSampleRate: 0.5,
	});

	Sentry.configureScope((scope) => {
		scope.setUser({ email: frappe.boot.user.email });
		scope.setTag("site", frappe.boot.sentry.site);
		scope.setTag("project", frappe.boot.sentry.project);
		scope.setTag("server_name", frappe.boot.sentry.server_name);
	});
}
