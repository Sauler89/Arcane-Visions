# BGEE support — v0.2.0-beta.11

Both components now accept Baldur's Gate: Enhanced Edition, with or without
Siege of Dragonspear, as well as BG2EE and EET. Previously both used
`REQUIRE_PREDICATE (GAME_IS ~eet bg2ee~) @1`, which excluded BGEE before
any animation could be installed. The predicate now lists `bgee bg2ee eet`.
WeiDU identifies BGEE+SoD as BGEE; no separate `GAME_IS ~sod~` is needed.

The graphics patchers already check whether the target resources exist.
Missing BG2 spells are skipped, not created in BGEE. Component 10 also checks
the recognized visual layout, root/child and temporary-weapon links, and
projectile layout. Unfamiliar or missing routes are skipped and logged.
The artwork, spell mappings, state opcodes and spell mechanics are unchanged.
No fireball component is included in this update.

Install after other spell-changing mods; on EET, also after EET_end. Users
whose previous attempt was skipped should download the updated repository
package, replace the mod folder and installer, and run the installer again.

## Verification

`tests/verify_bgee.py` runs real WeiDU 251 against synthetic resources and a
minimal KEY/TLK fixture. It reproduces the previous rejection, then checks:

- Both components independently and together, English and Italiano, on BGEE,
  BGEE+SoD, BG2EE and EET profiles.
- Install, stable reinstall, exact uninstall, both component orders and partial
  uninstall retaining the other component.
- Low-level existing spells change as intended; missing higher-level spells
  remain absent. Missing BG2 weapon/projectile routes are skipped.
- Nonvisual effects, casting effects, icons, Sanctuary state/duration and
  unrelated resources remain unchanged.
- IWDEE, PSTEE and classic BG1/BG2 are still skipped before resource writes.

All **40 cases passed**. See [BGEE_validation.json](BGEE_validation.json).
The existing component-0 installer suite now also tests BGEE alongside EET
and BG2EE. Asset integrity and the existing regression suite were rerun.

These are installer and binary-resource checks. They do not use a real BGEE
resource export, run the bundled Windows executable, or launch the game.
They establish that the reported game predicate rejection is resolved;
visual rendering and Melcar's specific modded installation still need testing
in his game.

## Reproduce

```sh
python3 tests/verify_bgee.py /path/to/weidu /path/to/results
python3 tests/verify_installer.py /path/to/weidu
python3 tests/verify_regressions.py /path/to/weidu
python3 tests/verify_graphics_integrity.py
```

The older repository/source audit reports describe their recorded beta and
EET baseline; this update does not relabel them as BGEE game tests.
