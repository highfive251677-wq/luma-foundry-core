from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path('/home/ubuntu/luma-foundry')
APP = ROOT / 'client/src/App.tsx'
PAGES = ROOT / 'client/src/pages'
CSS = ROOT / 'client/src/index.css'
HOOK = ROOT / 'client/src/hooks/useBatchReveal.ts'
OUT = ROOT / 'QC_Source_Evidence_2026-08-28'
OUT.mkdir(exist_ok=True)

app = APP.read_text(encoding='utf-8')
css = CSS.read_text(encoding='utf-8')
hook = HOOK.read_text(encoding='utf-8') if HOOK.exists() else ''

# Build the component-to-file map from the actual App.tsx imports, including grouped batch imports.
component_files: dict[str, Path] = {}
for match in re.finditer(r'import\s+([A-Za-z][A-Za-z0-9_]*)\s+from\s+["\'](\./pages/[^"\']+)["\']', app):
    component_files[match.group(1)] = (ROOT / 'client/src' / match.group(2).replace('./', '')).with_suffix('.tsx')
for match in re.finditer(r'import\s*\{([^}]+)\}\s*from\s+["\'](\./pages/[^"\']+)["\']', app):
    source_file = (ROOT / 'client/src' / match.group(2).replace('./', '')).with_suffix('.tsx')
    for name in match.group(1).split(','):
        name = name.strip()
        if name:
            component_files[name] = source_file

route_rows: list[dict[str, str]] = []
for match in re.finditer(r'<Route\s+path=\{["\'](/[^"\']*)["\']\}\s+component=\{([A-Za-z][A-Za-z0-9_]*)\}\s*/>', app):
    route, component = match.groups()
    if route in {'/', '/404', '/workspace', '/ember-signal', '/luma-intelligence'}:
        continue
    source_path = component_files.get(component)
    if not source_path or not source_path.exists():
        raise SystemExit(f'No source file mapped for {route} -> {component}')
    route_rows.append({'route': route, 'component': component, 'source': str(source_path.relative_to(ROOT))})

if len(route_rows) != 50:
    raise SystemExit(f'Expected 50 official routes, found {len(route_rows)}')

