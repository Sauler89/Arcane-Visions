# Historical SR integration review — 2026-10-08

The beta.2 review validated the original 14 animation BAMs, 12 VVCs and
16 patched SPLs. Beta.12 removes Shadow Door, leaving 13 BAMs, 11 VVCs and
15 selected SR SPLs. See [RIGOROUS_AUDIT.md](RIGOROUS_AUDIT.md) for the
combined graphics package and [ENGLISH_AND_DOORS.md](ENGLISH_AND_DOORS.md)
for the current exclusions.

The historical fixes preserve nonvisual effect bytes, icons, levels,
projectiles, casting globals and summon resources. Non-looping point cues
use the caster as a valid recipient while rendering at the selected point;
they are allowed to finish naturally. VVC phase indexes are one-based;
False Dawn's third-cycle reference is valid and its two phases are retained.
Mantle follows opcode 120 weapon protection duration/conditions, with old-aura
and explicit 24-second fallbacks when direct timed protection is absent.
Malformed, shared/overlapping or unordered effect layouts are skipped.
Private-name collisions abort before writes. Native replacements are shared
with other spells/items using those resources.

Real WeiDU install/reinstall/uninstall tests passed in isolated fixtures.
They establish file/installer preservation, not in-game rendering or universal
compatibility with every mod combination. Source controller rendering flags
are retained except documented renaming/audio cleanup. No new spell, icon,
avatar, creature or gameplay resource is imported. Third-party asset terms
remain in the [README](../../README.md#credits-and-asset-terms).
