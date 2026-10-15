# Credits and provenance

Arcane Visions integration and installer: Sauler89.

Spell Revisions v4.21: Demivrgvs (Marco Montagnoli), Mike1072 and Ardanis.
SR credits Yarpen and Scorpio for BAM contributions. Copyright 2008–2015
Marco Montagnoli. The original SR source notice states:

> This mod may not be sold, published, compiled or redistributed in any form without the consent of its author.

No new license is granted for third-party graphics.

Icewind Dale: Enhanced Edition artwork: Black Isle Studios, Interplay and
Beamdog. Only selected graphics exported from the owner's installation are
included; the game, its mechanics and complete game data are not distributed.

All animation BAMs are byte-identical to the supplied source assets. Visual
controllers are retargeted, stripped of audio, and (for IWD) normalized to let
the installed SPL/ITM effect control duration. Three direct IWD BAM references receive a
non-looping VVC wrapper. Two new single-cycle persistent BAMs receive looping
wrappers based on IWDEE's `#PRONM.VVC`; Protection from Arrows and the major
globe retain their source looping controller layouts. Manifests record
source/installed hashes and names. Beta.13 additionally gives the three SR
transient attached controllers finite duration caps (ILLUSH, GHARMOR, SPARMOR),
without changing their BAMs, rendering flags, phases or frame rates.

Beta.4 additionally retains the original GLDUSTH, #OTILUKE, RESURRH,
HEALH and SPOISOH controller layouts and phases. Those five retained additional BAMs
are also byte-identical to IWDEE. Beta.5 adds the original MMAGICH controller
and artwork. Web artwork/controllers were removed in beta.6 at the owner's
request. Beta.8 adds byte-identical SLIVINH/SSORBH and their source VVC
layouts for temporary-weapon impacts. Beta.9 adds SSORBT and CALLLIH: native destination SKYBOLT uses CALLLIH
bytes, identical to the other supplied IWDEE SKYBOLT, shipped only once.
SPCALLLI remains a comparison-only EET duplicate. No new artwork is generated or claimed.

Technical references:

- [IESDP BAM V1](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/bam_v1.htm)
- [IESDP VVC](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm)
- [IESDP BGEE opcodes](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm)
- [Near Infinity](https://github.com/Argent77/NearInfinity)
- [WeiDU](https://github.com/WeiDUorg/weidu)

WeiDU 251 Windows executable and [its own license](sr_original_spell_animations/docs/WEIDU-COPYING.txt) are included. Python tools use
standard libraries for installation checks; source-image comparison uses NumPy
and preview rendering uses Pillow. GIFs are generated from
the actual bundled assets and do not depict a launched game.

## Classic Spell Trap globe (component 20)

Cowled Menace, copyright © 2026 Maltodaxtrin/Daxtreme:
[source folder](https://github.com/Gibberlings3/CowledMenace/tree/c88daf97d585c68089972f4b30980fff29ca6b8a/cowledmenace/spelltrap).
The project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/);
its full [license and disclaimer](sr_original_spell_animations/docs/COWLED-MENACE-LICENSE.md)
are retained. Original BG2 graphics belong to their original creators.

`dx#trap.bam` becomes `sratrap.bam`, with identical bytes. Its duplicate
`SPMAGGLO.bam` is not imported. `dx#strap.vvc` becomes `sratrap.vvc`;
BAM/internal names change and three audio fields are cleared. All rendering
flags, offsets, FPS and phase mappings are retained. The README GIF is a
rendered preview derived from these assets. Integration code is new; no source
quest, spell or gameplay code is imported. No source-author endorsement is implied.
