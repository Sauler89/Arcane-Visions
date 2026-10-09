# Changelog

## v0.2.0-beta.3 — IWDEE persistent overlays

- Add Sanctuary (`SANCTRY`), Protection from Arrows (`PFNMISC`), Minor Globe
  (`MGOINVC`) and Globe of Invulnerability (`GOINVUC`) to component 10.
- Fix the earlier omission of engine overlays: redirect their graphic mode and
  resource while retaining existing state opcodes, duration, conditions and
  protections. Do not replace Sanctuary's state with opcode 215.
- Keep minor/major globe artwork isolated; do not replace MINORGLB globally.
- Add four real BAM previews, bringing the README gallery to ten GIFs.
- Verify all 36 EET SPLs and add 44 persistent-overlay regression cases.
- Reclassify all 246 supplied IWDEE BAMs and document distinct candidates that
  are still unintegrated. Do not mislabel technical exclusions as SR overlap.
- Mark Call Lightning pending missing IWDEE/EET SKYBOLT BAMs; do not substitute
  Lightning Bolt/Chain Lightning art or import IWDEE chain/damage mechanics.

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
- Keep the bundled WeiDU license with its documentation, separate from project/graphics licensing.
- Keep Globe of Invulnerability icons excluded from the animation-only mod.

## v0.2.0-beta.1

- Add optional component 10: 15 distinct IWD BAMs and 15 VVCs for 16 original BG spells.
- Exclude duplicates, shared/recolored shapes, SR-covered spells and gameplay imports.

## v0.1.0-beta.2

- Audit SR artwork and isolate custom names.
- Preserve summoning mechanics through independent point visuals.
- Derive Mantle visual duration/conditions from the installed weapon protection.