ledger_text = (ROOT / 'Route_Certification_Ledger_2026-08-27.md').read_text(encoding='utf-8')
ledger_by_route: dict[str, dict[str, str]] = {}
for line in ledger_text.splitlines():
    m = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(`?(/[^`|]+)`?)\s*\|\s*([^|]+?)\s*\|', line)
    if m:
        number, brand, category, _, route, evidence = m.groups()
        ledger_by_route[route.strip()] = {'number': number, 'brand': brand.strip(), 'category': category.strip(), 'evidence': evidence.strip()}

batch_names = [
    ['Axiom Grid', 'Selene Agents', 'Kinetic Mesh', 'Lattice Labs', 'Orbital Ledger'],
    ['Stilla Care Systems', 'Morrow Compute', 'Vanta Proof', 'Helio Relay', 'Folio Forms'],
    ['Noor Vale', 'Aster & Alder', 'Élan Method', 'Vela Maison', 'Sardis Parfums'],
    ['Ruth Ibarra Botanics', 'Tempo Atelier', 'Peregrine Editions', 'Caldera Optical', 'Maré House'],
    ['Monolith Works', 'Nocturne Estates', 'Alder House', 'Formwell Interiors', 'Studio Lumen'],
    ['Maison Rook', 'Terra Forma', 'Veloce District', 'Hinge & Hearth', 'Fieldnote Cabins'],
    ['Kansa Objects', 'Ora Roasters', 'Corella Run', 'Solace Audio', 'Basil & Bone'],
    ['Vesper Pantry', 'Arq Supply', 'Perrin Carry', 'Wildercare', 'Havenlark'],
    ['Sable & Type', 'Civic Assembly', 'Masonry Films', 'Northline Counsel', 'Pattern School'],
    ['Oriel Advisory', 'Hinterland Sound', 'Quorum House', 'Adjacent Talent', 'Lumen & Co.'],
]
name_by_index = {i + 1: name for i, name in enumerate(sum(batch_names, []))}


def one_line(value: str) -> str:
    value = re.sub(r'\{[^{}]*\}', '', value, flags=re.S)
    value = re.sub(r'<br\s*/?>', ' / ', value, flags=re.I)
    value = re.sub(r'<[^>]+>', ' ', value)
    value = re.sub(r'\bsetMenu\([^)]*\)\s*\}\s*', ' ', value)
    value = re.sub(r'\s+', ' ', value)
    return value.strip(' /\t\n')


def component_slice(source: str, component: str) -> str:
    start_match = re.search(rf'export\s+(?:default\s+)?function\s+{re.escape(component)}\b', source)
    if not start_match:
        start_match = re.search(rf'(?:^|[;\n])\s*function\s+{re.escape(component)}\b', source)
    if not start_match:
        start_match = re.search(rf'export\s+const\s+{re.escape(component)}\b', source)
    if not start_match:
        return source
    rest = source[start_match.end():]
    next_match = re.search(r'(?:^|[;\n])\s*export\s+(?:default\s+)?(?:function|const)\s+[A-Z][A-Za-z0-9_]*\b', rest)
    return source[start_match.start(): start_match.end() + (next_match.start() if next_match else len(rest))]


def first_texts(source: str, tag: str, limit: int = 8) -> list[str]:
    values = []
    for m in re.finditer(rf'<{tag}\b[^>]*>(.*?)</{tag}>', source, flags=re.S | re.I):
        text = one_line(m.group(1))
        if text and text not in values:
            values.append(text)
        if len(values) >= limit:
            break
    return values


def attr(attrs: str, key: str) -> str:
    m = re.search(rf'\b{key}\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{{([^}}]*)\}})', attrs)
    return next((x for x in m.groups() if x is not None), '') if m else ''

# Shared rule evidence is intentionally stated at source level. Runtime tab order is not claimed.
focus_selector_count = len(re.findall(r':focus-visible', css))
focus_summary = 'Global :focus-visible rules found in client/src/index.css; exact occurrence count: ' + str(focus_selector_count) + '.'

keyboard_rows: list[dict[str, str]] = []
copy_rows: list[dict[str, str]] = []
for index, row in enumerate(route_rows, 1):
    source_path = ROOT / row['source']
    source_full = source_path.read_text(encoding='utf-8')
    source = component_slice(source_full, row['component'])
    authored_skip = bool(re.search(r'(?:skip\s*to\s*(?:content|main)|skip-to-content|className=["\'][^"\']*skip)', source, flags=re.I))
    shared_hook = 'useBatchReveal' in source_full or bool(re.search(r'\buseE\s*\(', source_full))
    main_match = re.search(r'<main\b([^>]*)>', source, flags=re.S | re.I)
    main_attrs = main_match.group(1) if main_match else ''
    main_id = attr(main_attrs, 'id')
    explicit_main_focus = bool(re.search(r'\btabIndex\s*=\s*(?:\{\s*-1\s*\}|["\']-1["\'])', main_attrs))
    shared_main_focus = shared_hook and not authored_skip
    controls = []
    for control in re.finditer(r'<(a|button|input|select|textarea|summary)\b([^>]*)>', source, flags=re.S | re.I):
        tag, attrs = control.groups()
        label = attr(attrs, 'aria-label') or attr(attrs, 'href') or attr(attrs, 'type') or tag.lower()
        controls.append(f'{tag.lower()}[{label}]')
    controls = list(dict.fromkeys(controls))[:8]
    focus_path = []
    focus_path.append('authored skip link' if authored_skip else ('shared injected skip link' if shared_main_focus else 'no skip link detected in source'))
    focus_path.append(f'main#{main_id or "unidentified"}' + (' (explicit tabIndex=-1)' if explicit_main_focus else (' (shared hook target)' if shared_main_focus else '')))
    focus_path.append('first controls: ' + ', '.join(controls) if controls else 'first controls: none detected')
    risk = 'None found at source level' if (controls and (authored_skip or shared_main_focus)) else 'Review manually: no complete skip/main path evidenced in source'
    keyboard_rows.append({
        'no': str(index).zfill(2),
        'brand': ledger_by_route.get(row['route'], {}).get('brand', name_by_index.get(index, row['component'])),
        'route': row['route'],
        'component': row['component'],
        'source': row['source'],
        'source_order_evidence': '; '.join(focus_path),
        'visible_focus_evidence': focus_summary,
        'keyboard_risk': risk,
        'evidence_level': 'Source-level only; runtime tab order not tested in this lane.',
    })

    h1 = first_texts(source, 'h1', 1)
    paragraphs = first_texts(source, 'p', 5)
    button_texts = first_texts(source, 'button', 8)
    anchor_texts = []
    for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', source, flags=re.S | re.I):
        label = one_line(m.group(2))
        if label and label not in anchor_texts and not label.startswith('http'):
            anchor_texts.append(label)
        if len(anchor_texts) >= 8:
            break
    actions = list(dict.fromkeys(button_texts + anchor_texts))[:10]
    copy_rows.append({
        'no': str(index).zfill(2),
        'brand': ledger_by_route.get(row['route'], {}).get('brand', name_by_index.get(index, row['component'])),
        'category': ledger_by_route.get(row['route'], {}).get('category', ''),
        'route': row['route'],
        'component': row['component'],
        'hero_heading': h1[0] if h1 else 'Not extracted from source',
        'leading_copy': paragraphs[0] if paragraphs else 'Not extracted from source',
        'cta_and_navigation_copy': ' | '.join(actions) if actions else 'No literal action text extracted',
        'differentiation_basis': ledger_by_route.get(row['route'], {}).get('evidence', 'Source text extracted; manual differentiation review still required.'),
        'evidence_level': 'Source extraction plus existing certification-ledger note; not a new runtime conversion test.',
    })


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv(OUT / 'keyboard_tab_order_matrix.csv', keyboard_rows)
write_csv(OUT / 'copy_cta_differentiation_ledger.csv', copy_rows)


def md_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open('w', encoding='utf-8') as handle:
        handle.write('| ' + ' | '.join(headers) + ' |\n')
        handle.write('|' + '|'.join('---' for _ in headers) + '|\n')
        for row in rows:
            safe = [str(value).replace('|', '\\|').replace('\n', ' ') for value in row]
            handle.write('| ' + ' | '.join(safe) + ' |\n')

with (OUT / 'keyboard_tab_order_matrix.md').open('w', encoding='utf-8') as handle:
    handle.write('# Keyboard Tab-Order and Visible-Focus Evidence Matrix\n\n')
    handle.write('**Scope:** all 50 official routes. **Evidence class:** source-level only; this artifact does not claim a runtime browser tab-order test.\n\n')
    handle.write(f'Global focus evidence: `{focus_summary}` Shared hook evidence is recorded per route where `useBatchReveal` is present.\n\n')
    md_table(OUT / '_keyboard.tmp', ['#', 'Brand', 'Route', 'Source order evidence', 'Keyboard risk', 'Evidence level'], [
        [r['no'], r['brand'], r['route'], r['source_order_evidence'], r['keyboard_risk'], r['evidence_level']] for r in keyboard_rows
    ])
    handle.write((OUT / '_keyboard.tmp').read_text(encoding='utf-8'))
(OUT / '_keyboard.tmp').unlink()

with (OUT / 'copy_cta_differentiation_ledger.md').open('w', encoding='utf-8') as handle:
    handle.write('# Copy and CTA Differentiation Ledger\n\n')
    handle.write('**Scope:** all 50 official routes. This is a source extraction and cross-reference artifact; it does not claim a fresh runtime conversion test. Existing ledger evidence is preserved as the differentiation basis.\n\n')
    md_table(OUT / '_copy.tmp', ['#', 'Brand', 'Category', 'Route', 'Hero heading', 'Leading copy', 'CTA/navigation copy', 'Differentiation basis'], [
        [r['no'], r['brand'], r['category'], r['route'], r['hero_heading'], r['leading_copy'], r['cta_and_navigation_copy'], r['differentiation_basis']] for r in copy_rows
    ])
    handle.write((OUT / '_copy.tmp').read_text(encoding='utf-8'))
(OUT / '_copy.tmp').unlink()

# Timing inventory: capture every CSS timing declaration and every explicit timing utility in product-route sources.
timing_rows: list[dict[str, str]] = []
css_decl_re = re.compile(r'(?P<property>transition(?:-[\w-]+)?|animation(?:-[\w-]+)?)\s*:\s*(?P<value>[^;}]+)', re.I)
for path in [CSS, HOOK, *sorted(PAGES.glob('*.tsx')), *sorted(PAGES.glob('*.css'))]:
    text = path.read_text(encoding='utf-8')
    rel = str(path.relative_to(ROOT))
    for m in css_decl_re.finditer(text):
        value = m.group('value').strip()
        durations = re.findall(r'(?<![\w.-])(\d+(?:\.\d+)?)(ms|s)\b', value, flags=re.I)
        if not durations:
            continue
        line = text.count('\n', 0, m.start()) + 1
        ms_values = [round(float(number) * (1000 if unit.lower() == 's' else 1), 2) for number, unit in durations]
        status = 'Within routine 200–350 ms range' if all(200 <= value <= 350 for value in ms_values) else 'Intentional/needs review exception outside routine range'
        if 'data-reveal' in text[max(0, m.start()-220):m.start()+220] or any(value > 350 for value in ms_values):
            status = 'Documented exception: entrance/reveal or image treatment outside routine range'
        timing_rows.append({'file': rel, 'line': str(line), 'declaration': m.group('property'), 'value': value, 'durations_ms': ', '.join(map(str, ms_values)), 'status': status, 'evidence_level': 'Static source declaration; runtime feel not tested here.'})
    for m in re.finditer(r'\bduration-(\d+)\b', text):
        line = text.count('\n', 0, m.start()) + 1
        value = int(m.group(1))
        timing_rows.append({'file': rel, 'line': str(line), 'declaration': 'Tailwind duration utility', 'value': m.group(0), 'durations_ms': str(value), 'status': 'Within routine 200–350 ms range' if 200 <= value <= 350 else 'Intentional/needs review exception outside routine range', 'evidence_level': 'Static source utility; runtime feel not tested here.'})

# Stable de-duplication retains every unique declaration, but avoids duplicate hits from the same source span.
seen = set()
deduped = []
for row in timing_rows:
    key = tuple(row.items())
    if key not in seen:
        seen.add(key)
        deduped.append(row)
timing_rows = deduped
write_csv(OUT / 'complete_motion_timing_inventory.csv', timing_rows)

with (OUT / 'complete_motion_timing_inventory.md').open('w', encoding='utf-8') as handle:
    handle.write('# Complete Static Motion-Timing Inventory\n\n')
    handle.write('**Scope:** CSS timing declarations and explicit duration utilities found in the product source tree, shared hook, and global stylesheet. **Evidence class:** static source only; this does not prove runtime smoothness.\n\n')
    handle.write('Routine target: 200–350 ms. Entrance reveals, image treatments, and reduced-motion overrides are recorded as exceptions rather than silently treated as routine interactions.\n\n')
    md_table(OUT / '_timing.tmp', ['File', 'Line', 'Declaration', 'Value', 'Durations (ms)', 'Status', 'Evidence level'], [
        [r['file'], r['line'], r['declaration'], r['value'], r['durations_ms'], r['status'], r['evidence_level']] for r in timing_rows
    ])
    handle.write((OUT / '_timing.tmp').read_text(encoding='utf-8'))
(OUT / '_timing.tmp').unlink()

route_count = len(route_rows)
authored_count = sum('authored skip link' in r['source_order_evidence'] for r in keyboard_rows)
shared_count = sum('shared injected skip link' in r['source_order_evidence'] for r in keyboard_rows)
no_skip_count = route_count - authored_count - shared_count
routine_count = sum('Within routine' in r['status'] for r in timing_rows)
exception_count = len(timing_rows) - routine_count
with (OUT / 'README.md').open('w', encoding='utf-8') as handle:
    handle.write('# No-Credit QC Evidence Package\n\n')
    handle.write('Generated from the local Luma Foundry source tree and existing certification ledger only. No external connector, paid API, deployment, or Google Drive/Sheet mutation was used.\n\n')
    handle.write('| Artifact | Coverage | Evidence boundary |\n|---|---:|---|\n')
    handle.write(f'| Keyboard tab-order matrix | {route_count} routes | Source-level; runtime tab order not claimed |\n')
    handle.write(f'| Copy/CTA differentiation ledger | {route_count} routes | Source extraction plus existing ledger notes |\n')
    handle.write(f'| Static motion inventory | {len(timing_rows)} declarations/utilities | Source-level; runtime feel not claimed |\n')
    handle.write(f'| Authored skip-link evidence | {authored_count} routes | Source-level |\n')
    handle.write(f'| Shared injected skip-link evidence | {shared_count} routes | Source-level hook path |\n')
    handle.write(f'| No skip path detected in source | {no_skip_count} routes | Requires manual review or runtime evidence |\n')
    handle.write(f'| Routine-range timing entries | {routine_count} | Static declarations only |\n')
    handle.write(f'| Timing exceptions | {exception_count} | Must not be conflated with routine controls |\n\n')
    handle.write('These artifacts close the no-credit preparation lane only. They do not replace live browser verification, universal assistive-technology testing, commercial/IP clearance, checkout testing, or fulfillment testing.\n')

print(f'Generated {route_count} route rows, {len(timing_rows)} timing entries, {authored_count} authored skip-link rows, {shared_count} shared-hook skip-link rows, and {no_skip_count} source-level review rows.')
