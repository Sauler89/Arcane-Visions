# Rigorous audit — Arcane Visions v0.2.0-beta.8

Reviewed on 2026-10-09 (Europe/Rome). Scope: all 78 graphics/controller assets,
both installer components, all 859 source/comparison BAMs, source provenance, live exports, effect conditions,
resource-name collisions, previews, documentation and install/uninstall behavior.

## Findings and corrections

| Finding | Result |
|---|---|
| Implosion's 31-frame BAM at 25 fps needs about 1.24 seconds, but its SPL visual was limited to 1 second | Non-looping SR cues now use timing 1 and finish naturally; only visual timing changes |
| IWD patcher validated a global effect index even with zero global effects | Unused global indexes are accepted; real global effects retain bounds/overlap checks |
| Private BAM/VVC names could overwrite an unrelated mod's same-name resource | Both components check every private name before copying anything and abort on a collision |
| Missing/truncated IWD spells could be skipped without a diagnostic | Explicit missing/truncated messages added |
| Export-test result paths required an already-existing parent | Parent directories are created |
| A regression fixture reused a path after WeiDU changed filename case during restoration | Tests resolve the current resource path and assert no case-colliding filenames |
| Older README claims mixed the SR and IWD skip behavior and asset counts | Rewritten around the actual two components and their separate rules |
| Persistent IWDEE overlays were missed by the 141/215-only selection | Sanctuary, Protection from Arrows and both IWDEE globes added; not SR overlaps |
| README incorrectly generalized the exclusion of SR globe icons to IWDEE globe effects | Corrected; four new genuine BAM previews; SR icons still excluded |

## Full source and omission review

Beta.5 adds MMAGICH for Miscast Magic and three missing CONFUSH bindings:
cleric/wizard Confusion and Chaos. Counting BAMs alone had hidden the latter
omissions because CONFUSH was already included for Sphere of Chaos. Chaos
has two same-resource visual effects per ability; both references change,
while separate conditions and existing timing/duration remain byte-identical.
Six extra real-export regressions cover independent conditions and rejection
of an unknown second, missing, third, delayed or differently targeted cue.
The non-looping source CONFUSH controller is retained.

The audit now generates pending reasons from actual dependency paths and
reports included artwork with unbound roots in
[iwd_unbound_included_art.csv](iwd_unbound_included_art.csv). The additional
delayed HEALH phase of Regeneration has no matching EET cue. Beta.6 also
records GLDUSTA spread/ring fields in IWD GLDUST.PRO: they were hidden by
one-path-per-BAM traversal although its target cue was already included.
Those two area phases remain unbound in EET, whose shared SPARGONP.PRO has
no spread/ring fields and uses a different explosion mode.

Web is explicitly excluded at the owner's request in beta.6. Its target
patch, private BAM/VVC and GIF were removed; area candidates WEBA/WEBX
are excluded too. Export tests confirm SPWI215 remains byte-identical
with either component combination and no private Web resource is installed.
The source inventory retains all three as user exclusions, not omissions.

Beta.7 also excludes Abi-Dalzim's Horrid Wilting at the owner's request.
SPWI812 receives no patch and keeps the installed BG2EE/EET animation.
The private sriowilt BAM/VVC and installer references are removed.
ADHWILH/ADHWILA/ADHWILX are user exclusions, including area phases.
Real-export tests confirm SPWI812 stays byte-identical with either component
combination and no private Horrid Wilting resource is installed.


Beta.4 added Glitterdust, Resilient Sphere, Resurrection,
Heal and Slow Poison. The real source controllers/phases are preserved.
The two child
SPLs are changed only when the original root still calls them after casting.
The root bytes remain identical. The cue patcher now rejects additional
state overlays 153–158. Case-insensitive source lookup prevents Linux filename
omissions. Five BAMs recovered through cue, child and shape selection
remain included; the sixth, Web, was removed in beta.6 at the owner's request.

[Full source review and exclusions](FULL_SOURCE_AUDIT.it.md) inventories every
SR source BAM, all original-spell dependencies and 40 remaining IWD candidates.
No additional demonstrated active original-spell SR artwork was found.

## Persistent overlay and selection review

Beta.3 adds four byte-identical IWDEE BAMs and four isolated looping VVCs.
For opcodes 153/155/156, only parameter 2 (custom artwork mode) and resource
reference are changed. The state opcode, timing, duration and every other
byte of the effect are preserved. A preexisting recognized major-globe
opcode 215 stays opcode 215. No MINORGLB global replacement is used.

[Detailed review and all exclusions](IWD_SELECTION_RECHECK.it.md). The
complete 248-BAM classification distinguishes duplication, SR spell overlap
and distinct unintegrated candidates. New SKYBOLT exports are distinct, but hardcoded routing/timing remains
unverified at runtime. SPCALLLI is identical in both games and has no
traced SPPR302 binding. See [new export review](NEW_EXPORT_REVIEW.it.md).

## Asset checks

- All **40 BAMs** are byte-identical to the supplied source artwork.
- **1,316 total BAM frames** validated.
- All frames, cycle lookups, offsets, dimensions and RLE data validated.
- All **38 VVCs** have valid signatures, resolved BAM dependencies and valid
  one-based phase references (zero/default and -1 omissions handled).
