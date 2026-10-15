# Affected spells and animation assignments

These tables identify the selected phases changed by each component, not
all effects used by a spell. All installed spell mechanics are retained.

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

### Component 10 — IWDEE artwork

| Original BG spell / phase changed | SPL | IWDEE animation BAM installed |
|---|---|---|
| Remove Paralysis | `SPPR308` | `RPARALH` |
| Poison | `SPPR411` | `POISONH` |
| Lesser Restoration | `SPPR417` | `LRESTORH` |
| Cure Critical Wounds | `SPPR502` | `CCWOUNH` |
| Blade Barrier | `SPPR603` | `BBARRH1`, `BBARRH2` |
| Finger of Death | `SPPR708` | `FODEATH` |
| Regeneration — initial cue | `SPPR711` | `REGENERH` |
| Greater Restoration | `SPPR713` | `GRESTORH` |
| Storm of Vengeance — direct target cue | `SPPR722` | `FODEATH` |
| Death Spell — target cue | `SPWI605` | `DSPELLH` |
| Power Word Silence | `SPWI612` | `PWSILEH` |
| Sphere of Chaos — selected direct cue | `SPWI711` | `CONFUSH` |
| Finger of Death | `SPWI713` | `FODEATH` |
| Power Word Stun | `SPWI715` | `PWSTUNH` |
| Dragon's Breath | `SPWI922` | `SPDRGNBR` |
| Sanctuary | `SPPR109` | `SANCTRY` |
| Protection from Normal Missiles / Arrows | `SPWI311` | `PFNMISC` |
| Minor Globe of Invulnerability | `SPWI406` | `MGOINVC` |
| Globe of Invulnerability | `SPWI602` | `GOINVUC` |
| Glitterdust — target cue | `SPWI224` | `GLDUSTA` |
| Otiluke's Resilient Sphere | `SPWI413` → `SPWI413A` | `ORSPHEC` |
| Resurrection | `SPPR712` → `SPPR712A` | `RESURRH` |
| Heal | `SPPR607` | `HEALH` |
| Slow Poison | `SPPR212` | `SPOISOH` |
| Miscast Magic | `SPPR310` | `MMAGICH` |
| Confusion (cleric) | `SPPR709` | `CONFUSH` |
| Confusion (wizard) | `SPWI401` | `CONFUSH` |
| Chaos | `SPWI508` | `CONFUSH` |
| Slay Living (weapon hit) | `SPPR511` → `SLAYLIVE.ITM` | `SLIVINH` |
| Sol's Searing Orb (weapon hit and travel) | `SPPR614` → `SORB.ITM` | `SSORBH`, `SSORBT` |
| Call Lightning (shared native graphics) | `SPPR302`; `SKYBOLT.BAM` | `CALLLIH` (alias of IWDEE `SKYBOLT`) |

### Component 20 — classic Spell Trap globe

| Original spell | SPL | Private BAM / VVC | Source artwork |
|---|---|---|---|
| Spell Trap — level 9 wizard spell | `SPWI902` | `sratrap` | Cowled Menace `dx#trap.bam` |

## Scope notes

- Component 0's native Entangle, Chromatic Orb and `SPMAGGLO` replacements
  also affect other consumers of those shared graphics. The elemental BAMs
  change arrival cues for both normal and lesser summons, not creature art.
- Component 10's Call Lightning artwork replaces shared native `SKYBOLT`.
  Storm of Vengeance and Finger of Death share `FODEATH` in the supplied
  IWDEE source; only their selected target cue changes.
- Component 20 patches only `SPWI902`, including other callers of that exact
  spell. Separate item implementations are untouched. While active, it hides
  the bearer's other hardcoded protection auras; their mechanics are retained.
  See [Spell Trap details](SPELL_TRAP.md).
- Web, Abi-Dalzim's Horrid Wilting, Dimension Door and Shadow Door retain
  their installed artwork. The Fireball family is not included.

[Source coverage and pending effects](FULL_SOURCE_AUDIT.md) ·
[Back to the README](../../README.md)
