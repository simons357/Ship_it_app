"""HTML renderer for Process Console v5."""

from __future__ import annotations

import html
from typing import Any

from .process_console import ConsoleSnapshot, RunView
from .schema import ProcessStatus


def _esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _status_class(status: ProcessStatus) -> str:
    return {
        ProcessStatus.INCONCLUSIVE: "badge-inconclusive",
        ProcessStatus.PREREGISTERED: "badge-prereg",
        ProcessStatus.WITHDRAWN: "badge-withdrawn",
        ProcessStatus.CLOSED_NEGATIVE: "badge-closed",
        ProcessStatus.EXECUTED: "badge-executed",
    }.get(status, "badge-plain")


def _run_card(view: RunView) -> str:
    run = view.run
    checks = "".join(
        f"""
        <li class="check {'fail' if not c['passed'] else 'ok'}" data-check-id="{_esc(c['check_id'])}">
          <div class="check-flag">{'FAILED' if not c['passed'] else 'locked'}</div>
          <div>
            <div class="mono">{_esc(c['check_id'])}</div>
            <div><span class="k">Stipulated</span> {_esc(c['stipulated_formula'])}</div>
            <div><span class="k">Implementation</span> {_esc(c['implementation'])}</div>
            <p>{_esc(c['detail'])}</p>
          </div>
        </li>"""
        for c in (view.failed_checks or [c.to_dict() for c in run.consistency_checks])
    )
    if view.failed_checks:
        check_block = f"""
        <section class="failed-box" data-failed-checks="true">
          <h3>Failed consistency check</h3>
          <ul class="checks">{checks}</ul>
        </section>"""
    else:
        check_block = f"""
        <section>
          <h3>Consistency checks</h3>
          <ul class="checks">{checks}</ul>
        </section>"""

    stamps = "".join(
        f"""
        <li class="stamp stamp-{_esc(s['kind'])}">
          <span class="stamp-kind">{_esc(s['kind'].replace('_', ' ').upper())}</span>
          <span>{_esc(s['label'])}</span>
          <span class="stamp-status">{_esc(s['status'])}</span>
        </li>"""
        for s in view.stamps
    )
    promote_disabled = "disabled" if view.promotion.value != "allowed" else ""
    notes = "".join(f"<li>{_esc(n)}</li>" for n in run.notes)
    inherits = run.diagnostics.get("inherits_3915_663")
    inherit_line = (
        "<p class='ok-line'>Does not inherit 3,915/663 as evidence.</p>"
        if inherits is False
        else ""
    )
    hashes = "".join(
        f"<li><code>{_esc(k)}</code> <span class='mono'>{_esc(v[:12])}…</span></li>"
        for k, v in run.code_hashes.items()
    )
    hash_block = f"<ul class='hashes'>{hashes}</ul>" if hashes else "<p>No locked code hashes.</p>"
    return f"""
    <article class="run-card" id="{_esc(run.run_id)}" data-run-id="{_esc(run.run_id)}"
             data-process-status="{_esc(view.process_status.value)}"
             data-promotion="{_esc(view.promotion.value)}"
             data-scientific-outcome="{_esc(run.scientific_outcome)}">
      <header>
        <div class="eyebrow">{_esc(run.lane)} · {_esc(run.version)} · schema v5</div>
        <h2>{_esc(run.title)}</h2>
        <div class="badge {_status_class(view.process_status)}" data-status-badge="true">
          {_esc(view.process_status.value.upper())}
        </div>
      </header>
      <p class="outcome-note">
        Scientific outcome is stored, not judged:
        <em>{_esc(run.scientific_outcome)}</em>
      </p>
      {check_block}
      <section>
        <h3>Stamps (typed — not DA-STAMPED)</h3>
        <ul class="stamps">{stamps}</ul>
      </section>
      <section>
        <h3>Decision window</h3>
        <p class="mono">{_esc(run.decision_window.window_id)}</p>
        <p>Locked unless DA changes it beforehand.
           changed_by_da={_esc(run.decision_window.changed_by_da)}</p>
      </section>
      <section>
        <h3>Locked hashes</h3>
        {hash_block}
        {inherit_line}
      </section>
      <section>
        <h3>Notes</h3>
        <ul>{notes}</ul>
      </section>
      <footer class="promote-row">
        <button type="button" class="promote" data-promote="{_esc(run.run_id)}" {promote_disabled}>
          Promote to evidence
        </button>
        <p class="promote-reason" data-promote-reason="{_esc(run.run_id)}">
          {_esc(view.promotion_reason)}
        </p>
      </footer>
    </article>"""


