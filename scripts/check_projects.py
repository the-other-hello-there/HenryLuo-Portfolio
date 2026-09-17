"""Check the catalog, generated page, and dialogs in locally installed Edge."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'assets/data/projects.json').read_text(encoding='utf-8'))
page = (ROOT / 'index.html').read_text(encoding='utf-8')
embedded = json.loads(re.search(r'<script type="application/json" id="project-data">(.*?)</script>', page, re.S)[1])
assert embedded == {p['id']: p for p in catalog}, 'Rebuild the page after editing the catalog.'
assert len(embedded) == len(catalog)
for p in catalog:
    for document in p.get('documents', []):
        assert (ROOT / document['src']).is_file(), document['src']
    for asset in p['media']:
        assert (ROOT / asset['src']).is_file(), asset['src']


class PageCheck(HTMLParser):
    ids = []
    buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'data-project' in attrs:
            self.buttons.append(attrs['data-project'])


parser = PageCheck()
parser.feed(page)
assert len(parser.ids) == len(set(parser.ids)), 'Duplicate HTML IDs'
assert set(parser.buttons) == set(embedded)
assert len(parser.buttons) == len(catalog) + sum(bool(p.get('highlight')) for p in catalog)
print(f'PASS: {len(catalog)} catalog entries, {len(parser.buttons)} cards, all media paths, and unique IDs.')

browser = Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')) / 'Microsoft/Edge/Application/msedge.exe'
if not browser.is_file():
    raise SystemExit('Edge is unavailable; browser verification was not run.')

video_checks = ''.join(f'<video class="video-decoder-check" hidden preload="auto" muted src="{asset["src"]}"></video>'
                       for project in catalog if project['id'] in ('motor-mount', 'ghost-arm', 'battle-bot')
                       for asset in project['media'] if asset['type'] == 'video')
harness = video_checks + '''<script>
window.addEventListener('load', async () => {
  const failures = [];
  try {
    if (document.documentElement.scrollWidth > innerWidth) failures.push('Page overflows horizontally');
    document.querySelector('[data-project-years="collapse"]').click();
    if ([...document.querySelectorAll('.project-year')].some(year => year.open)) failures.push('Collapse all');
    document.querySelector('[data-project-years="expand"]').click();
    if ([...document.querySelectorAll('.project-year')].some(year => !year.open)) failures.push('Expand all');
    const ghostVideo = [...document.querySelectorAll('.video-decoder-check')].find(video => video.src.includes('live-demo-web.mp4'));
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 32;
    const context = canvas.getContext('2d', {willReadFrequently: true});
    const pixels = () => { context.drawImage(ghostVideo, 0, 0, 32, 32); return context.getImageData(0, 0, 32, 32).data; };
    const firstFrame = pixels();
    ghostVideo.currentTime = 2;
    for (const year of document.querySelectorAll('details.project-year')) {
      const summary = year.querySelector('summary');
      year.open = true;
      summary.click();
      if (year.open) failures.push('Collapse: ' + year.id);
      summary.click();
      if (!year.open) failures.push('Expand: ' + year.id);
      year.open = false;
      document.querySelector(`.project-year-nav a[href="#${year.id}"]`).click();
      if (!year.open) failures.push('Year navigation: ' + year.id);
    }
    const buttons = [...document.querySelectorAll('.project-open')];
    for (const button of buttons) {
      button.click();
      const modal = document.querySelector('dialog');
      const p = projectData[button.dataset.project];
      if (!modal.open || modal.querySelector('h2').textContent !== p.title) failures.push('Dialog: ' + p.id);
      if (p.outcome && !modal.textContent.includes(p.outcome)) failures.push('Outcome: ' + p.id);
      if (modal.querySelectorAll('figure').length !== p.media.length) failures.push('Gallery: ' + p.id);
      for (const document of p.documents || []) {
        if (![...modal.querySelectorAll('a')].some(link => link.textContent === document.label)) failures.push('Report link: ' + p.id);
      }
      if (p.id === 'motor-mount') {
        const video = modal.querySelector('video');
        if (!video || !video.controls || !video.src.endsWith('vertical-hover.mp4')) failures.push('Dodo video controls');
      }
      if (modal.scrollWidth > modal.clientWidth) failures.push('Dialog overflow: ' + p.id);
      document.querySelector('.dialog-close').click();
      if (modal.open) failures.push('Close: ' + p.id);
    }
    const images = [...document.querySelectorAll('.project-card img')];
    images.forEach(img => img.loading = 'eager');
    await new Promise(resolve => setTimeout(resolve, 3000));
    images.forEach(img => { if (!img.complete || !img.naturalWidth) failures.push('Image: ' + img.src); });
    await new Promise(resolve => setTimeout(resolve, 3000));
    document.querySelectorAll('.video-decoder-check').forEach(video => {
      if (video.error || !video.videoWidth || video.readyState < 2) failures.push('Video decoding: ' + video.getAttribute('src'));
    });
    const laterFrame = pixels();
    if (!laterFrame.some((value, index) => index % 4 !== 3 && value > 30)) failures.push('Ghost Arm black video frame');
    if (!laterFrame.some((value, index) => index % 4 !== 3 && Math.abs(value - firstFrame[index]) > 10)) failures.push('Ghost Arm frames do not change');
    if (ghostVideo.currentTime < 1.9 || ghostVideo.seeking) failures.push('Ghost Arm seek');
    const result = document.createElement('pre');
    result.id = 'browser-check-result';
    result.textContent = JSON.stringify({failures, width: innerWidth, dialogs: buttons.length, images: images.length});
    document.body.append(result);
  } catch (error) {
    document.body.setAttribute('data-check-error', error.message);
  }
});
</script>'''
test_page = ROOT / '.project-check.html'

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args):
        pass

    def do_GET(self):
        # Video seeking requires byte-range responses, as on the deployed host.
        path = Path(self.translate_path(self.path))
        try:
            if path.suffix.lower() != '.mp4' or not path.is_file():
                return super().do_GET()
            size = path.stat().st_size
            match = re.fullmatch(r'bytes=(\d+)-(\d*)', self.headers.get('Range', ''))
            start = int(match[1]) if match else 0
            end = min(int(match[2]), size - 1) if match and match[2] else size - 1
            self.send_response(206 if match else 200)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(end - start + 1))
            if match:
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            with path.open('rb') as source:
                source.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk = source.read(min(65536, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass

server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    test_page.write_text(page.replace('</body>', harness + '</body>'), encoding='utf-8')
    for width in (1440, 390):
        profile = Path(tempfile.mkdtemp(prefix='henry-portfolio-edge-')).resolve()
        profile.relative_to(Path(tempfile.gettempdir()).resolve())
        result = subprocess.run([str(browser), '--headless', '--disable-gpu', '--no-first-run',
                                 f'--user-data-dir={profile}', f'--window-size={width},1000',
                                 '--virtual-time-budget=10000', '--dump-dom', f'http://127.0.0.1:{server.server_port}/{test_page.name}'],
                                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
        match = re.search(r'<pre id="browser-check-result">(.*?)</pre>', result.stdout, re.S)
        if not match:
            print(result.stdout[-2000:])
            print(result.stderr[-2000:])
            raise AssertionError('Browser checks did not complete: ' + str(result.returncode))
        report = json.loads(match[1])
        assert not report['failures'], report
        print('PASS browser:', report)
finally:
    server.shutdown()
    server.server_close()
    test_page.unlink(missing_ok=True)
