# Rigorous audit — Arcane Visions v0.2.0-beta.3

Reviewed on 2026-10-09 (Europe/Rome). Scope: all 64 graphics/controller assets,
both installer components, source provenance, live exports, effect conditions,
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

## Persistent overlay and selection review

Beta.3 adds four byte-identical IWDEE BAMs and four isolated looping VVCs.
For opcodes 153/155/156, only parameter 2 (custom artwork mode) and resource
reference are changed. The state opcode, timing, duration and every other
byte of the effect are preserved. A preexisting recognized major-globe
opcode 215 stays opcode 215. No MINORGLB global replacement is used.

[Detailed review and all exclusions](IWD_SELECTION_RECHECK.it.md). The
complete 246-BAM classification distinguishes duplication, SR spell overlap
and distinct unintegrated candidates. Call Lightning still needs its missing
IWDEE/EET SKYBOLT BAMs; no exclusivity claim can be made for absent artwork.

## Asset checks

- All **33 BAMs** are byte-identical to the supplied source artwork.
- **1,011 total BAM frames** validated.
- All frames, cycle lookups, offsets, dimensions and RLE data validated.
- All **31 VVCs** have valid signatures, resolved BAM dependencies and valid
  one-based phase references (zero/default and -1 omissions handled).
- No controller depends on an external bitmap palette, alpha BAM or audio file.
- Source/installed hashes retained in both manifests. Private resource names
  are at most eight characters and unique case-insensitively.
- The final 19 IWD BAMs have no complete, cropped-art, shape or emitted-RGB
  cycle match against the 386 EET BAMs or 14 SR BAMs compared. Shared names
  are not used as evidence of duplication; compression and alias names are ignored.
- All ten README GIFs are rendered from bundled assets with retained provenance.
  Frame anchors are retained; blending is illustrative, not an engine renderer.
- The 17 supplied EET BMP headers were checked. None of the EET VVCs replaced
  by component 10 uses an external palette or alpha BAM.

## Installer and preservation tests

| Test | Result |
|---|---|
| SR assets checked against actual v4.21 source bytes | PASS |
| SR EET and BG2EE synthetic profiles: install, reinstall, uninstall | PASS |
| Actual source SR SPL layouts patched and restored | PASS |
| 16 real EET SR SPLs plus 20 real EET IWD SPLs: combined install | PASS |
| IWD component installed independently | PASS |
| Reinstallation snapshot stable, standalone and combined | PASS |
| Disinstallation restores all original resource bytes and removes new graphics | PASS |
| SPL globals, icons, projectile indexes, levels and nonvisual effects retained | PASS |
| IWD visual probability, save, target, power and resistance flags retained | PASS |
| Unknown additional visual from another mod safely skipped by IWD component | PASS |
| 22 extra regressions: invalid layouts, conditional visuals, collision guards and unsupported games | PASS |
| 44 new persistent-overlay regressions: state/conditions/duration, custom modes, unknown visuals, collisions and bounds | PASS |
| README local links and GIF/asset hash provenance | PASS |

The 22 regressions include 13 malformed/unsupported SPL layouts, a legal
unused global index, a visual with non-default save/probability/resistance,
wrong target, delayed or unexpectedly persistent cue, collisions in both
components, and unsupported-game checks for both components.

The SR synthetic tests also exercise Mantle's protection-derived conditions,
its old-aura and explicit 24-second fallbacks, missing native resources,
empty ability blocks and point targeting. A collision is an explicit component
failure before resource copying, not silent partial overwriting.

The exported EET baseline includes IWDification v11, SCS and other spell
packs. Test fixtures use a synthetic minimal KEY/TLK, not the owner's full
installation. WeiDU's derived ADD_SPELL.IDS cache is excluded from snapshot
comparisons because WeiDU clears it independently of these components.

Results: `IWD_validation.json`, `regression_validation.json`,
`integrity_validation.json`, `overlay_validation.json`. Test programs are in the repository's `tests/`.

## Scope and remaining limits

Component 0 patches 16 selected SPLs, deliberately replacing their 141/215
ability visuals. Component 10 patches 20 other SPLs only where the original
visual configuration is recognized. It preserves effect order/counts and
all nonvisual bytes. Missing or unfamiliar abilities are skipped and logged.
The two root spell lists do not overlap. Persistent Sanctuary/globe state
opcodes retain their behavior, and the original protections stay byte-exact.
This is a selected import; 42 distinct candidate BAMs remain unintegrated.

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
