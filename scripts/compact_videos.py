"""Prepare and validate smaller browser-compatible MP4 replacements.

Outputs a migration manifest; originals are backed up outside the website.
Requires ffmpeg and ffprobe. Existing efficient MP4s are left unchanged.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / 'assets/project_descriptions'
WORK = ROOT / '.tmp-video-conversion'
WORK.mkdir(exist_ok=True)
backup = Path(tempfile.mkdtemp(prefix='henry-original-videos-'))


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def video(info):
    return next(s for s in info['streams'] if s['codec_type'] == 'video')


record = {'backup': str(backup), 'entries': []}
files = sorted(p for p in PROJECTS.rglob('*') if p.suffix.lower() in {'.mp4', '.mov', '.m4v', '.avi', '.webm'})
for number, source in enumerate(files):
    original = probe(source)
    stream = video(original)
    duration = float(original['format']['duration'])
    relative = source.relative_to(ROOT)
    # Avoid unnecessary generation loss on already compact, compatible clips.
    if source.suffix == '.mp4' and stream['codec_name'] == 'h264' and source.stat().st_size * 8 / duration < 1600000:
        print('Keep efficient:', relative, flush=True)
        continue
    candidate = WORK / f'{number}.mp4'
    filters = []
    hdr = stream.get('color_transfer') in {'arib-std-b67', 'smpte2084'}
    if hdr:
        filters += ['zscale=t=linear:npl=100', 'format=gbrpf32le', 'zscale=p=bt709', 'tonemap=tonemap=mobius:desat=0', 'zscale=t=bt709:m=bt709:r=limited']
    filters += ['scale=trunc(iw/2)*2:trunc(ih/2)*2', 'format=yuv420p']
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
               '-map', '0:v:0', '-map', '0:a:0?', '-map_metadata', '-1', '-vf', ','.join(filters),
               '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-maxrate', '3M', '-bufsize', '6M',
               '-threads', '4', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
               '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', str(candidate)]
    print('Encode:', relative, flush=True)
    subprocess.run(command, check=True)
    result = probe(candidate)
    assert abs(float(result['format']['duration']) - duration) < 0.25, relative
    assert sum(s['codec_type'] == 'audio' for s in original['streams']) == sum(s['codec_type'] == 'audio' for s in result['streams']), relative
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(candidate), '-f', 'null', '-'], check=True)
    saving = 1 - candidate.stat().st_size / source.stat().st_size
    if saving < 0.15 and source.suffix.lower() == '.mp4':
        candidate.unlink()
        print('Keep original: savings below 15%', flush=True)
        continue
    name = re.sub(r'[^a-z0-9]+', '-', source.stem.lower()).strip('-') + '.mp4'
    target = source.with_name(name) if source.suffix != '.mp4' else source
    assert target == source or not target.exists(), target
    saved = backup / relative
    saved.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, saved)
    record['entries'].append({'source': relative.as_posix(), 'target': target.relative_to(ROOT).as_posix(),
                              'candidate': candidate.relative_to(ROOT).as_posix(), 'before': source.stat().st_size,
                              'after': candidate.stat().st_size, 'original_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                              'sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(), 'hdr_to_sdr': hdr,
                              'duration': duration})
    (WORK / 'manifest.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(f'Validated: {saving:.0%} smaller', flush=True)
print('Prepared replacements; recovery copies:', backup, flush=True)
