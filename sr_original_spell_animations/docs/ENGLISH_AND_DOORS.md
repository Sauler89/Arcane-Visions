# English-only installer and original door effects — beta.12

The installer now offers English only. The other translation and its installer
entry are removed. The separate translated README is removed and the technical
review documents are provided in English, with their internal links updated.
This does not change the language of the game or its spell descriptions.

## Door effects

The SR DVSDOOR BAM/VVC had been bound only to Shadow Door (SPWI505).
That complete spell patch is removed, together with private srasdor.bam and
srasdor.vvc, their mapping/manifest rows and private-name guards. The source
archive's SPDIMNDR was never distributed by this mod; it is recorded with
DVSDOOR as an explicit exclusion in [sr_user_exclusions.json](sr_user_exclusions.json).
Dimension Door (SPWI402), Shadow Door, Blindness (SPWI109), native SPDIMNDR.BAM
and DDOORH.BAM/VVC remain installed as before. No native door is overwritten
globally, so other spells sharing those animations also retain their artwork.

The different ILLUSH illusion effect and the three elemental summoning effects
remain selected; they are separate assets, not the removed DVSDOOR effect.
Web and Horrid Wilting remain excluded. Fireball work is still suspended.

The package now contains 41 BAMs and 37 VVCs, with 1,409 physical BAM frames.
Component 0 contains 13 BAMs/11 VVCs and patches 15 selected SPLs. Component
10 is unchanged: 28 BAMs/26 VVCs, 28 selected SPLs, two temporary-weapon hits,
the isolated SORB travel clone and shared SKYBOLT artwork. The full export
fixture therefore covers 43 selected SPLs and two ITMs.

## Upgrading an installed older version

Replace the mod distribution while retaining its backup directory, then
reinstall the installed components through WeiDU using English. This makes
WeiDU restore Shadow Door from its old backup and removes the old private
door resources before applying the reduced selection. Copying new BAMs into
override manually does not perform that restoration.

An automated upgrade case installs tracked beta.11 using its former language,
updates the distribution to beta.12, then reinstalls in English. It checks
the restored door SPL/BAM/VVC bytes, absent obsolete assets, English entries
in WeiDU.log, stable reinstall and exact uninstall. The baseline is an
isolated copy of owner-supplied EET exports with minimal KEY/TLK.

## Validation

- Single-component and combined installs preserve all eight protected source
  resources: both door spells, Blindness, three native door graphics/controllers,
  Web and Horrid Wilting.
- Both component orders, reinstall and partial/full uninstall retain exact
  resource bytes outside the selected visual changes.
- BGEE, BGEE+SoD, BG2EE and EET profiles retain their game guards. The current
  installer tests use English only; historical reports identify older checks.
- Source hashes, BAM frames/cycles/RLE, VVC dependencies and README links are
  checked against the reduced package selection.

[Door and upgrade results](english_doors_validation.json),
[BGEE results](BGEE_validation.json), [full EET results](IWD_validation.json),
[asset integrity](integrity_validation.json). Tests do not launch the game
or demonstrate visual rendering on every modlist.
