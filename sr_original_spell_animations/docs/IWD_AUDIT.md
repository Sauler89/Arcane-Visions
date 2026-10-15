# IWDEE component audit

The current component includes 28 source-identical BAMs and 26 private VVCs
for recognized post-cast effects. It patches 28 SPL resources (including two
children), two temporary-weapon impacts, a private Sol's Searing Orb travel
projectile and shared native Call Lightning artwork. The current spell table
is in the [README](../../README.md#component-10--iwdee-artwork).

## Selection and graphics preservation

The complete comparison inventory contains 249 IWDEE, 388 exported EET and
224 SR BAMs. Byte/raw/render identity and complete visible-cycle artwork
are separate from diagnostic shape similarity. A matching outline or one
shared cycle does not establish a redundant animation. Heal and Slow Poison
retain their distinct colours despite sharing shapes with EET artwork.

Only existing recognized ability effects are redirected. Casting features,
icons, nonvisual effects, saves, probabilities, resistance, target conditions
and mechanical state opcodes remain installed. Persistent Sanctuary, missile
protection and globes keep their existing opcodes and durations. Child spells
are edited only while still reached from their original roots. Temporary
weapon hits are edited in the installed ITMs, never by importing source items.
Private names and SRIOSORB registry symbols are checked before any writes.

Web and Horrid Wilting are explicitly excluded, including their area phases.
Dimension Door and Shadow Door also retain their installed BG artwork in
beta.12. Not every IWDEE animation has been imported: see
[FULL_SOURCE_AUDIT.md](FULL_SOURCE_AUDIT.md) and
[iwd_pending_candidates.csv](iwd_pending_candidates.csv).

## Verification

All BAM frames, palette/lookup bounds and RLE data are validated. VVC names,
phase indexes and BAM dependencies resolve; no controller requires an external
palette, alpha BAM or audio. Tests run actual WeiDU on isolated copies of
exports with minimal KEY/TLK fixtures, not a launched game. Stable reinstall,
exact uninstall, unknown-layout skips, component order and condition
preservation are checked. Final engine blending, position and synchronization
remain subject to visual testing in the game.

[Current audit](RIGOROUS_AUDIT.md), [IWD results](IWD_validation.json),
[asset integrity](integrity_validation.json), [source provenance](source_archive_inventory.json).
