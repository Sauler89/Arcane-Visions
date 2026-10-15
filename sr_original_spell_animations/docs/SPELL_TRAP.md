# Classic BG2 Spell Trap globe — beta.14

Component 20 adds the globe from Cowled Menace's `spelltrap` directory only
to `SPWI902.SPL`, the level 9 wizard spell. It is independent of components
0 and 10 and requires no Cowled Menace installation.

## Source and assets

Pinned source: [Gibberlings3/CowledMenace, c88daf9](https://github.com/Gibberlings3/CowledMenace/tree/c88daf97d585c68089972f4b30980fff29ca6b8a/cowledmenace/spelltrap).
The source directory contains two byte-identical BAMs (`dx#trap.bam` and
`SPMAGGLO.bam`) and one VVC. The current source installer does not reference
that directory; this integration implements its own spell-scoped binding.

- `dx#trap.bam` → `sratrap.bam`: exact bytes, 33 frames and one cycle.
- `dx#strap.vvc` → `sratrap.vvc`: private BAM/internal name; audio references
  cleared. Preserve source flags (0x9, including looping), blending, placement,
  orientation, 15 FPS, default phase mapping and effect-controlled duration.
- Never copy the source `SPMAGGLO.bam` over a native engine resource.
- Reject either private-name collision before any spell or asset write.

[Manifest](spelltrap_asset_manifest.json) records source commit and both hashes.
[License](COWLED-MENACE-LICENSE.md): CC BY-NC 4.0, copyright © 2026
Maltodaxtrin/Daxtreme. Original game artwork remains its creators' property.

## Binding and lifetime

The installed spell must remain wizard type, level 9, with valid, separate
ordered effect blocks. Each ability must contain exactly one direct opcode
259 for every power level 1–9, with a common positive timed duration and
application conditions, self target, and no probability or saving-throw gate.
Unsupported indirect/custom visual routes and conditional trap sets are skipped.
Each trap's resource must be empty or `SPWI902B`; this field is an exhaustion
spell callback, **not a BAM or VVC reference**.

The installed `SPWI902B` must already contain unconditional, immediate opcode
321 removal of `SPWI902` in every ability. It is checked, never patched. If the
root or cleanup route is absent/unrecognized, the component installs no assets.

Two visual effects are appended to each recognized root ability:

| Opcode | Function | Lifetime and conditions |
|---|---|---|
| 291, parameter 2 = 1 | Suppress native protection auras on the bearer | Copied from installed opcode 259 |
| 215, parameter 2 = 1, `sratrap` | Attached classic globe | Copied from installed opcode 259 |

Original global/casting effects, all original ability effects and their order,
spell level, icons, projectiles, sounds, absorption capacity, power levels,
spell recall and removal callbacks remain byte-identical. The supplied EET
root uses 108 seconds; another recognized uniform duration is copied rather
than replaced with a fixed value. Both additions belong to parent `SPWI902`,
so its existing exhaustion cleanup removes them along with the protection.
Ordinary expiry and source-based removal follow the same parent/duration.
No save, CRE, item or callback resource is rewritten.

## Scope and engine limitation

Only casting `SPWI902` gives this globe. Separate item implementations and
other spell resources are unchanged. An item or mod that explicitly casts
`SPWI902` receives the same spell visual: the engine does not distinguish
spellbook casting from another caller of that identical spell resource.

The engine's opcode 259 selects hardcoded `SPMAGGLO`. It offers no field for
an isolated custom animation. Opcode 291 suppresses **both** hardcoded
`SPMAGGLO` and `SPTURNI2` on the bearer while active; concurrently active
protection spells can therefore lose their hardcoded auras temporarily.
Their mechanical effects remain unchanged. Explicit opcode 215 visuals,
including the private globe, are not suppressed. Other creatures and the
shared BAM/VVC files are unaffected by component 20.

Component 0 still intentionally replaces native SPMAGGLO for its own shared
protection artwork. Component 20 neither reverses nor overwrites that change.

## Validation

The [retained results](spelltrap_validation.json) cover real exported EET
Spell Trap/callback resources inside isolated KEY/TLK fixtures, three game
profiles and rejection of IWDEE, combined and reverse component orders, multiple ability headers,
nondefault duration, missing/repurposed resources, conditional traps/cleanup,
invalid layouts, duplicate power levels, private-name collisions, partial uninstall, stable
reinstall and byte-exact uninstall. Component 20 alone changes only
`SPWI902.SPL` and adds its two private visual assets. Every original effect,
all other spells/items and native graphics are compared byte-for-byte.

These are installer/data tests, not a running BGEE/BG2EE/EET game. The README
GIF is decoded from the shipped BAM with approximate blending. In-game
placement, expiry, depletion, dispelling/removal, recasting, concurrent auras
and save/area transitions still require confirmation in the actual engine.

Technical references: [IESDP opcodes 259, 291, 215 and 321](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm),
[VVC format](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm).
