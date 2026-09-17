"""Build static project cards and embedded case-study data from the project catalog."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '    <!-- PROJECTS:START -->'
END = '    <!-- PROJECTS:END -->'


def build():
    projects = json.loads((ROOT / 'assets/data/projects.json').read_text(encoding='utf-8'))
    esc = html.escape

    def card(project, highlight=False):
        media = project.get('media', [])
        cover = next((item for item in media if item['type'] == 'image'), None)
        photo = f'<img class="project-image" src="{esc(cover["src"])}" alt="{esc(cover["caption"])}" loading="lazy" decoding="async" />' if cover else ''
        tags = ''.join(f'<span>{esc(tag)}</span>' for tag in project['tags'])
        award = f'<p class="award">{esc(project["award"])}</p>' if project.get('award') else ''
        anchor = '' if highlight else f' id="project-{project["id"]}"'
        return f'''<article class="project-card"{anchor}>
              {photo}
              <div class="project-body">
                <p class="project-context">{project['year']} · {esc(project['context'])}</p>
                <div class="project-tags">{tags}</div>
                <h3>{esc(project['title'])}</h3>
                <p>{esc(project['summary'])}</p>
                {award}
                <button class="text-link project-open" data-project="{project['id']}" aria-label="View case study: {esc(project['title'])}">View case study →</button>
              </div>
            </article>'''

    years = sorted({p['year'] for p in projects}, reverse=True)
    highlights = '\n'.join(card(p, True) for p in projects if p.get('highlight'))
    navigation = ''.join(f'<a href="#projects-{year}">{year}</a>' for year in years)
    groups = []
    for year in years:
        cards = '\n'.join(card(p) for p in projects if p['year'] == year)
        groups.append(f'''<details class="project-year" id="projects-{year}" open>
            <summary class="year-heading"><h3 id="year-{year}">{year}</h3></summary>
            <div class="project-grid">{cards}</div>
          </details>''')
    data = json.dumps({p['id']: p for p in projects}, ensure_ascii=False).replace('<', '\\u003c')
    section = f'''{START}
    <section class="section section-alt" id="projects" aria-labelledby="projects-heading">
      <div class="container">
        <div class="section-heading">
          <h2 id="projects-heading">Project Highlights</h2>
          <p class="section-subtitle">Selected work in mechanical design, prototyping, and electromechanical systems.</p>
        </div>
        <div class="project-grid">{highlights}</div>
        <div class="project-archive">
          <h2>Projects by Year</h2>
          <div class="project-year-controls" aria-label="Project year controls" hidden>
            <button class="btn btn-small btn-ghost" type="button" data-project-years="expand">Expand all</button>
            <button class="btn btn-small btn-ghost" type="button" data-project-years="collapse">Collapse all</button>
          </div>
          <nav class="project-year-nav" aria-label="Browse projects by year">{navigation}</nav>
          {''.join(groups)}
        </div>
        <noscript><p>Enable JavaScript to open the detailed case studies. Project summaries and images are available above.</p></noscript>
      </div>
    </section>
    <script type="application/json" id="project-data">{data}</script>
{END}'''
    section = '\n'.join(line.rstrip() for line in section.splitlines())
    index = ROOT / 'index.html'
    content = index.read_text(encoding='utf-8')
    if START in content:
        start, end = content.index(START), content.index(END) + len(END)
    else:
        start = content.index('    <section class="section section-alt" id="projects">')
        end = content.index('    <section class="section" id="experience">', start)
    index.write_text(content[:start] + section + '\n\n' + content[end:].lstrip('\n'), encoding='utf-8')
    print(f'Built {len(projects)} projects across {len(years)} years.')


if __name__ == '__main__':
    build()
