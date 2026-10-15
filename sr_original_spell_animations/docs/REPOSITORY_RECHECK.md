# Repository recheck — historical beta.10

Review dated 2026-10-12 of beta.9 and its beta.10 fix. This report records
that baseline, not the smaller English-only beta.12 selection. No EET game
was launched. See [ENGLISH_AND_DOORS.md](ENGLISH_AND_DOORS.md) for beta.12.

## Reproduced installer fault

A PROJECTL.IDS SRIOSORB symbol without SRIOSORB.PRO caused ADD_PROJECTILE
to skip creation. Beta.9 still assigned its index to SORB (7778 in the
reproduction), leaving a missing projectile. FILE_EXISTS_IN_GAME alone did
not detect this registry-only collision. Beta.10 checks SRIOSORB in both
PROJECTL.IDS and MISSILE.IDS case-insensitively before writes. A collision
fails only the IWDEE component with an explicit message. Three cases cover
either registry separately and both together without a PRO.

## Recorded checks

| Check on the beta.10 baseline | Result |
|---|---|
| 42 BAMs, 1,429 frames, palettes, cycles and RLE | PASS |
| 38 VVCs, dependencies, phases and source correspondence | PASS |
| 15 GIFs and source hashes (three elemental previews were added later) | PASS |
| 44 exported EET SPLs and two ITMs, standalone/combined installs | PASS |
| Stable reinstall, exact uninstall, reverse component order, partial uninstall | PASS |
| Both then-available installer languages and unchanged TLK | PASS |
| 24 projectile cases including IDS-only collisions | PASS |
| 30 item, 44 overlay, 12 child and 28 regression cases | PASS |
| Six Chaos double-cue cases with independent conditions | PASS |
| EET/BG2EE synthetic profiles and actual SR source layouts | PASS |
| IWDEE builder byte-exact reproduction | PASS |
| Bundled Windows WeiDU 251 matches official bytes | PASS; not executed on Windows |
| 861 source BAM decisions and eight archive hashes | PASS |
| Web/Horrid Wilting unchanged, private assets absent | PASS |

SORB clones installed PFIRE3, changing only BAM flags/reference/orientation;
root SPPR614 and original PFIRE3 remain identical. Call Lightning changes
shared SKYBOLT artwork, not SPL/PRO data or hardcoded chain indexes. Neither
source gameplay nor icons are imported. The source summary reads VERSION
from the TP2 rather than a separate hardcoded version.

38 distinct IWDEE BAM candidates and three phases of included BAMs remain
unintegrated: delayed Regeneration HEALH and Glitterdust spread/ring. Declared
PRO references are not proof that each phase is activated. Tests execute
WeiDU on export copies with minimal KEY/TLK; they do not demonstrate universal
modlist compatibility or engine rendering. Position, blending and timing
need game confirmation, especially the hardcoded lightning chains.

[Recorded results](repository_recheck_validation.json),
[EET tests](IWD_validation.json), [projectile tests](projectile_validation.json),
[integrity](integrity_validation.json), [Windows installer](windows_installer_validation.json),
[classification](iwd_selection_recheck.csv), [candidates](iwd_pending_candidates.csv),
[unbound phases](iwd_unbound_included_art.csv).
