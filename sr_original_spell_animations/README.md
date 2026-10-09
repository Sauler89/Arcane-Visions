# Arcane Visions — Spell Effect Animations

**Standalone post-cast spell animations for EET and Baldur's Gate II: Enhanced Edition.**

Arcane Visions gives selected original BG spells the visual effects used by
Spell Revisions or Icewind Dale: Enhanced Edition. It replaces the artwork
shown after a spell is cast, while retaining the installed spell's mechanics.
**Spell Revisions and IWDification are not required.**

Current version: **v0.2.0-beta.6**, by **Sauler89**.
[Italian instructions](../README.it.md) · [Affected spells](#affected-spells) ·
[Audit and validation](docs/RIGOROUS_AUDIT.md)

## Animation examples

These GIFs are decoded from BAMs actually shipped with this mod. They are
illustrative previews, not screenshots captured in the game. Blend rendering
is approximated on a dark background; the engine controls placement, palette,
orientation and timing. Entangle shows an individual animated tendril.

| Shared protection aura — `SPMAGGLO` | Entangle — `SPENTAAI` | Ghost Armor — `GHARMOR` |
|:---:|:---:|:---:|
| ![SPMAGGLO animation](../docs/previews/spmagglo.gif) | ![Entangle animation](../docs/previews/entangle.gif) | ![Ghost Armor animation](../docs/previews/ghost-armor.gif) |

| Chromatic Orb — `SPCHRORB` | Mantle — `DVMANTLE` | Blade Barrier — `BBARRH1` |
|:---:|:---:|:---:|
| ![Chromatic Orb animation](../docs/previews/chromatic-orb.gif) | ![Mantle animation](../docs/previews/mantle.gif) | ![Blade Barrier animation](../docs/previews/blade-barrier.gif) |

| Sanctuary — `SANCTRY` | Protection from Arrows — `PFNMISC` |
|:---:|:---:|
| ![Sanctuary animation](../docs/previews/sanctuary.gif) | ![Protection from Arrows animation](../docs/previews/protection-from-arrows.gif) |

| Minor Globe of Invulnerability — `MGOINVC` | Globe of Invulnerability — `GOINVUC` |
|:---:|:---:|
| ![Minor Globe animation](../docs/previews/minor-globe.gif) | ![Globe of Invulnerability animation](../docs/previews/globe-of-invulnerability.gif) |

| Glitterdust — `GLDUSTA`, VVC phase 2 |
|:---:|
| ![Glitterdust animation](../docs/previews/glitterdust.gif) |

| Otiluke's Resilient Sphere — `ORSPHEC` | Resurrection — `RESURRH` |
|:---:|:---:|
| ![Resilient Sphere animation](../docs/previews/resilient-sphere.gif) | ![Resurrection animation](../docs/previews/resurrection.gif) |

The two globe previews are **IWDEE effect animations**, added in beta.3.
The similarly named SR files `spwi406a/b/c` and `spwi602a/b/c` remain excluded
because they are icons. `SPMAGGLO` is a separate shared protection overlay.

## Components

| Component | Content | Assets |
|---|---|---|
| **0** | SR effect animations for selected original spells | 14 BAMs, 12 VVCs |
| **10** | Distinct IWDEE effects for 29 other original spells | 25 BAMs, 25 VVCs |

Components can be installed independently or together. Their targeted spell
lists are disjoint. The complete package contains **39 animation BAMs and
37 visual-controller VVCs**, and patches **45 SPL files (including two child spells)** in the
supplied EET baseline. Additional spells use the replaced native graphics.

No spellbook/action-bar/portrait icons, new spells, revised spell descriptions,
IWDEE or SR gameplay, source SPL/EFF/PRO files, creature avatars or weapons
are imported. Existing casting-feature effects, sounds, damage, saves,
protections, summon mechanics, spell levels and projectile indexes are retained.

## Installation

1. Extract the entire package into the EET/BG2EE game folder containing `chitin.key`.
2. Run `setup-sr_original_spell_animations.exe` and select English or Italiano.
3. Install component **0**, **10**, or both. No source-game exports are needed.

Install after **EET_end** and after other mods that change these spells.
Windows WeiDU 251 is bundled. On Linux/macOS, use a native WeiDU executable:

```sh
weidu sr_original_spell_animations/setup-sr_original_spell_animations.tp2
```

Uninstall or reinstall through the same installer. The existing installer,
folder names and component numbers are retained for compatibility with the
previous beta. EET/BG2EE are supported; BGEE alone, IWDEE and classic BG2 are
rejected before any assets are copied.

## Affected spells

### Component 0 — Spell Revisions artwork

| Original spell / effect | SPL | SR animation BAM |
|---|---|---|
| Entangle | `SPPR105` | `spentaai, spentaci` |
| Chromatic Orb | `SPWI118` | `spchrorb` |
| Invisibility | `SPWI206` | `illush` |
| Mirror Image | `SPWI212` | `illush` |
| Invisibility 10′ Radius | `SPWI307` | `illush` |
| Pixie Dust | `SPPR516` | `illush` |
| Ghost Armor | `SPWI317` | `gharmor` |
| Spirit Armor | `SPWI414` | `sparmor` |
| Shadow Door | `SPWI505` | `dvsdoor` |
| Implosion | `SPPR728` | `dvimplo` |
| False Dawn | `SPPR609` | `dvsun` |
| Conjure Lesser Fire Elemental | `SPWI516` | `dvelfire` |
| Conjure Lesser Air Elemental | `SPWI520` | `dvelair` |
| Conjure Lesser Earth Elemental | `SPWI521` | `dveleart` |
| Conjure Fire Elemental | `SPWI620` | `dvelfire` |
| Conjure Air Elemental | `SPWI621` | `dvelair` |
| Conjure Earth Elemental | `SPWI622` | `dveleart` |
| Mantle (SR: Prismatic Mantle) | `SPWI708` | `dvmantle` |
| Shared deflection / immunity / shield overlay | `SPWI318, SPWI618, SPWI519, SPWI510 and its school subspells; SPPR701` | `spmagglo` |


For elemental spells, only the arrival animation at the chosen point changes.
Counts, creatures, summon EFFs and spawn timing are retained. Mantle uses SR's
Prismatic Mantle artwork without its new gameplay. False Dawn uses two visual
phases without importing SR's damage, blindness, confusion or subspells.

**Shared-resource scope:** `SPMAGGLO` is a native engine overlay. Replacing it
also changes spells/items from other mods that use that same resource, when
their current effects enable the overlay. This is not limited to the listed
five protection spells. Entangle and Chromatic Orb also retain their native
resource names; other consumers of those BAMs receive the replacement art.

### Component 10 — IWDEE artwork

| Original BG spell | SPL | IWDEE animation BAM |
|---|---|---|
| Remove Paralysis | `SPPR308` | `RPARALH` |
| Poison | `SPPR411` | `POISONH` |
| Lesser Restoration | `SPPR417` | `LRESTORH` |
| Cure Critical Wounds | `SPPR502` | `CCWOUNH` |
| Blade Barrier | `SPPR603` | `BBARRH1`, `BBARRH2` |
| Finger of Death | `SPPR708` | `FODEATH` |
| Regeneration | `SPPR711` | `REGENERH` |
| Greater Restoration | `SPPR713` | `GRESTORH` |
| Storm of Vengeance | `SPPR722` | `FODEATH` |
| Death Spell | `SPWI605` | `DSPELLH` |
| Power Word Silence | `SPWI612` | `PWSILEH` |
| Sphere of Chaos | `SPWI711` | `CONFUSH` |
| Finger of Death | `SPWI713` | `FODEATH` |
| Power Word Stun | `SPWI715` | `PWSTUNH` |
| Abi-Dalzim's Horrid Wilting | `SPWI812` | `ADHWILH` |
| Dragon's Breath | `SPWI922` | `SPDRGNBR` |
| Sanctuary | `SPPR109` | `SANCTRY` |
| Protection from Normal Missiles / Arrows | `SPWI311` | `PFNMISC` |
| Minor Globe of Invulnerability | `SPWI406` | `MGOINVC` |
| Globe of Invulnerability | `SPWI602` | `GOINVUC` |
| Glitterdust | `SPWI224` | `GLDUSTA` |
| Otiluke's Resilient Sphere | `SPWI413` → `SPWI413A` | `ORSPHEC` |
| Resurrection | `SPPR712` → `SPPR712A` | `RESURRH` |
| Heal | `SPPR607` | `HEALH` |
| Slow Poison | `SPPR212` | `SPOISOH` |
| Miscast Magic | `SPPR310` | `MMAGICH` |
| Confusion (cleric) | `SPPR709` | `CONFUSH` |
| Confusion (wizard) | `SPWI401` | `CONFUSH` |
| Chaos | `SPWI508` | `CONFUSH` |


Storm of Vengeance replaces its existing direct visual cue only; its weather,
area and projectiles remain installed as before. Sphere of Chaos replaces its
direct hit cue. The separate Confusion/Chaos spells now use the same IWDEE
artwork for their recognized status visuals; their mechanical confusion state
and visual effect timing/duration are retained. Blade
Barrier preserves the existing duration of both visual layers. Dito/Finger of
Death variants and Storm of Vengeance share one isolated `FODEATH` copy.

The four state overlays retain their existing state opcodes, duration,
conditions and protections. Only the recognized graphic reference/mode changes.
Both globes use private resources, so minor and major can show different art
without replacing `MINORGLB` globally. Sanctuary's state is retained; it is
never replaced with a graphics-only effect.

## Compatibility and graphics handling

The installer edits the resources currently present in the game. Missing
spells or unsupported/truncated/shared effect layouts are skipped. Component
10 additionally requires the recognized original visual reference, target,
attachment and effect count in each ability; unfamiliar visuals from another
mod are skipped and logged. Component 0 deliberately replaces all 141/215
ability visuals of its selected spells, while retaining their nonvisual effects.

Private resource names are checked before installation. A collision aborts
that component before it can overwrite another mod's similarly named resource.
Native replacements intentionally overwrite the engine graphic resources.

Non-looping cues play their full sequence. Mantle follows the duration and
conditions of the existing weapon protection; False Dawn retains its two-phase
schedule. Elemental arrival cues are independent point effects, not changes to
opcode 67's resource fields. The IWD component preserves effect order/counts,
all nonvisual bytes and the probability/save/resistance/target conditions of
the replaced visual effects.

The complete source review compares **246 IWDEE BAMs, 386 exported EET BAMs,
and all 224 BAMs in the SR archive**. Only exact graphics and all-visible-cycle
art matches are duplicate evidence; partial matches and shared/recolored shapes
are diagnostics. Heal and Slow Poison are retained despite shared EET shapes.
All 25 imported IWD BAMs have no full-art match to the selected original-spell
SR artwork. The comparison concerns the supplied exports, not every modlist.

**This is a selected import, not all IWDEE BAMs.** Beta.4 adds Glitterdust,
Otiluke's Resilient Sphere, Resurrection, Heal and Slow
Poison. Beta.5 also adds Miscast Magic and binds the already included
CONFUSH artwork to both Confusion spells and Chaos. Chaos retains both
visual effect instances and their separate conditions; the existing effect
timing/duration remains unchanged for these three CONFUSH bindings. The source
controller is non-looping. Child spells are patched only
when the original root still calls them. The root bytes are unchanged.
The full archive review found no additional demonstrated active original-spell
SR artwork to add. **43 distinct IWD candidates remain unintegrated**, including
projectile/area/conditional phases; they are not labeled SR duplicates.
Included BAMs are also checked for uncovered spell bindings: the extra delayed
HEALH phase in IWD Regeneration has no matching direct cue in this EET baseline
and remains unbound. The initial REGENERH cue is included.
The review also found two unbound GLDUSTA area phases (spread/ring) in IWD
Glitterdust: its target cue is included, while the installed EET shared
projectile has different bindings. These are additional phases of already
included artwork, not two new BAMs.

**Web is excluded at the owner's request in beta.6**, including area and target
artwork. No Web SPL or PRO is patched and no private Web asset is shipped.
WEBA/WEBC/WEBX are classified as user exclusions in the source inventory,
separately from the 43 pending candidates.
Call Lightning still needs IWDEE/EET SKYBOLT BAMs. Slay Living and Sol's Searing
Orb need the installed EET temporary weapons before their hit art can be bound.
See [the full source review](docs/FULL_SOURCE_AUDIT.it.md),
[all IWD decisions](docs/iwd_selection_recheck.csv),
[all SR decisions](docs/sr_source_selection.csv)
and [every pending candidate](docs/iwd_pending_candidates.csv).

## Validation and beta status

WeiDU installation, reinstallation and byte-exact uninstallation passed in
isolated fixtures, including the **45 real exported EET SPL files**. Assets were
checked for hashes, frame bounds/RLE data, cycle references, VVC dependencies,
phase indexes, private names and absence of external palettes/alpha BAMs/audio.

An additional **28 regression cases** cover malformed layouts, an unused global
index, conditional visual effects, wrong targets/delays, resource collisions
and unsupported games. Source SR spell layouts and both EET/BG2EE synthetic
profiles also passed. **44 further overlay cases** verify state and conditional
duration preservation, recognized/custom layouts, safe skips and collisions.
**12 child-spell cases** verify recognized, missing, detached, malformed and
repurposed roots, unknown child visuals, reinstall and exact uninstall.
Full details and retained results are in
[the rigorous audit](docs/RIGOROUS_AUDIT.md).

**The mod has not yet been visually tested in a launched EET game.** Position,
blending and synchronization of the effects require in-game confirmation.
The GIFs do not replace that test. Install/uninstall tests use minimal KEY/TLK
fixtures and exported resources; they do not load a complete game installation.

## Development

```sh
python3 tests/verify_assets.py [path/to/extracted/spell_rev]
python3 tests/verify_graphics_integrity.py [path/to/IWDEE-BAM-export] [path/to/IWDEE-metadata]
python3 tests/verify_installer.py /path/to/weidu [path/to/extracted/spell_rev]
python3 tests/verify_regressions.py /path/to/weidu
python3 tests/verify_iwd_on_export.py /path/to/EET-export /path/to/weidu /path/to/results
python3 tests/verify_overlays.py /path/to/EET-export /path/to/weidu /path/to/results
python3 tests/verify_child_visuals.py /path/to/EET-export /path/to/weidu /path/to/results
```

Tests require Python 3 and WeiDU. Preview generation additionally needs Pillow:
`python3 tools/render_bam_previews.py`. The IWD builder requires owner-supplied
IWDEE metadata/BAM exports; it is unnecessary for installation. Source and
installed hashes are retained in the asset manifests.
The full source audit additionally requires NumPy:
`python3 tools/audit_source_coverage.py IW_METADATA IW_BAMS EET_EXPORT SR_FOLDER OUTPUT`.

## Credits and asset terms

Spell Revisions: **Demivrgvs (Marco Montagnoli)**, with **Mike1072** and
**Ardanis**. Its supplied README credits **Yarpen** and **Scorpio** for BAM work.
Original SR copyright: **2008–2015 Marco Montagnoli**. IWDEE graphics are
credited to **Black Isle Studios/Interplay and Beamdog**; BG graphics to their
respective original creators. This project claims no ownership of those assets.

The supplied SR README says: “This mod may not be sold, published, compiled
or redistributed in any form without the consent of its author.” That source
notice remains applicable; inclusion here does not grant a new graphics license.
WeiDU is distributed under its own license in [WeiDU license](docs/WEIDU-COPYING.txt).
See [CREDITS.md](../CREDITS.md) for provenance and technical references.
