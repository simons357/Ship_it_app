# Cursor Setup Advisor (plugin)

Personal advisor plugin that helps you configure Cursor correctly.

## Components

- `agents/cursor-setup-advisor.md` — specialist setup coach
- `skills/cursor-setup-check/` — setup audit (`/cursor-setup-check`)
- `skills/choose-cursor-feature/` — feature picker (`/choose-cursor-feature`)
- `rules/cursor-setup-advisor.mdc` — surfaces guidance on setup questions

## Local install

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /absolute/path/to/ship_it_app/cursor-setup-advisor ~/.cursor/plugins/local/cursor-setup-advisor
```

Reload Cursor, then open **Customize** and confirm the plugin components are visible.

See [docs/CURSOR-SETUP-ADVISOR.md](../docs/CURSOR-SETUP-ADVISOR.md) for full usage.
