# Transient attached visuals — beta.13

A player reported Ghost Armor repeatedly appearing on Silke after she followed
the party into the tavern, including while unconscious. The supplied screenshot
is consistent with the GHARMOR artwork; no saved game or live game session was
available to reproduce that exact area-transition sequence.

## Confirmed configuration issue

Beta.12 added Ghost Armor as opcode 215, parameter 2 = 1 (attached), timing 1
(permanent), duration zero. Its non-looping VVC had duration 0xffffffff.
The BAM looping flag was already clear: the defect is not a set looping bit.
The transient visual had been given an unbounded attached effect/controller
lifetime. It could outlive the initial animation and remain associated with
the creature across area or saved-state reconstruction. This is a plausible
explanation of the report, not an in-game reproduction of Silke's behavior.

The same installer branch produced this configuration for ILLUSH and Spirit
Armor. All six affected spell bindings are corrected together.

| Spell | SPL | Controller | Attached effect lifetime | VVC lifetime cap |
|---|---|---|---|---|
| Invisibility | SPWI206 | srailus | timing 0, 2 seconds | 30 frames |
| Mirror Image | SPWI212 | srailus | timing 0, 2 seconds | 30 frames |
| Invisibility 10 ft. | SPWI307 | srailus | timing 0, 2 seconds | 30 frames |
| Pixie Dust | SPPR516 | srailus | timing 0, 2 seconds | 30 frames |
| Ghost Armor | SPWI317 | sraghst | timing 0, 3 seconds | 45 frames |
| Spirit Armor | SPWI414 | srasprt | timing 0, 4 seconds | 60 frames |

These reuse the original installer budgets. The complete visible cycles fit:
ILLUSH 12 frames/15 fps, GHARMOR 23/15, SPARMOR 15/8. Each controller remains
non-looping and retains its original artwork, frame rate, offsets, rendering
flags and phase mapping. Only its lifetime field changes. All BAM bytes are
unchanged.

The spell patch changes only visual timing/duration relative to beta.12.
Armor Class, saves, invisibility/illusion state, buff duration, icons, casting
features, projectile and nonvisual effects are preserved. Mantle's persistent
aura and False Dawn's two-phase timing remain unchanged. Independent point
summoning cues and the unattached Implosion cue retain instant timing so they
can finish naturally. Component 10 and its IWDEE visuals are unchanged.

## Verification

The test installs tracked beta.12 into an isolated owner-supplied EET export
fixture and confirms the old permanent attached effect and unbounded VVC.
It then upgrades to beta.13, validates the six finite effects and three finite
controllers, and compares old/new spell bytes: only the visual timing and
duration fields differ. It also checks full-cycle playback budgets, original
nonvisual effects, persistent/point effects, stable reinstall and exact
uninstall. Separate installer suites exercise BGEE, BG2EE and EET profiles.

[Regression results](transient_visuals_validation.json). These are file and
WeiDU checks; they do not launch BGEE/EET, simulate an area transition or
demonstrate the exact Silke encounter is fixed in the proprietary engine.

## Updating and existing saves

Update the distribution without deleting its backup directory and reinstall
component 0. This corrects future casts. Effects already serialized on a
creature in an existing save are not rewritten by changing the SPL. For a
clean test, load a save before the affected spell was cast and repeat the
encounter. If a stuck visual persists in a later save, that saved creature's
effects need inspection; do not remove the entire armor spell or all opcode
215 effects, which could erase unrelated buffs/visuals.

Technical references: [IESDP opcode 215](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op215)
and [VVC flags/duration](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm).
GemRB's [PlayVisualEffect implementation](https://github.com/gemrb/gemrb/blob/master/gemrb/plugins/FXOpcodes/FXOpcodes.cpp)
and [ScriptedAnimation](https://github.com/gemrb/gemrb/blob/master/gemrb/core/ScriptedAnimation.cpp)
provide additional implementation context; GemRB is a separate engine and is
not runtime proof for Beamdog's Enhanced Editions.
