"""Build linked project libraries without hiding retained supporting material."""
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'assets/data/projects.json').read_text(encoding='utf-8'))
esc = html.escape
total = 0
for project in catalog:
    page = ROOT / project['supporting_page']
    folder = page.parent
    files = sorted(p for p in folder.rglob('*') if p.is_file() and p != page
                   and p.suffix.lower() not in {'.creo', '.crc', '.dwl', '.dwl2', '.pbk'}
                   and not p.name.lower().startswith('trail.txt.'))
    project.pop('supporting_download', None)
    groups = {}
    for path in files:
        relative = path.relative_to(folder)
        category = '/'.join(relative.parts[:2]) if relative.parts[0] == 'media' else relative.parts[0] if len(relative.parts) > 1 else 'notes'
        groups.setdefault(category, []).append(path)
    sections = []
    for category, paths in sorted(groups.items()):
        entries = []
        for path in paths:
            relative = path.relative_to(folder).as_posix()
            url = esc(quote(relative))
            size = path.stat().st_size
            label = esc(relative)
            preview = ''
            if path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
                preview = f'<a href="{url}"><img src="{url}" alt="{esc(path.stem)}" loading="lazy" style="max-width:240px;max-height:180px;object-fit:contain"></a>'
            if path.suffix.lower() == '.mp4':
                preview = f'<video controls playsinline preload="none" src="{url}" aria-label="{esc(path.stem)}" style="max-width:100%;max-height:360px"></video>'
            if path.suffix.lower() in {'.md', '.txt', '.ino', '.cpp', '.h', '.py', '.csv'} and path.stat().st_size < 100000:
                preview = '<details><summary>Read text</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + esc(path.read_text(encoding='utf-8', errors='replace')) + '</pre></details>'
            entries.append(f'<li style="margin-block:1rem;overflow-wrap:anywhere">{preview}<p><a class="text-link" href="{url}">{label}</a> · {size / 1048576:.2f} MB · <a href="{url}" download>Download</a></p></li>')
        sections.append(f'<details><summary>{esc(category.title())} ({len(paths)})</summary><ul>{"".join(entries)}</ul></details>')
    title = esc(project['title'])
    page.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Supporting files</title>
<link rel="stylesheet" href="../../../css/styles.css">
<link rel="canonical" href="https://the-other-hello-there.github.io/HenryLuo-Portfolio/{quote(project['supporting_page'])}">
</head><body><main class="container section">
<a class="btn btn-small" href="https://the-other-hello-there.github.io/" aria-label="Personal landing page">HL</a>
<p><a class="text-link" href="../../../../index.html#project-{esc(project['id'])}">Back to project</a></p>
<h1>{title}</h1><h2>Supporting files</h2>
<p>Additional photos, video recordings, requirements, and project notes. The main case study presents the selected results; these files provide further context and design history.</p>
<p>Each file can be opened or downloaded individually. Expand a category to browse individual files. HEIC images may require downloading to view.</p>
{''.join(sections)}</main></body></html>''', encoding='utf-8')
    total += len(files)
print(f'Built {len(catalog)} supporting libraries linking {total} files.')

(ROOT / "assets/data/projects.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
