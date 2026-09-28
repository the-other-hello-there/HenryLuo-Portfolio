"""Check the catalog, generated page, and dialogs in locally installed Edge."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
from urllib.parse import quote
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
        if asset['type'] == 'video':
            assert (ROOT / asset['poster']).is_file(), asset['poster']
            assert f'src="{quote(asset["src"])}" aria-label=' in page, asset['src']


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
                       for project in catalog
                       for asset in project['media'] if asset['type'] == 'video')
harness = video_checks + '''<script>
window.addEventListener('load', async () => {
  const failures = [];
  try {
    if (document.documentElement.scrollWidth > innerWidth) failures.push('Page overflows horizontally');
    document.querySelectorAll('.project-card details').forEach(details => details.open = true);
    if (document.documentElement.scrollWidth > innerWidth) failures.push('Expanded resources overflow horizontally');
    document.querySelector('[data-project-years="collapse"]').click();
    if ([...document.querySelectorAll('.project-year')].some(year => year.open)) failures.push('Collapse all');
    document.querySelector('[data-project-years="expand"]').click();
    if ([...document.querySelectorAll('.project-year')].some(year => !year.open)) failures.push('Expand all');
    const ghostVideo = [...document.querySelectorAll('.video-decoder-check')].find(video => video.src.includes('live-demo-web.mp4'));
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 32;
    const context = canvas.getContext('2d', {willReadFrequently: true});
    const pixels = () => { context.drawImage(ghostVideo, 0, 0, 32, 32); return context.getImageData(0, 0, 32, 32).data; };
    const waitForMedia = (video, event, ready) => new Promise((resolve, reject) => {
      if (ready()) return resolve();
      const timer = setTimeout(() => reject(new Error('Timed out waiting for ' + event)), 12000);
      video.addEventListener(event, () => { clearTimeout(timer); resolve(); }, {once: true});
      video.addEventListener('error', () => { clearTimeout(timer); reject(new Error('Video decode failed')); }, {once: true});
    });
    await waitForMedia(ghostVideo, 'loadeddata', () => ghostVideo.readyState >= 2);
    const firstFrame = location.protocol === 'file:' ? null : pixels();
    ghostVideo.currentTime = 2;
    await waitForMedia(ghostVideo, 'seeked', () => !ghostVideo.seeking && ghostVideo.currentTime >= 1.9);
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
    const catCard = document.getElementById('project-feline');
    if (catCard.querySelectorAll('video').length !== 2 || !catCard.querySelector('video').src.endsWith('cat-hype.mp4')) failures.push('Cat showcase and functional demonstrations');
    for (const card of document.querySelectorAll('.project-card')) {
      const supporting = [...card.querySelectorAll('a')].find(a => a.textContent === 'Browse supporting files');
      if (supporting && supporting.parentElement.textContent.trim() !== 'Browse supporting files') failures.push('Supporting link clutter');
    }
    const buttons = [...document.querySelectorAll('.project-open')];
    for (const button of buttons) {
      button.click();
      const modal = document.querySelector('dialog');
      const p = projectData[button.dataset.project];
      if (!modal.open || modal.querySelector('h2').textContent !== p.title) failures.push('Dialog: ' + p.id);
      if (p.outcome && !modal.textContent.includes(p.outcome)) failures.push('Outcome: ' + p.id);
      for (const step of p.iterations || []) {
        if (!modal.textContent.includes(step.before) || !modal.textContent.includes(step.after)) failures.push('Design evolution: ' + p.id);
      }
      for (const link of p.external_links || []) {
        if (![...modal.querySelectorAll('a')].some(a => a.href === link.url)) failures.push('External CAD link: ' + p.id);
      }
      if (p.supporting_page && ![...modal.querySelectorAll('a')].some(a => decodeURIComponent(a.getAttribute('href')) === p.supporting_page)) failures.push('Supporting files: ' + p.id);
      if (modal.textContent.includes('Open video fileDownload video')) failures.push('Joined video links');
      if (p.id === 'sunglasses-holder' && !modal.textContent.includes('nearly two years')) failures.push('Sunglasses field service missing');
      const gallery = p.media;
      if (modal.querySelectorAll('figure').length !== gallery.length) failures.push('Gallery: ' + p.id);
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
    await Promise.all(Object.values(projectData).flatMap(p => p.media.filter(m => m.type === 'image')).map(async asset => {
      const image = new Image(); image.src = asset.src;
      try { await image.decode(); } catch { failures.push('Gallery image decode: ' + asset.src); }
    }));
    const images = [...document.querySelectorAll('.project-card img')];
    images.forEach(img => img.loading = 'eager');
    await new Promise(resolve => setTimeout(resolve, 3000));
    images.forEach(img => { if (!img.complete || !img.naturalWidth) failures.push('Image: ' + img.src); });
    await new Promise(resolve => setTimeout(resolve, 3000));
    document.querySelectorAll('.video-decoder-check').forEach(video => {
      if (video.error || !video.videoWidth || video.readyState < 2) failures.push('Video decoding: ' + video.getAttribute('src'));
    });
    if (firstFrame) {
    const laterFrame = pixels();
    if (!laterFrame.some((value, index) => index % 4 !== 3 && value > 30)) failures.push('Ghost Arm black video frame');
    if (!laterFrame.some((value, index) => index % 4 !== 3 && Math.abs(value - firstFrame[index]) > 10)) failures.push('Ghost Arm frames do not change');
    }
    if (ghostVideo.currentTime < 1.9 || ghostVideo.seeking) failures.push('Ghost Arm seek');
    if (document.querySelector('.cad-load, .cad-resource')) failures.push('Removed CAD controls remain');
    const result = document.createElement('pre');
    result.id = 'browser-check-result';
    result.textContent = JSON.stringify({failures, width: innerWidth, dialogs: buttons.length, images: images.length});
    document.body.append(result);
    await fetch('/__check_result', {method: 'POST', body: result.textContent});
  } catch (error) {
    await fetch('/__check_result', {method: 'POST', body: JSON.stringify({failures: [error.message]})});
  }
});
</script>'''
test_page = ROOT / '.project-check.html'

check_done = threading.Event()
check_report = None

class QuietHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        global check_report
        if self.path != '/__check_result':
            self.send_error(404)
            return
        check_report = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.send_response(200)
        self.end_headers()
        check_done.set()

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
    local_harness = harness.replace("'/__check_result'", f"'http://127.0.0.1:{server.server_port}/__check_result'")
    test_page.write_text(page.replace('</body>', local_harness + '</body>'), encoding='utf-8')
    test_url = test_page.as_uri() if '--file' in sys.argv else f'http://127.0.0.1:{server.server_port}/{test_page.name}'
    for width in (1440, 390):
        profile = Path(tempfile.mkdtemp(prefix='henry-portfolio-edge-')).resolve()
        profile.relative_to(Path(tempfile.gettempdir()).resolve())
        check_done.clear()
        process = subprocess.Popen([str(browser), '--headless', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run',
                                    f'--user-data-dir={profile}', f'--window-size={width},1000',
                                    test_url],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            assert check_done.wait(50), 'Browser checks did not finish within 50 seconds'
            report = check_report
        finally:
            process.terminate()
            process.wait(timeout=10)
        assert not report['failures'], report
        print('PASS browser:', report)
finally:
    server.shutdown()
    server.server_close()
    test_page.unlink(missing_ok=True)
