# Sol's Searing Orb and Call Lightning

CALLLIH IWDEE has 23 frames and one cycle; EET SPFIRSED has 50 frames and
five cycles. CALLLIH is byte-identical to IWDEE SKYBOLT: one physical copy
is distributed. SPCALLLI is an EET duplicate and remains excluded.

## Sol's Searing Orb

The target retains the SSORBH impact introduced in beta.8. Travel uses
SSORBT: 90 frames, nine directions, matching IWDEE SSORB.PRO's granularity 9.
The mod verifies that SPPR614 still creates SORB and that its installed
weapon has the recognized PFIRE3 projectile and impact. It clones the
installed PRO, registers SRIOSORB with ADD_PROJECTILE, and changes only
SORB's projectile index. PFIRE3 and root SPPR614 remain byte-identical.

Only graphics fields in the clone change: BAM flags 0x100 = 0x280,
reference 0x104 = srioorbt and orientation 0x133 = 9. The old smoke/light
settings are not layered over the new artwork. Installed speed (40 in the
baseline), sounds, behavior flags, damage, saves and conditions remain.
The IWDEE PRO, which has speed 48, is not imported.

Unknown graphics/trails, area projectiles, Pillar behavior and detached
weapons are skipped. A private file or SRIOSORB symbol collision in either
PROJECTL.IDS or MISSILE.IDS aborts before resource writes.

## Call Lightning

IWDEE PROJECTL index 22 resolves CALLLIH.PRO -> CALLLIH; EET resolves the
same index to SKYBOLT.PRO -> SKYBOLT. Both PROs are single-target with Hit
Immediately + Pillar (0x88), BAM flags 0x280, cycle zero and orientation one.
The IWDEE artwork differs from the six-frame EET animation.

After checking the native configuration and SPPR302 chain missiles 81-91,
the mod replaces only SKYBOLT.BAM with the original CALLLIH bytes. SPLs,
PROs, chain indexes, lightning count, delays, damage and sounds are unchanged.
Other spells/items sharing SKYBOLT receive the same artwork; no additional
caster VVC or lightning bolts are created.

CALLLIH.PRO -> CALLLIH.BAM is direct file evidence. Its use in hardcoded
chains is an engine association, not a fabricated literal SPL/PRO graph edge.
Rendering position, frequency and sequence still require an in-game test.

## Verification

24 projectile cases cover installed speed/audio, unknown/missing/truncated
resources, detached weapons, other chains, private files and IDS-only
collisions, stable reinstall and exact uninstall. The beta.12 package has
41 BAMs, 37 VVCs and 1,409 physical frames after removing SR Shadow Door.
Web, Horrid Wilting and dimensional-door resources remain unchanged.

[Projectile results](projectile_validation.json),
[source hashes](projectile_source_validation.json),
[full EET results](IWD_validation.json), [IWDEE decisions](iwd_selection_recheck.csv).

Technical references: [IESDP PRO V1](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/pro_v1.htm)
and [WeiDU ADD_PROJECTILE](https://weidu.org/WeiDU/README-WeiDU.html#ADD_PROJECTILE).
