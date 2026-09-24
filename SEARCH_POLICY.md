# Search discovery and crawler policy

The sitemap promotes the portfolio homepage, 46 selected project images, and the
existing recruiting résumé. It deliberately does not enumerate the repository.
Selection is an editorial judgment about clear evidence, not a guarantee of how
an employer will react or independent certification of project claims.

## What was reviewed

On September 23, 2026, the review covered the catalog and project descriptions,
contact sheets of the 99 images in project media directories (97 decoded; two
`.jpg` files actually contain HEIC data), extracted report text, the thermal
report page overview, résumé text/layout, and 12 sampled frames from each of the
eight MP4 files. No original media or reports were edited.

The individually approved paths, SHA-256 fingerprints, and reasons are in
`scripts/search-selection.json`. Images are associated with the homepage using
the image sitemap extension. Project dialogs and `#project-...` fragments are
not separate pages, so they are not listed as invented page URLs. Some gallery
images require opening a dialog; sitemap inclusion helps discovery but does not
guarantee indexing. The résumé is a separate document URL.

Specific exclusions:

| Material | Reason |
| --- | --- |
| ME 315 final report | Table 2, 15% infill at 81°C: the printed resistance is 0.147 K·m²/W, while the printed conductivity is 1.35 W/(m·K). With the report's 0.0254 m thickness and `k = L / R`, the latter corresponds to approximately 0.0188 K·m²/W. This apparent inconsistency needs checking against the original data before promoting the PDF. The setup and specimen images remain selected. |
| ME 30801 final report | The conclusion claims the objectives were met and makes practical safety claims, while the discussion documents mounting interference, incomplete similarity, inability to test gusts, and ground-clearance limitations. The existing case-study summary preserves these qualifications. The PDF is withheld from promotion pending technical revision; this is not a finding that the whole experiment lacks value. |
| All eight videos | Sampled frames establish relevance, but all files have audio and neither audio nor uninterrupted playback was reviewed. Under the requested strict verification threshold, none is approved yet. Sampled frames alone cannot certify an entire clip. |
| HRC stress simulation image | Missing visible numerical legend and physical validation context; selected CAD images demonstrate the design without implying tested strength. |
| Other robots in HRC archives | Reference material, not evidence of this project's fabrication. |
| Receipts, raw CAD, ZIP archives, code exports, Office documents and older portfolio exports | Not selected as standalone recruiting evidence; not comprehensively audited. Unknown files are excluded rather than assumed favorable. |
| Duplicate/early/low-detail images | Prefer the selected final build, installed use, and clear CAD views. Per-file catalog decisions are in the manifest. |
| Two construction-step JPGs | The files contain HEIC data despite their extensions; not included. |

The résumé was reviewed for readable presentation and recruiting relevance;
employment, awards, credentials, and ownership claims were not independently
verified. Public project descriptions retain their existing attribution and
limitations. Exclusion from this sitemap does not remove links from the portfolio
or make a file private.

## Crawler settings

`robots.txt` asks unlisted compliant crawlers not to crawl this portfolio.
Google's web/image/video crawlers, Bingbot, and LinkedInBot may fetch only the homepage,
its CSS/JavaScript, sitemap, and the approved files. Explicit Google-Extended
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

## Hosting requirement — action still needed

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
This workspace does not contain that user-site repository, so that host-level
change has not been made.

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

Before promoting a report, read every page, check numerical consistency and
claims, and review annotations and personal information. Before promoting a
video, watch and listen to the entire clip. A video sitemap entry additionally
needs a suitable public thumbnail, truthful title/description, content URL and
actual landing page. The current generator deliberately supports only reviewed
images and documents; extend it for the video namespace after full review.

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
