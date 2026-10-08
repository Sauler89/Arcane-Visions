# Changelog

## v0.2.0-beta.2 — rigorous review

- Let non-looping SR visuals finish their BAM sequence, fixing the 1-second
  Implosion cutoff (31 frames at 25 fps, about 1.24 seconds).
- Check private asset names before changing any game resources; abort on collisions.
- Accept an unused global effect index when the global count is zero in the IWD patcher.
- Report missing and truncated IWD spell resources explicitly.
- Add 22 regression cases and reject duplicate filenames differing only by case in tests.
- Fix nested result-directory creation in the exported-EET test utility.
- Document native/shared-resource scope and component-specific skip behavior accurately.
- Add six reproducible GIF previews and English/Italian README instructions.
- Keep Globe of Invulnerability icons excluded from the animation-only mod.

## v0.2.0-beta.1

- Add optional component 10: 15 distinct IWD BAMs and 15 VVCs for 16 original BG spells.
- Exclude duplicates, shared/recolored shapes, SR-covered spells and gameplay imports.

## v0.1.0-beta.2

- Audit SR artwork and isolate custom names.
- Preserve summoning mechanics through independent point visuals.
- Derive Mantle visual duration/conditions from the installed weapon protection.
