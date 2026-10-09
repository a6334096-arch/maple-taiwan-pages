"""Verify the portable static package without altering files."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parent
places = json.loads((root / 'places.json').read_text(encoding='utf-8'))
seasons = json.loads((root / 'seasons.json').read_text(encoding='utf-8'))
foliage = json.loads((root / 'foliage.json').read_text(encoding='utf-8'))
ids = {p['id'] for p in places}
assert len(ids) == len(places)
assert ids == {k for k in seasons if not k.startswith('_')}
assert ids == set(foliage['foliage'])
photos = 0
for p in places:
    assert 21.8 <= p['lat'] <= 25.5 and 119.5 <= p['lon'] <= 122
    for photo in p.get('historical_photos', []):
        for field in ('src', 'large_src'):
            value = photo.get(field)
            if value and value.startswith('./photos/'):
                assert (root / value).is_file(), value
            assert not (value or '').startswith('/photos/'), 'Root path breaks project Pages'
        photos += 1
html = (root / 'index.html').read_text(encoding='utf-8')
for marker in ('terrain-shading', 'county-labels', 'town-labels', 'markers', 'mountain', 'high-mountain'):
    assert marker in html, marker
for value in re.findall(r'(?:src|href)=["\']([^"\']+)', html):
    if not value.startswith(('http:', 'https:', '#', 'data:')) and value != './':
        assert (root / value).exists(), value
assert '@media' in (root / 'style.css').read_text(encoding='utf-8')
assert 'setInterval' in (root / 'app.js').read_text(encoding='utf-8')
print(f'PASS: {len(places)} places, separate seasonal/foliage JSON, {photos} photos, map layers, responsive CSS.')
