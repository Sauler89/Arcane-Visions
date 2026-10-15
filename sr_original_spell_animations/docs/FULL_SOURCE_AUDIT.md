# Full source review

The source comparison was performed on 249 IWDEE BAMs (10,307 physical
frames), 388 exported EET BAMs (17,904 frames) and all 224 BAMs in the supplied
Spell Revisions v4.21 archive (3,661 frames). These are owner-supplied exports,
not every resource in the complete EET CHITIN.KEY. The beta.12 selection removes
SR door artwork at the owner's request; the source inventory remains evidence
of the original files, including files no longer selected for distribution.

## Current SR selection

| Classification | BAMs |
|---|---:|
| Included original-spell artwork | 13 |
| Icons | 178 |
| Wings/avatar/equipment | 17 |
| New spells/replacements/items | 8 |
| Inactive or unreferenced | 5 |
| Unused tool artwork | 1 |
| Owner-excluded door artwork | 2 |

DVSDOOR had been assigned only to Shadow Door (SPWI505). Its private BAM/VVC
and entire binding are removed. The archive's SPDIMNDR was not copied by the
active SR installer and had never been shipped here. It is now also recorded
as an explicit owner exclusion. Dimension Door (SPWI402), Shadow Door and
native SPDIMNDR/DDOORH resources retain their installed bytes.

Other inactive SR assets include A#SHOPE/A#SPAIN (copied but no live visual
controller binding found), DVHOLYA1/2 (commented installation) and SPCCOLDL
(the installer edits the game's BAM rather than copying this archive variant).
New spell artwork such as Storm Shield, Vitriolic Sphere, Icelance, Sound
Burst and Mestil's Acid Sheath is not included. Spellbook/action icons,
celestial wings and equipment images are excluded.

## IWDEE selection

The beta.10 comparison classifies 28 physical imports, one byte-identical
included alias (SKYBOLT/CALLLIH), 164 complete EET matches, one all-visible-cycle
art match, five SR spell overlaps, six without a mapped original BG root,
six owner exclusions for Web/Horrid Wilting and 38 distinct pending candidates.
The beta.12 removal of SR Shadow Door does not add or change IWDEE artwork.
DDOORH already matches EET exactly and is not distributed.

Selection reviews recovered persistent state overlays (Sanctuary, Protection
from Arrows and both globes), differently named controllers (Glitterdust),
child spells (Resilient Sphere/Resurrection), distinct colour variants
(Heal/Slow Poison/Miscast Magic) and bindings hidden by reuse of an already
selected BAM (Confusion/Chaos). Chaos changes both separately conditioned
visual cues together; additional unknown cues cause a safe skip.

Source spell graphs follow ability/casting effects, external EFFs, VVC/VEF,
PRO and temporary-weapon links. Only actual post-cast uses of mapped original
BG player spells/HLAs establish selection. Shape similarity is diagnostic;
a single matching cycle is not proof of a complete duplicate. A declared PRO
field or uncertain nested projectile index is not proof of runtime activation.
The graph covers 319 mapped original roots, not every NPC/innate spell.

## Known unintegrated phases

38 distinct IWDEE candidate BAMs remain unintegrated. Fireball's FIREBAT,
FIREBAX, FIREBAA and FIREBAR are among them; work on that optional integration
is suspended and absent from this distribution. The delayed HEALH phase in
Regeneration and two GLDUSTA area phases remain unbound even though those
BAMs are included for other selected cues. Web and Horrid Wilting remain
owner exclusions across target and area phases.

Sol's Searing Orb imports SSORBH in the installed SORB weapon and SSORBT
through a clone of installed PFIRE3. Call Lightning uses CALLLIH as shared
native SKYBOLT artwork; the supplied IWDEE SKYBOLT is byte-identical, so it is
not copied twice. SPCALLLI is an EET duplicate without a proven SPPR302 link.
See [PROJECTILE_IMPORT.md](PROJECTILE_IMPORT.md).

## Verification and reproducibility

The original archives remain unchanged. Source/installed hashes are retained
in asset manifests; BAMs are copied byte-for-byte, VVC changes are documented.
Tests check effect layout, targeting, saves, probability, resistance, timing,
private collisions, component order, reinstall and exact uninstall. They use
WeiDU and exported files with synthetic KEY/TLK, not the game renderer.
No source SPL/EFF/PRO/ITM/CRE/BCS or gameplay content is imported.

Machine-readable evidence:
[source inventory](source_BAM_inventory.csv),
[SR classification](sr_source_selection.csv),
[IWDEE classification](iwd_selection_recheck.csv),
[all dependency paths](source_dependency_paths.csv),
[pending candidates](iwd_pending_candidates.csv),
[unbound phases](iwd_unbound_included_art.csv),
[source archives](source_archive_inventory.json),
[source summary](source_coverage_summary.json),
[current audit](RIGOROUS_AUDIT.md).
