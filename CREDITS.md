# Credits and provenance

Arcane Visions integration and installer: Sauler89.

Spell Revisions v4.21: Demivrgvs (Marco Montagnoli), Mike1072 and Ardanis.
SR credits Yarpen and Scorpio for BAM contributions. Copyright 2008–2015
Marco Montagnoli. The original source README's consent requirement for
redistribution is retained in the project README. No new license is granted
for third-party graphics.

Icewind Dale: Enhanced Edition artwork: Black Isle Studios, Interplay and
Beamdog. Only selected graphics exported from the owner's installation are
included; the game, its mechanics and complete game data are not distributed.

All animation BAMs are byte-identical to the supplied source assets. Visual
controllers are retargeted, stripped of audio, and (for IWD) normalized to let
the SPL effect control duration. Three direct IWD BAM references receive a
non-looping VVC wrapper. Manifests record source/installed hashes and names.

Technical references:

- [IESDP BAM V1](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/bam_v1.htm)
- [IESDP VVC](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm)
- [IESDP BGEE opcodes](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm)
- [Near Infinity](https://github.com/Argent77/NearInfinity)
- [WeiDU](https://github.com/WeiDUorg/weidu)

WeiDU 251 Windows executable and its license are included. Python tools use
standard libraries; preview rendering uses Pillow. GIFs are generated from
the actual bundled assets and do not depict a launched game.
