# IWDEE selection and exclusions

## Effects recovered during the reviews

| Original BG spell | IWDEE BAM | Installed binding |
|---|---|---|
| Sanctuary, SPPR109 | SANCTRY | Private sriosanc; opcode 153 retained |
| Protection from Arrows, SPWI311 | PFNMISC | Private srioarrw; opcode 156 retained |
| Minor Globe, SPWI406 | MGOINVC | Private sriomglb; opcode 155 retained |
| Globe, SPWI602 | GOINVUC | Private sriogglb; installed opcode 155 or recognized 215 retained |
| Glitterdust, SPWI224 | GLDUSTA | Target cue; separate area phases remain unbound |
| Resilient Sphere | ORSPHEC | SPWI413A, only while reached from SPWI413 |
| Resurrection | RESURRH | SPPR712A, only while reached from SPPR712 |
| Heal / Slow Poison | HEALH / SPOISOH | Distinct colour variants, not shape-based duplicates |
| Miscast Magic | MMAGICH | Recognized direct cue |
| Confusion (both) / Chaos | CONFUSH | Existing status cues; both separately conditioned Chaos cues retained |
| Slay Living | SLIVINH | Recognized hit in installed SLAYLIVE.ITM |
| Sol's Searing Orb | SSORBH / SSORBT | Installed SORB impact and private travel clone |
| Call Lightning | CALLLIH | Shared native SKYBOLT replacement after guards |

These selected IWDEE BAMs do not duplicate the selected SR original-spell
artwork in the supplied comparison. SR globe files spwi406a/b/c and
spwi602a/b/c are icons and remain excluded; that exclusion does not apply to
IWDEE globe world effects. Minor and major globe use separate private names.

## Conditions and limits

Changing graphic mode/reference never replaces Sanctuary or globe state with
a graphics-only opcode. Duration, targeting and application conditions remain
installed. Unrecognized additional visuals cause a safe skip. Non-looping
controllers are retained; looping Blade Barrier effects follow existing spell
durations. Storm of Vengeance uses FODEATH only for its recognized direct cue;
its SPSTRMVA storm artwork is already byte-identical in both supplied games.

The delayed HEALH phase of Regeneration and GLDUSTA spread/ring in GLDUST.PRO
remain unbound: the installed EET routes differ. The source graph records
references, not proof that every declared projectile field is activated.

## Owner exclusions

- Web: SPWI215; WEBA/WEBC/WEBX, target and area phases, no private Web assets.
- Horrid Wilting: SPWI812; ADHWILH/ADHWILA/ADHWILX, target and area phases.
- Dimensional doors: SPWI402 and SPWI505 retain installed BG resources;
  SR DVSDOOR and SPDIMNDR are excluded. No global native door replacement.

Call Lightning's hardcoded chain binding remains an engine inference that
requires visual game confirmation; SPCALLLI is an EET duplicate and is not
used as its artwork. See [PROJECTILE_IMPORT.md](PROJECTILE_IMPORT.md).

[Complete classifications](iwd_selection_recheck.csv),
[remaining candidates](iwd_pending_candidates.csv),
[unbound selected artwork](iwd_unbound_included_art.csv),
[SR exclusions](sr_user_exclusions.json).
