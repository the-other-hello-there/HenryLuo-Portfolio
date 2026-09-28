# Engineering portfolio

Edit `assets/data/projects.json` for project content. Selected images, videos,
and posters live in each project's `media/` folders. Supporting files are linked
individually from `supporting/index.html`; there are no project-wide ZIPs or
`downloads/` folders. Images and videos preview in the browser; text and source
code have inline previews. Specialized formats can be downloaded individually.

Install presentation dependencies with `python -m pip install -r scripts/requirements-presentation.txt`.
Then rebuild after every project-content or selected-image change:

```powershell
python scripts/build_supporting.py
python scripts/build_projects.py
python scripts/build_search.py
python scripts/build_presentation.py --check
python scripts/build_search.py --check
python scripts/check_projects.py
python scripts/check_projects.py --file
```

`build_projects.py` automatically rebuilds `assets/project_descriptions/fullportfolio.pptx`.
The presentation has one illustrated slide per project, with concise bullets and fuller
catalog details and limitations in speaker notes. Its build record fingerprints
the catalog, selected images, notes, generator, and output to detect stale content.
The presentation is a sitemap-only Easter egg. Keep both formats synchronized, as
required by `AGENTS.md`.

Copy `scripts/root-sitemap.xml` to `../GithubMainRepo/sitemap.xml` and `robots.txt`
to that site's root. Approved image/video hashes live in `scripts/search-selection.json`.
Review asset changes before refreshing them. No build step deploys the website.

Native CAD and its viewer have been removed. STEP exports are permitted, at most
one per distinct part, but deleted models are not automatically restored.
Cleanup and video-conversion records remain in `scripts/`; the video record
identifies external recovery copies of the original recordings.

`Introduction.txt` and `fullportfolio.pptx` are sitemap-only Easter eggs. Neither
has website navigation links or explicit robots.txt rules; existing crawler restrictions remain.
