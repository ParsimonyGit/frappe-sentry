## Sentry

Sends errors and performance data to Sentry. Compatible with Frappe / ERPNext v14.

### Features

- Sends front-end and backend errors to Sentry
- Performance monitoring (only front-end)
- Sends account email and site when error occurs
- If `frappe.log_error` is called without exception, it takes the message and title and passes that to Sentry

### Configuring Sentry

You can add the following keys to either the `common_site_config.json` file, or a specific site's `site_config.json` file.

**Note**: Adding any key to a site's `site_config.json` file will override that attribute's value in the `common_site_config.json` file.

```json
{
    ...
    "enable_sentry_developer_mode": true, // to enable sentry when `developer_mode` is active
    "sentry_dsn": "https://<key>:<secret>@sentry.io/<project_id>",  // fetch from a Sentry project's settings
    "sentry_site": "", // optional attribute to tag events with a site; default: site URL
    "sentry_project": "", // optional attribute to tag events with a project; default: site URL
    "sentry_server_name": "", // optional attribute to tag events with a server name; default: site URL
    ...
}
```

### License

MIT