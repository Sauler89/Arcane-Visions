"""Exercise real WeiDU against synthetic resources; no game rendering implied."""
from pathlib import Path
import tempfile, struct, subprocess, shutil, json, sys

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'sr_original_spell_animations'
CONFIG = json.loads((MOD / 'docs/test_config.json').read_text())
SPELLS = CONFIG['spells']
WEIDU = Path(sys.argv[1] if len(sys.argv) > 1 else (shutil.which('weidu') or 'weidu')).resolve()


def effect(op, target=2, duration=60, res='', timing=0, where=0):
    b = bytearray(48)
    struct.pack_into('<H', b, 0, op)
    b[2:4] = bytes([target, 4])
    struct.pack_into('<I', b, 8, where)
    b[12:14] = bytes([timing, 1])
    struct.pack_into('<I', b, 14, duration)
    b[18] = 100
    b[20:28] = res.encode().ljust(8, b'\0')
    struct.pack_into('<IIi', b, 28, 3, 6, -2)
    return bytes(b)


def spl(mantle=False, ability_target=1):
    b = bytearray(0x72 + 3 * 40)
    b[:8] = b'SPL V1  '
    b[58:66] = b'ICONOLDc'
    struct.pack_into('<I', b, 52, 7)
    struct.pack_into('<IHIHH', b, 100, 114, 3, len(b), 0, 2)
    effects = [effect(141, res='GLOBAL'), effect(50)]
    for i in range(3):
        h = 114 + i * 40
        b[h] = 1
        b[h + 12] = ability_target
        b[h + 4:h + 12] = b'ICONOLDb'
        struct.pack_into('<H', b, h + 16, 1 + i * 10)
        current = [effect(12, duration=3600), effect(67, res='ORIGCRE', timing=1),
                   effect(177, res='ORIGEFF'), effect(215, res='OLDVVC', duration=600, where=1),
                   effect(141), effect(142)]
        if mantle:
            protection = bytearray(effect(120, target=1, duration=24 * (i + 1)))
            protection[3] = 7
            protection[13] = 3
            protection[18:20] = bytes([91, 7])
            struct.pack_into('<Ii', protection, 36, 1, -3)
            current.append(bytes(protection))
        struct.pack_into('<HH', b, h + 30, len(current), len(effects))
        struct.pack_into('<H', b, h + 38, 73)
        effects.extend(current)
    return bytes(b) + b''.join(effects)


def parse(b):
    ao, n, eo = struct.unpack_from('<IHI', b, 100)
    idx, cnt = struct.unpack_from('<HH', b, 110)
    globals_ = [b[eo + (idx + j) * 48:eo + (idx + j + 1) * 48] for j in range(cnt)]
    headers = []
    for i in range(n):
        h = b[ao + i * 40:ao + (i + 1) * 40]
        cnt, idx = struct.unpack_from('<HH', h, 30)
        effects = [b[eo + (idx + j) * 48:eo + (idx + j + 1) * 48] for j in range(cnt)]
        headers.append((h, effects))
    return globals_, headers


def opcode(e):
    return struct.unpack_from('<H', e)[0]


def assert_preserved(original, patched, spell):
    assert patched[:106] == original[:106], spell
    assert patched[110:114] == original[110:114], spell
    g, h = parse(original)
    ng, nh = parse(patched)
    assert g == ng and len(h) == len(nh), spell
    for (head, effects), (nhead, neffects) in zip(h, nh):
        assert head[:30] == nhead[:30] and head[34:] == nhead[34:], spell
        assert [e for e in effects if opcode(e) not in (141, 215)] == [
            e for e in neffects if opcode(e) not in (141, 215)], spell
    return nh


