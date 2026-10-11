# Sol’s Searing Orb e Call Lightning — beta.9

I due nuovi BAM sono stati controllati integralmente. `SPFIRSED.BAM` EET
ha 50 frame e 5 cicli; `CALLLIH.BAM` IWDEE ha 23 frame e un ciclo.
CALLLIH è byte-identico allo SKYBOLT IWDEE già ricevuto: viene inclusa una
sola copia fisica, non due effetti sovrapposti. SPCALLLI resta un duplicato EET.

## Sol’s Searing Orb

Il bersaglio conserva il cue SSORBH aggiunto nella beta.8. Ora è inclusa
anche la grafica di viaggio SSORBT: 90 frame, 9 direzioni, contro i 5 cicli
del vecchio SPFIRSED. La sorgente IWDEE `SSORB.PRO` conferma la granulosità 9.

Il mod verifica che SPPR614 crei ancora SORB e che l’arma usi il proiettile
PFIRE3 riconosciuto e il cue di impatto previsto. Clona quindi il PRO
**installato**, registra SRIOSORB tramite ADD_PROJECTILE e assegna il nuovo
indice solo all’abilità di SORB. PFIRE3 e la SPL principale restano identici.
Nel clone cambiano solo i campi grafici: flags BAM 0x100 = 0x280, riferimento
0x104 = srioorbt, orientamento 0x133 = 9. Fumo/luci del vecchio globo non
vengono sovrapposti alla nuova grafica. Velocità EET (40 nella baseline),
suoni, flag di comportamento, danni, salvezze e condizioni restano installati.
Non viene importato il PRO IWDEE, che avrebbe velocità 48.

Layout diversi, altre animazioni/trail, proiettili di area, comportamento
Pillar e armi scollegate vengono saltati. Una collisione del nome privato
SRIOSORB interrompe il componente prima delle scritture.

## Call Lightning

Il PROJECTL.IDS IWDEE associa l’indice 22 a CALLLIH.PRO, che richiama CALLLIH;
EET associa lo stesso indice a SKYBOLT.PRO, che richiama SKYBOLT. Entrambi i
PRO sono single-target, Hit Immediately + Pillar (0x88), flags BAM 0x280,
ciclo 0 e orientamento 1. La grafica IWDEE è distinta dai 6 frame EET.

Il mod verifica la configurazione nativa e le abilità SPPR302 con le catene
81–91. Sostituisce allora **solo SKYBOLT.BAM** con i byte originali CALLLIH.
SPL, PRO, indici delle catene, numero di fulmini, ritardi, danni e suoni
restano byte-identici. L’animazione visibile passa da 6 a 23 frame.
È una sostituzione condivisa: altre spell o oggetti che usano SKYBOLT
ricevono la stessa grafica. Non vengono aggiunti VVC al caster o nuovi fulmini.

Il riferimento CALLLIH.PRO → CALLLIH.BAM è provato dai file; l’uso di questo
BAM nelle catene hard-coded è un collegamento del motore. I test sui file
non eseguono il motore EET: il componente rimane beta e richiede verifica
visiva di posizione, frequenza e sequenza delle scariche nel gioco.

## Verifiche e documentazione

PASS: 21 casi reali dei proiettili, inclusi velocità/suono personalizzati,
layout sconosciuti, armi scollegate, file troncati, catene diverse e collisioni.
PASS: reinstallazione stabile e disinstallazione byte-esatta.
I controlli del pacchetto coprono 42 BAM, 38 VVC e 1.429 frame fisici.
Nessun BAM aggiuntivo è necessario per queste due integrazioni.
Web e Abi-Dalzim restano esclusi, con le loro SPL invariate.

[Risultati dei proiettili](projectile_validation.json),
[hash delle sorgenti](projectile_source_validation.json),
[verifica EET completa](IWD_validation.json),
[decisioni su tutti i BAM IWDEE](iwd_selection_recheck.csv).

Riferimenti: [IESDP PRO V1](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/pro_v1.htm)
(campi grafici 0x100/0x104/0x133 e flags Hit Immediately/Pillar),
[WeiDU ADD_PROJECTILE](https://weidu.org/WeiDU/README-WeiDU.html#ADD_PROJECTILE).
