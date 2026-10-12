# Changelog

## v0.2.0-beta.10 — full repository recheck

- Reject SRIOSORB symbol collisions in PROJECTL.IDS and MISSILE.IDS before
  writes, including absent-PRO collisions that previously left SORB pointing
  to a missing projectile. Add three mixed-case IDS collision regressions.
- Verify both component orders, English/Italiano and partial uninstall while
  retaining the other component. All 24 projectile and existing suites pass.
- Recheck every shipped asset and all 861 source BAMs; selection is unchanged.
- Align version/count/date reports and install-order guidance; clarify the
  private SORB clone exception and the pending in-game lightning verification.

## v0.2.0-beta.9 — Sol orb travel and native lightning

- Add SSORBT travel through a private clone of the installed PFIRE3 projectile.
  Preserve speed/audio/gameplay; register the clone and retarget SORB only.
- Add CALLLIH as shared native SKYBOLT artwork after recognized layout guards.
  Preserve all SPL/PRO bytes and chain indexes. The IWDEE SKYBOLT source is
  byte-identical to CALLLIH and is not shipped twice. In-game test remains pending.
- Pass 21 projectile guard cases and full combined install/reinstall/uninstall.
- Include 42 BAMs, 38 VVCs and 15 actual BAM previews; compare all 861 source BAMs.
- Keep Web and Abi-Dalzim excluded.

## v0.2.0-beta.8 — verified temporary-weapon impacts

- Add SLIVINH/SSORBH at the actual Slay Living and Sol Searing Orb weapon hits.
- Preserve root SPLs, weapon gameplay, projectiles and all effect conditions;
  skip detached roots and unknown/malformed hit layouts. No source ITM import.
- Validate 44 exported SPLs and two ITMs, plus 30 weapon guard cases.
- Compare new SKYBOLT exports (23 vs 6 frames); retain as a pending hardcoded
  candidate. SPCALLLI is identical between IWDEE/EET, with no SPPR302 binding.
- Inventory 859 BAMs: 248 IWDEE, 387 EET, 224 SR. Web/Horrid Wilting stay excluded.

## v0.2.0-beta.4 — full source review

- Add six omitted IWD effects: Glitterdust, Web target overlay, Resilient Sphere,
  Resurrection, Heal and Slow Poison. Preserve original gameplay and Web state.
- Resolve source filename case and use the actual GLDUSTH/WEBC/#OTILUKE/RESURRH
  controller phases. Guard both child patches by a live original-root cast link.
- Count state overlays 153–158 when checking for unexpected additional visuals.
- Audit all 246 IWD, 386 EET and 224 source SR BAMs; do not exclude distinct
  colours just because shapes match, or entire BAMs because one cycle matches.
- Verify 42 real EET SPLs, 54 overlay cases, 28 regressions and 12 child cases.
- Retain full input inventories, graph paths, SR decisions and 46 pending IWD
  candidates with explicit reasons. No additional active original-spell SR BAM found.
- Add four actual BAM GIFs, bringing the README gallery to 14.


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