GAME = Path(tempfile.mkdtemp(prefix='sra-weidu-test-'))
try:
    shutil.copytree(ROOT, GAME, dirs_exist_ok=True)
    automatic_installer = GAME / 'setup-sr_original_spell_animations'
    shutil.copy2(WEIDU, automatic_installer)
    automatic_installer.chmod(automatic_installer.stat().st_mode | 0o111)
    override = GAME / 'override'
    override.mkdir()
    (GAME / 'chitin.key').write_bytes(b'KEY V1  ' + struct.pack('<IIII', 0, 0, 24, 24))
    (GAME / 'dialog.tlk').write_bytes(b'TLK V1  ' + struct.pack('<HII', 0, 1, 44) + bytes(26))
    (override / 'eet.flag').write_bytes(b'EET fixture')

    def path(name):
        return next(p for p in override.iterdir() if p.name.lower() == name.lower())

    def snapshot():
        files = list(override.iterdir())
        result = {p.name.lower(): p.read_bytes() for p in files}
        assert len(result) == len(files), 'duplicate filenames differing only by case'
        return result

    def run(*args, language=0, expect_success=True, autodetect=False):
        command = [str(automatic_installer)] if autodetect else [str(WEIDU), 'sr_original_spell_animations/setup-sr_original_spell_animations.tp2']
        p = subprocess.run([*command,
                            '--noautoupdate', '--language', str(language), '--no-exit-pause', *args],
                           cwd=GAME, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert bool(p.returncode == 0) == expect_success, p.stdout
        return p.stdout

    originals = {}
    for spell, _, _, where, _, persistent in SPELLS:
        original = spl(mantle=bool(persistent), ability_target=4 if where == 2 else 5 if spell in ('SPWI212', 'SPWI505', 'SPPR609', 'SPWI708') else 1)
        originals[spell] = original
        (override / (spell.lower() + '.spl')).write_bytes(original)
    for spell in ['spwi118', 'sppr105', 'spwi112', 'spwi526', 'spwi802', 'spwi403']:
        (override / (spell + '.spl')).write_bytes(spl())
    for name in ['spentaai', 'spentaci', 'spchrorb', 'spmagglo']:
        (override / (name + '.bam')).write_bytes(b'old native bam')
    (override / 'spmagglo.vvc').write_bytes(b'old native vvc')
    (override / 'origeff.eff').write_bytes(b'original summon eff sentinel')
    (override / 'unchanged.itm').write_bytes(b'item with icons remains unchanged')
    before = snapshot()
    tlk = (GAME / 'dialog.tlk').read_bytes()
    for profile, language in [('EET', 0), ('BG2EE', 1)]:
        if profile == 'BG2EE':
            path('eet.flag').unlink()
            (override / 'oh6000.are').write_bytes(b'BG2EE fixture')
            before = snapshot()
        run('--force-install-list', '0', language=language, autodetect=(profile == 'EET'))
        for spell, vvc, target, where, duration, persistent in SPELLS:
            nh = assert_preserved(originals[spell], path(spell + '.spl').read_bytes(), spell)
            for i, (_, effects) in enumerate(nh):
                visuals = [e for e in effects if opcode(e) == 215]
                assert len(visuals) == (2 if spell == 'SPPR609' else 1), spell
                e = visuals[0]
                assert e[2] == target and struct.unpack_from('<I', e, 8)[0] == where, spell
                assert e[20:28].split(b'\0')[0].lower() == vvc.encode(), spell
                assert struct.unpack_from('<I', e, 14)[0] == (24 * (i + 1) if persistent else duration if spell == 'SPPR609' else 0), spell
                assert e[12] == (0 if persistent or spell == 'SPPR609' else 1), spell
                if persistent:
                    protection = next(e for e in effects if opcode(e) == 120)
                    for start, end in [(2, 4), (12, 20), (36, 44)]:
                        assert e[start:end] == protection[start:end], spell
                if spell == 'SPPR609':
                    second = visuals[1]
                    assert second[12] == 3 and struct.unpack_from('<I', second, 14)[0] == 3
                    assert second[20:28].split(b'\0')[0] == b'srasun2'
        for name in ['spwi118.spl', 'sppr105.spl', 'spwi112.spl', 'spwi526.spl',
                     'spwi802.spl', 'spwi403.spl', 'origeff.eff', 'unchanged.itm']:
            assert path(name).read_bytes() == before[name], name
        assert (GAME / 'dialog.tlk').read_bytes() == tlk
        for _, dest, _, kind in CONFIG['assets']:
            assert path(dest).read_bytes() == (MOD / 'assets' / kind / dest).read_bytes(), dest
        installed = snapshot()
        run('--force-install-list', '0', language=language)
        assert snapshot() == installed, 'reinstallation must be stable'
        run('--force-uninstall-list', '0', language=language)
        assert snapshot() == before, 'uninstall must restore bytes and remove new resources'
        print('PASS:', profile, 'install, reinstall, uninstall; 16 spells x 3 headers; mechanics/icons/globals/projectiles/TLK preserved')

    # Reject truncated global/ability tables and shared or unordered effect blocks.
    def mutate(offset, fmt, value):
        b = bytearray(spl())
        struct.pack_into(fmt, b, offset, value)
        return bytes(b)

    invalid = [b'SPL V1  ', b'BAD V1  ' + spl()[8:], mutate(100, '<I', 0xfffffff0),
               mutate(104, '<H', 65535), mutate(106, '<I', 100), mutate(106, '<I', 0xfffffff0),
               mutate(110, '<H', 65535), mutate(112, '<H', 65535),
               mutate(114 + 30, '<H', 65535), mutate(114 + 32, '<H', 65535),
               mutate(114 + 32, '<H', 0), mutate(154 + 32, '<H', 2),
               mutate(104, '<H', 0)]
    for spell, *_ in SPELLS:
        path(spell + '.spl').unlink()
    for (spell, *_), data in zip(SPELLS, invalid):
        (override / (spell.lower() + '.spl')).write_bytes(data)
    for name in ['spentaai.bam', 'spmagglo.bam', 'spmagglo.vvc']:
        path(name).unlink()
    before = snapshot()
    run('--force-install-list', '0')
    for (spell, *_), data in zip(SPELLS, invalid):
        assert path(spell + '.spl').read_bytes() == data, spell
    run('--force-uninstall-list', '0')
    assert snapshot() == before
    print('PASS: 13 malformed/unsupported layouts, missing spells and missing native resources skipped safely')

    # A nonstandard Mantle using an external buff falls back to its old aura.
    mantle = spl(mantle=False, ability_target=5)
    path('spwi708.spl').write_bytes(mantle)
    before = snapshot()
    run('--force-install-list', '0')
    nh = assert_preserved(mantle, path('spwi708.spl').read_bytes(), 'Mantle fallback')
    assert all(struct.unpack_from('<I', next(e for e in es if opcode(e) == 215), 14)[0] == 600 for _, es in nh)
    run('--force-uninstall-list', '0')
    assert snapshot() == before
    print('PASS: Mantle follows weapon protection despite longer unrelated effects; old-aura fallback verified')

    # Empty but valid ability blocks can still receive an independent visual.
    empty = bytearray(spl())
    for i in range(3):
        struct.pack_into('<HH', empty, 114 + i * 40 + 30, 0, 2)
    path('spwi206.spl').write_bytes(empty)
    # No direct protection and no existing attached aura: explicit fallback.
    fallback = bytearray(mantle)
    ao, n, eo = struct.unpack_from('<IHI', fallback, 100)
    for i in range(n):
        cnt, idx = struct.unpack_from('<HH', fallback, ao + i * 40 + 30)
        for j in range(cnt):
            pos = eo + (idx + j) * 48
            if struct.unpack_from('<H', fallback, pos)[0] == 215:
                struct.pack_into('<H', fallback, pos, 121)
    path('spwi708.spl').write_bytes(fallback)
    (override / 'spmagglo.bam').write_bytes(b'old native bam')
    before = snapshot()
    output = run('--force-install-list', '0')
    assert '24s fallback' in output
    nh = assert_preserved(bytes(fallback), path('spwi708.spl').read_bytes(), 'Mantle 24s fallback')
    assert all(struct.unpack_from('<I', next(e for e in es if opcode(e) == 215), 14)[0] == 24 for _, es in nh)
    nh = assert_preserved(bytes(empty), path('spwi206.spl').read_bytes(), 'empty ability')
    assert all(len(es) == 1 and opcode(es[0]) == 215 for _, es in nh)
    assert path('spmagglo.vvc').read_bytes() == (MOD / 'assets/native/spmagglo.vvc').read_bytes()
    run('--force-uninstall-list', '0')
    after = snapshot()
    assert after == before, {'added': sorted(after.keys() - before.keys()), 'removed': sorted(before.keys() - after.keys()), 'changed': sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}
    print('PASS: empty ability blocks, explicit 24s fallback and missing native SPMAGGLO VVC')

    # Unsupported games must fail before copying any assets.
    path('oh6000.are').unlink()
    before = snapshot()
    output = run('--force-install-list', '0')
    assert 'SKIPPING:' in output, output
    assert snapshot() == before
    print('PASS: unsupported-game guard leaves all resources unchanged')

    # Optional format coverage on real supplied SR files (still no game runtime).
    if len(sys.argv) > 2:
        source = Path(sys.argv[2]).resolve()
        (override / 'eet.flag').write_bytes(b'EET fixture')
        source_originals = {}
        for spell, *_ in SPELLS:
            original = next(source.rglob(spell.lower() + '.spl')).read_bytes()
            source_originals[spell] = original
            matches = [p for p in override.iterdir() if p.name.lower() == spell.lower() + '.spl']
            destination = matches[0] if matches else override / (spell.lower() + '.spl')
            destination.write_bytes(original)
        before = snapshot()
        run('--force-install-list', '0')
        for spell, vvc, *_ in SPELLS:
            nh = assert_preserved(source_originals[spell], path(spell + '.spl').read_bytes(), spell)
            assert all(any(opcode(e) == 215 and e[20:28].split(b'\0')[0].lower() == vvc.encode()
                           for e in effects) for _, effects in nh), spell
        run('--force-uninstall-list', '0')
        assert snapshot() == before
        print('PASS: actual SR source SPL layouts patched; nonvisual effect bytes preserved and uninstall restored originals')
finally:
    shutil.rmtree(GAME)