def render_console_html(snapshot: ConsoleSnapshot) -> str:
    engineering = [v for v in snapshot.runs if v.run.lane in {"historical", "engineering"}]
    research = [v for v in snapshot.runs if v.run.lane not in {"historical", "engineering"}]
    if not engineering:
        engineering = snapshot.runs[:1]
        research = snapshot.runs[1:]
    eng_html = "".join(_run_card(v) for v in engineering)
    res_html = "".join(_run_card(v) for v in research)
    shortcuts = "".join(
        f"""
        <figure class="shortcut" data-shortcut-id="{_esc(s.shortcut_id)}">
          <figcaption>Closed shortcut</figcaption>
          <div class="boxed">{_esc(s.statement)}</div>
          <p class="tex">{_esc(s.boxed)}</p>
          <p>{_esc(s.evidence_role)}</p>
          <p class="origin">{_esc(s.origin)}</p>
        </figure>"""
        for s in snapshot.atlas.prominent_shortcuts()
    )
    stamp_legend = "".join(
        f"<li><strong>{_esc(s['kind'].replace('_', ' ').upper())}</strong> — {_esc(s['label'])}</li>"
        for s in snapshot.stamp_kinds
    )
    rules = "".join(f"<li>{_esc(r)}</li>" for r in snapshot.rules)
    live = snapshot.live_taylor_green
    withdrawn = snapshot.withdrawn_taylor_green
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Process Console v5</title>
  <style>
    :root {{
      --ink: #1b1a17;
      --paper: #f4efe6;
      --card: #fffdf8;
      --rule: #d8cfc0;
      --fail: #8b1e1e;
      --fail-bg: #f8e4e2;
      --prereg: #1f4d3a;
      --prereg-bg: #dcece4;
      --withdrawn: #6b4a16;
      --withdrawn-bg: #f3e6c8;
      --accent: #243f73;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 16px/1.45 "Iowan Old Style", "Palatino Linotype", Palatino, serif;
      background: var(--paper);
      color: var(--ink);
    }}
    header.mast {{
      padding: 28px 32px 18px;
      border-bottom: 2px solid var(--ink);
    }}
    header.mast h1 {{ margin: 0 0 6px; font-size: 32px; letter-spacing: 0.02em; }}
    .sub {{ color: #4a453c; max-width: 70ch; }}
    main {{ padding: 24px 32px 64px; }}
    .lanes {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    @media (max-width: 960px) {{ .lanes {{ grid-template-columns: 1fr; }} }}
    h2.lane {{
      margin: 0 0 12px;
      font-size: 13px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }}
    .run-card {{
      background: var(--card);
      border: 1px solid var(--rule);
      padding: 20px 22px 16px;
      margin-bottom: 18px;
    }}
    .eyebrow {{ font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: #6a6358; }}
    .run-card h2 {{ margin: 6px 0 10px; font-size: 22px; }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      font-size: 13px;
      letter-spacing: 0.08em;
      border: 1px solid currentColor;
    }}
    .badge-inconclusive {{ color: var(--fail); background: var(--fail-bg); }}
    .badge-prereg {{ color: var(--prereg); background: var(--prereg-bg); }}
    .badge-withdrawn {{ color: var(--withdrawn); background: var(--withdrawn-bg); }}
    .failed-box {{
      background: var(--fail-bg);
      border-left: 4px solid var(--fail);
      padding: 8px 12px;
      margin: 12px 0;
    }}
    .k {{ font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: #6a6358; margin-right: 6px; }}
    .mono {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; }}
    .stamps, .checks, .hashes {{ list-style: none; padding: 0; }}
    .stamp {{ margin: 6px 0; padding: 8px; border: 1px dashed var(--rule); }}
    .stamp-kind {{ font-weight: 700; margin-right: 8px; }}
    .promote-row {{ margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--rule); }}
    button.promote {{
      font: inherit;
      padding: 8px 14px;
      border: 1px solid var(--ink);
      background: #eee8dc;
    }}
    button.promote[disabled] {{
      color: var(--fail);
      border-color: var(--fail);
      background: var(--fail-bg);
      cursor: not-allowed;
    }}
    .promote-reason {{ margin: 8px 0 0; font-size: 14px; }}
    .atlas, .errata, .legend, .rules {{
      margin-top: 28px;
      padding: 18px 20px;
      border: 1px solid var(--ink);
      background: var(--card);
    }}
    .boxed {{
      font-size: 20px;
      padding: 16px;
      border: 2px solid var(--ink);
      text-align: center;
      margin: 10px 0;
    }}
    .tex {{ font-family: ui-monospace, monospace; font-size: 13px; color: #4a453c; }}
    .withdrawn-tag {{
      display: inline-block;
      background: var(--withdrawn-bg);
      color: var(--withdrawn);
      padding: 2px 8px;
      letter-spacing: 0.1em;
      font-size: 12px;
      border: 1px solid var(--withdrawn);
    }}
    .values {{ display: flex; gap: 24px; flex-wrap: wrap; }}
    .ok-line {{ color: var(--prereg); }}
    .toast {{
      position: fixed; right: 18px; bottom: 18px;
      background: var(--fail); color: white; padding: 10px 14px;
      display: none;
    }}
  </style>
</head>
<body>
  <header class="mast">
    <h1>Process Console</h1>
    <p class="sub">
      Schema {snapshot.schema_version}. Engineering lane first: F-X2 relabels
      are finished. This desk represents Q4 correctly as
      <strong>INCONCLUSIVE</strong> when the consistency check failed.
      It does not depend on Q4’s scientific outcome.
    </p>
  </header>
  <main>
    <div class="lanes">
      <section>
        <h2 class="lane">Engineering lane — historical / process</h2>
        {eng_html}
      </section>
      <section>
        <h2 class="lane">Research lane — preregistered</h2>
        {res_html}
      </section>
    </div>

    <section class="atlas" id="atlas">
      <h2>Atlas — closed shortcuts</h2>
      <p>Not bad news. A closed door on the scientific map.</p>
      {shortcuts}
    </section>

    <section class="errata" id="errata">
      <h2>Taylor–Green erratum</h2>
      <div class="values">
        <div>
          <h3>Live scientific value</h3>
          <p class="boxed">r² = {_esc(live.get('r_squared'))}<br>
          T<sub>c</sub>/(ν D<sub>s</sub>) = {_esc(live.get('T_c_over_nu_D_s'))}</p>
        </div>
        <div>
          <h3>Historical provenance</h3>
          <span class="withdrawn-tag">WITHDRAWN</span>
          <p>Old Taylor–Green fraction {_esc(withdrawn.get('display'))}
             is not a live scientific value.</p>
        </div>
      </div>
    </section>

    <section class="legend">
      <h2>Stamp kinds — schema, not prose</h2>
      <ul>{stamp_legend}</ul>
      <p>Opaque <code>DA-STAMPED</code> is rejected by F-X2.</p>
    </section>

    <section class="rules">
      <h2>Process rules this error produced</h2>
      <ul>{rules}</ul>
    </section>
  </main>
  <div class="toast" id="toast" role="status"></div>
  <script>
    const toast = document.getElementById('toast');
    document.querySelectorAll('[data-promote]').forEach((btn) => {{
      btn.addEventListener('click', async () => {{
        const id = btn.getAttribute('data-promote');
        let decision = 'prohibited';
        let reason = document.querySelector('[data-promote-reason="' + id + '"]').textContent.trim();
        try {{
          const res = await fetch('/api/promote', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{run_id: id}})
          }});
          const data = await res.json();
          decision = data.decision || decision;
          reason = data.reason || reason;
        }} catch (err) {{
          decision = 'prohibited';
        }}
        toast.textContent = id + ' — promotion ' + decision + '. ' + reason;
        toast.style.display = 'block';
      }});
    }});
  </script>
</body>
</html>
"""
