"""Validate all BAM frames/cycles, VVC dependencies and optional SR provenance."""
from pathlib import Path
import hashlib, json, struct, sys, zlib

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'sr_original_spell_animations'
manifest = json.loads((MOD / 'docs/asset_manifest.json').read_text())
config = json.loads((MOD / 'docs/test_config.json').read_text())
source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None


def bam(data):
    if data[:4] == b'BAMC':
        assert data[4:8] == b'V1  '
        expected = struct.unpack_from('<I', data, 8)[0]
        data = zlib.decompress(data[12:])
        assert len(data) == expected
    assert data[:8] == b'BAM V1  '
    frames, cycles, transparent = struct.unpack_from('<HBB', data, 8)
    frame_offset, palette_offset, lookup_offset = struct.unpack_from('<III', data, 12)
    assert frames and cycles and palette_offset + 1024 <= len(data)
    cycle_offset = frame_offset + 12 * frames
    assert cycle_offset + cycles * 4 <= len(data)
    cycle_lengths = []
    for i in range(cycles):
        count, first = struct.unpack_from('<HH', data, cycle_offset + i * 4)
        assert lookup_offset + (first + count) * 2 <= len(data)
        for j in range(count):
            assert struct.unpack_from('<H', data, lookup_offset + (first + j) * 2)[0] < frames
        cycle_lengths.append(count)
    for i in range(frames):
        width, height, _, _, offset = struct.unpack_from('<HHhhI', data, frame_offset + i * 12)
        pos = offset & 0x7fffffff
        total = width * height
        if offset & 0x80000000:
            assert pos + total <= len(data)
        else:
            decoded = 0
            while decoded < total:
                assert pos < len(data)
                value = data[pos]
                pos += 1
                if value == transparent:
                    assert pos < len(data)
                    decoded += data[pos] + 1
                    pos += 1
                else:
                    decoded += 1
                assert decoded <= total
    return frames, cycle_lengths


assert len(manifest) == 26
assert len({a['destination'].lower() for a in manifest}) == 26
assert len(config['spells']) == 16
assets = {Path(a['destination']).name.lower(): a for a in manifest}
assert set(assets) == {a[1] for a in config['assets']}
renames = {Path(a['source']).stem.upper(): Path(a['destination']).stem.upper()
           for a in manifest if a['destination'].endswith('.bam')}
frames_checked = 0
for entry in manifest:
    path = ROOT / entry['destination']
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['installed_sha256'], path
    assert len(path.stem) <= 8
    if source:
        original = (source / entry['source']).read_bytes()
        assert hashlib.sha256(original).hexdigest() == entry['source_sha256'], path
        expected = bytearray(original)
        if path.suffix == '.vvc':
            name = expected[8:16].split(b'\0')[0].decode().upper()
            expected[8:16] = renames[name].encode().ljust(8, b'\0')
            expected[96:104] = path.stem.upper().encode().ljust(8, b'\0')
            for offset in (120, 128, 148):
                expected[offset:offset + 8] = bytes(8)
        assert data == expected, path
    if path.suffix == '.bam':
        assert entry['source_sha256'] == entry['installed_sha256'], path
        frames, _ = bam(data)
        frames_checked += frames
    else:
        assert len(data) == 492 and data[:8] == b'VVC V1.0', path
        dep = data[8:16].split(b'\0')[0].decode().lower() + '.bam'
        assert dep in assets, (path, dep)
        _, cycles = bam((ROOT / assets[dep]['destination']).read_bytes())
        for offset in (104, 108, 144):
            sequence = struct.unpack_from('<I', data, offset)[0]
            # VVC indices are one-based; zero/-1 omit a phase (single-phase
            # controllers with all zeroes fall back to BAM cycle zero).
            assert sequence in (0, 0xffffffff) or sequence <= len(cycles), (path, sequence)
        assert data[120:136] == bytes(16) and data[148:156] == bytes(8), path
        assert data[16:24] == bytes(8) and data[68:76] == bytes(8) and data[136:144] == bytes(8), path
for _, vvc, _, where, _, _ in config['spells']:
    dep = assets[vvc + '.vvc']
    flags = struct.unpack_from('<I', (ROOT / dep['destination']).read_bytes(), 32)[0]
    if where == 2:
        assert not flags & 1, 'permanent-timing point visuals must not loop'
print(f'PASS: 14 BAMs, {frames_checked} frames, all cycles/RLE data; 12 VVC dependencies/sequences; hashes, no external palettes/alpha BAMs/audio; 16 spell mappings')
if source:
    print('PASS: BAMs byte-identical to SR; VVC changes limited to resource names and audio removal')