- No controller depends on an external bitmap palette, alpha BAM or audio file.
- Source/installed hashes retained in both manifests. Private resource names
  are at most eight characters and unique case-insensitively.
- All 26 imported IWD BAMs have no full artwork match to the selected original-spell
  SR BAMs. Source comparison covers all 224 SR BAMs, 248 IWD BAMs and 387 EET BAMs.
  Heal and Slow Poison are distinct colour variants despite shared EET shapes.
  Shape alone and a single shared cycle are not complete-duplicate evidence.
- All 13 README GIFs are rendered from bundled assets with retained provenance.
  Frame anchors are retained; blending is illustrative, not an engine renderer.
- The 17 supplied EET BMP headers were checked. None of the EET VVCs replaced
  by component 10 uses an external palette or alpha BAM.

## Installer and preservation tests

| Test | Result |
|---|---|
| SR assets checked against actual v4.21 source bytes | PASS |
| SR EET and BG2EE synthetic profiles: install, reinstall, uninstall | PASS |
| Actual source SR SPL layouts patched and restored | PASS |
| 16 real EET SR SPLs plus 28 real EET IWD SPLs and two ITMs: combined install | PASS |
| IWD component installed independently | PASS |
| Reinstallation snapshot stable, standalone and combined | PASS |
| Disinstallation restores all original resource bytes and removes new graphics | PASS |
| SPL globals, icons, projectile indexes, levels and nonvisual effects retained | PASS |
| IWD visual probability, save, target, power and resistance flags retained | PASS |
| Unknown additional visual from another mod safely skipped by IWD component | PASS |
| 28 extra regressions: invalid layouts, conditional visuals, collision guards and unsupported games | PASS |
| 44 persistent-overlay regressions: state/conditions/duration, custom modes, unknown visuals, collisions and bounds | PASS |
| 12 child-spell cases: recognized/missing/detached/malformed roots and unknown child visuals | PASS |
| Web and Horrid Wilting excluded: both original SPLs byte-identical; no private assets | PASS |
| Six repeated-cue Chaos cases, with separate conditions and all-or-nothing guards | PASS |
| 30 temporary-weapon cases: links, conditions, unknown visuals, bounds, reinstall/uninstall | PASS |
| README local links and GIF/asset hash provenance | PASS |

The 28 regressions include 13 malformed/unsupported SPL layouts, a legal
unused global index, a visual with non-default save/probability/resistance,
wrong target, delayed or unexpectedly persistent cue, collisions in both
components, and unsupported-game checks for both components, plus six additional
state-overlay guard cases (opcodes 153–158).

The SR synthetic tests also exercise Mantle's protection-derived conditions,
its old-aura and explicit 24-second fallbacks, missing native resources,
empty ability blocks and point targeting. A collision is an explicit component
failure before resource copying, not silent partial overwriting.

The exported EET baseline includes IWDification v11, SCS and other spell
packs. Test fixtures use a synthetic minimal KEY/TLK, not the owner's full
installation. WeiDU's derived ADD_SPELL.IDS cache is excluded from snapshot
comparisons because WeiDU clears it independently of these components.

Results: `IWD_validation.json`, `regression_validation.json`,
`integrity_validation.json`, `overlay_validation.json`, `child_validation.json`, `item_validation.json`. Test programs are in the repository's `tests/`.

## Scope and remaining limits

Component 0 patches 16 selected SPLs, deliberately replacing their 141/215
ability visuals. Component 10 patches 28 other SPLs, including two child spells, only where the original
visual configuration is recognized. It also patches two recognized temporary-weapon
hit cues while keeping their roots byte-identical. It preserves effect order/counts and
all nonvisual bytes. Missing or unfamiliar abilities are skipped and logged.
The two root spell lists do not overlap. Persistent Sanctuary/globe state
opcodes retain their behavior, and the original protections stay byte-exact.
This is a selected import; 40 distinct candidate BAMs remain unintegrated.

Native SPENTAAI/SPENTACI, SPCHRORB and SPMAGGLO replacements are shared
resources; any other spell/item using them can receive the new artwork.
SPMAGGLO visibility depends on the installed spell effects and overlay
suppression settings. The installer does not force a suppressed overlay on.

No source SPL/EFF/PRO/ITM/CRE/BCS, new spell, icon, creature or mechanic is
imported. Elemental spawn rules and existing projectiles are unchanged.

**No game was launched.** In-game positions, engine blending, hit/caster
placement and synchronization still require visual confirmation. The GIFs
are illustrations of artwork, not proof of runtime appearance. The comparison
covers exported EET graphics and their supplied aliases, not all 19,841 BAMs
listed in CHITIN.KEY or every resource from every future modlist.

Source SR provenance, credits and its supplied consent notice remain retained.
No third-party graphics ownership or new redistribution license is claimed.

## Beta.8 temporary-weapon hits

SLIVINH and SSORBH now replace recognized impacts in installed SLAYLIVE.ITM
and SORB.ITM, only while their original roots still create those weapons.
No source ITM is imported; roots, weapon headers/projectiles, nonvisual effects
and conditions stay byte-identical. The parser validates ITM signatures,
56-byte headers and disjoint effect blocks. Full export install/reinstall/
uninstall checks include both items; [30 item guard cases](item_validation.json)
pass. SKYBOLT and SSORBT remain unintegrated.
