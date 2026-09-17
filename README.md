Created in tandem with ChatGPT

Project content lives in `assets/data/projects.json`. After updating the catalog, run
`python scripts/build_projects.py` to regenerate the static project cards and case-study
data in `index.html`. The page works directly from disk and on GitHub Pages; no server
or JavaScript build step is required to view it.

Run `python scripts/check_projects.py` to verify the catalog, asset paths, and generated
cards, followed by desktop and narrow-screen dialog checks in Microsoft Edge on Windows.
The browser checks require permission to launch headless Edge.
