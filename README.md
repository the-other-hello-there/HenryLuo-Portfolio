Created in tandem with ChatGPT

Project content lives in `assets/data/projects.json`. After updating the catalog, run
`python scripts/build_projects.py` to regenerate the static project cards and case-study
data in `index.html`. The page works directly from disk and on GitHub Pages; no server
or JavaScript build step is required to view it.

Run `python scripts/check_projects.py` to verify the catalog, asset paths, and generated
cards, followed by desktop and narrow-screen dialog checks in Microsoft Edge on Windows.
The browser checks require permission to launch headless Edge.

Search discovery is curated in `scripts/search-selection.json`. After reviewing
changes to approved assets, run `python scripts/build_search.py`, then
`python scripts/build_search.py --check`. See [SEARCH_POLICY.md](SEARCH_POLICY.md)
for review decisions, crawler settings, and the required host-root installation
of `robots.txt` for this GitHub Pages project site.
