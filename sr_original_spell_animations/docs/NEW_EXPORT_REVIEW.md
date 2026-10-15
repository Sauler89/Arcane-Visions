# Additional EET/IWDEE exports — historical beta.8 review

This section records the beta.8 investigation. SSORBT travel and shared
CALLLIH/SKYBOLT were subsequently included in beta.9; see
[PROJECTILE_IMPORT.md](PROJECTILE_IMPORT.md) for current behavior.

| Resource | Finding | Current action |
|---|---|---|
| SPCALLLI.BAM | Identical in IWDEE/EET, 18 frames, one cycle | Excluded as redundant; no proven SPPR302 binding |
| SKYBOLT.BAM | IWDEE 23 frames, EET 6; different artwork/anchors | Included via byte-identical IWDEE CALLLIH alias, one copy |
| SLAYLIVE.ITM | EET impact opcode 141/39, target 2 | Replace recognized cue with private SLIVINH |
| SORB.ITM | EET impact opcode 215, ICFIRSDI, p2=0, target 2 | Replace recognized cue with private SSORBH |

SPCALLLI is referenced by AMCALL/CALLLIGH controllers in both games and by
other EET resources, including BDZAP and SPIN656/SPIN721. These references do
not establish that it is the graphic for the original Call Lightning spell.
The SPPR302 exports use hardcoded chain missiles (EET 81-85, IWDEE 85-91),
not a direct literal SKYBOLT reference. Engine documentation supports that
association; file-only tests do not prove the runtime chain's rendering.

IWDEE applies SLIVINH and SSORBH directly to the target. The supplied EET
spells instead create temporary SLAYLIVE/SORB weapons through opcode 111.
The mod reads their roots without writing them, validates the existing link
(target caster, p1=1, p2=0, positive duration, timing 0), then patches the
recognized hit in the installed item. It never imports an IWDEE weapon or
adds the hit cue to the caster. ITM V1 signatures, 56-byte ability headers,
disjoint effect blocks and visual conditions are checked. Missing/detached
weapons, additional visuals, delays and unfamiliar layouts are skipped.

The beta.8 tests covered 44 EET SPLs and two ITMs; beta.12 removes Shadow
Door, leaving 43 selected SPLs. Stable reinstall, byte-exact uninstall and
30 item guard cases were recorded. SORB's later private projectile reference
is the explicit exception to retaining its entire original header. Root SPLs,
nonvisual effects, saves, probabilities, icons and all other item bytes stay
installed. Web and Horrid Wilting remain excluded.

[Export evidence](new_export_validation.json), [item tests](item_validation.json),
[current full EET tests](IWD_validation.json), [item mappings](iwd_item_mapping.json),
[archive provenance](source_archive_inventory.json).
