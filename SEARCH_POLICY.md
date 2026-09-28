# Search discovery and crawler policy

The portfolio sitemap includes the homepage, selected images and videos, the
resume, and all 15 supporting-file pages. The personal-site sitemap also includes
the personal landing page. CAD screenshots remain in the galleries; native CAD,
model archives, the Onshape link, and the 3D viewer were removed at the owner's
request after replacement screenshots were provided.

`scripts/search-selection.json` records approved image/video paths and hashes.
Project dialog fragments are not separate sitemap URLs. Individual supporting files are crawlable resources linked from their project pages.
No project-wide ZIP packages are generated. The illustrated PowerPoint is a sitemap-only Easter egg.

Distinct media is preserved. Reviewed thermal and headwind notes qualify the
experiments' limitations; their problematic full reports were removed. Explicit
project requirements and useful documentation remain. Source-code credential
literals and corresponding code screenshots were sanitized. Engineering claims,
CAD image geometry, and awards are not independently certified by these checks.

## Crawler settings

`robots.txt` asks unlisted compliant crawlers not to crawl this portfolio.
Google's web/image/video crawlers, Bingbot, and LinkedInBot may fetch only the homepage,
its CSS/JavaScript, sitemap, and the approved files, including individual supporting files,
video files, and video posters. Explicit Google-Extended
and Google-CloudVertexBot restrictions cover those product controls. LinkedInBot
is allowed for link previews and documented recruiting integrations; this does
not register the portfolio in LinkedIn Recruiter. No Indeed or Workday crawler
token was verified for indexing candidate portfolios, so none is invented.

For recruiter visibility, add the portfolio link to LinkedIn's Featured section
and contact information where available, and keep it in uploaded resumes and
application website/portfolio fields. LinkedIn Recruiter supports attaching
portfolio links to candidate profiles. Indeed's documented discovery control is
the profile setting **Employers can find you**. Workday employer career sites
collect candidate applications/profiles and can parse uploaded resumes; allowing
a hypothetical Workday crawler would not substitute for submitting those details.
The résumé already contains the portfolio URL. These account changes were not
performed. Unknown sourcing tools remain blocked if they respect robots.txt;
robots.txt cannot recognize whether a generic AI/browser tool is being used by
a recruiter. Human visitors can still open all public links normally.

| Setting | Use |
| --- | --- |
| `User-agent` | Select a crawler's documented token. `*` covers crawlers with no more specific group. |
| `Disallow` | Ask that crawler not to fetch a path. Here the whole portfolio prefix is denied by default. |
| `Allow` | Permit an exception. The generated exact-file rules end with `$` so they do not also permit similarly named backups. |
| `Sitemap` | Advertise the absolute sitemap URL. It does not grant permission to crawl. |
| `#` | Add a comment. |
| `Crawl-delay` | Nonstandard and crawler-dependent; Google ignores it. Not enabled here. |

Specific groups do not inherit the wildcard group's restrictions, which is why
the search group repeats the deny rule before its exceptions. These rules use
Google/Bing-supported end anchors. URL queries are not allowed by the exact-path
exceptions. If you need tracking-query URLs crawled, revise that policy explicitly.

`noindex` is not a supported Google robots.txt directive. To prevent indexing,
use an HTML robots meta tag or an HTTP `X-Robots-Tag` header, with crawling allowed
so the engine can see it. PDF indexing controls need an HTTP header. A blocked
URL can still appear in search based on external links. Sitemap omission also
does not prevent indexing.

Robots rules are voluntary and user-agent strings can be spoofed. They cannot
prevent copying, browser/user-initiated fetches, or downstream reuse. Allowing a
search engine also cannot guarantee that its index is used only for traditional
search. Google-Extended controls specified Gemini training/grounding uses without
removing Google Search eligibility; it is not a universal AI prohibition.
Authentication or server/CDN enforcement is needed for actual access control.
The same files in a public GitHub repository remain available independently of
this website's robots policy.

## Hosting requirement

The current public URL, also printed in the résumé, was verified to return HTTP
200: `https://the-other-hello-there.github.io/HenryLuo-Portfolio/`.

Deploy `sitemap.xml` with this project. However, crawlers will look for robots
rules at **https://the-other-hello-there.github.io/robots.txt**, not at
`/HenryLuo-Portfolio/robots.txt`. Merely publishing this repository's robots file
under the project path does **not** activate its rules.

Install/merge the generated `robots.txt` into the root of the GitHub Pages user
site repository (`the-other-hello-there.github.io`), or configure a custom domain
that serves this portfolio at its root. The generated restrictions are scoped
to `/HenryLuo-Portfolio/` to avoid changing unrelated project sites. Preserve
existing host policies and review overlapping user-agent groups when merging.
The sibling `../GithubMainRepo` contains the user-site repository. Keep its
`robots.txt` and `sitemap.xml` synchronized with the generated portfolio copies.
The host-root robots file was confirmed live during the sitemap investigation.

For a custom domain, first change `site_url` in the manifest, update the canonical
and Open Graph URLs in `index.html`, and regenerate.
Do not publish a sitemap with an unconfirmed replacement hostname. After deploy,
verify HTTP 200 and plain-text content for the host-root robots file, and XML
content for the sitemap. Submit the sitemap URL in Google Search Console and
Bing Webmaster Tools. No deployment or search-console submission was performed.

## Maintaining the selection

Run `python scripts/build_search.py` to regenerate, then
`python scripts/build_search.py --check` to verify hashes and generated output.
The generator uses only Python's standard library. Replacing an approved asset
causes verification to fail until it has been reviewed and its fingerprint
deliberately updated. New catalog files are not automatically added.

Run `python scripts/build_supporting.py` and `python scripts/build_projects.py`
before the search generator. The supporting builder links notes, requirements, extra images, data, and code individually.
Video metadata uses the displayed caption, poster, and content URL. Inclusion
helps discovery but does not guarantee indexing. Sitemap omissions and robots
rules do not make publicly served files private.

Primary references:

- [Google robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)
- [Google crawler and product tokens](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
- [Google image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps)
- [Google video sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps)
- [Bing robots.txt guidance](https://www.bing.com/webmasters/help/how-to-create-a-robots-txt-file-cb7c31ec)
- [LinkedIn's documented LinkedInBot user agent](https://www.linkedin.com/help/recruiter/answer/a6547297)
- [Portfolio links in LinkedIn Recruiter](https://www.linkedin.com/help/linkedin/answer/a416553)
- [LinkedIn Featured work samples](https://www.linkedin.com/help/recruiter/answer/a550399)
- [Indeed profile visibility](https://support.indeed.com/hc/en-us/articles/204524164-Profile-Settings-Menu-Managing-Your-Privacy)
- [Workday career-site candidate profiles and resume parsing](https://doc.workday.com/admin-guide/en-us/human-capital-management/recruiting/career-sites/san1394588983205.html)

Introduction.txt and fullportfolio.pptx are listed in both sitemaps as Easter eggs.
Neither is linked from site pages or explicitly listed in robots.txt. The existing blanket
portfolio restrictions therefore still apply; sitemap discovery does not grant
crawl permission or guarantee indexing.
