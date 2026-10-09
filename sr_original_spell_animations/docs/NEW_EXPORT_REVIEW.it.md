# Nuovi export EET/IWDEE — beta.8

Controllati i due ZIP del 9 ottobre 2026: tre risorse EET e due BAM IWDEE,
CRC integri e nessuna sovrascrittura conflittuale delle sorgenti precedenti.
Gli archivi originali restano invariati.

| Risorsa | Risultato | Azione |
|---|---|---|
| `SPCALLLI.BAM` IWDEE | Byte-identico all'EET, 18 frame, 1 ciclo | Nessuna copia ridondante |
| `SKYBOLT.BAM` IWDEE/EET | 23 contro 6 frame, 1 ciclo; grafica e ancore differenti | Candidato distinto, non importato |
| `SLAYLIVE.ITM` EET | Impatto opcode 141, parametro 2 = 39, bersaglio 2 | Sostituito il solo cue con `SLIVINH` privato |
| `SORB.ITM` EET | Impatto opcode 215, `ICFIRSDI`, parametro 2 = 0, bersaglio 2 | Sostituito il solo riferimento con `SSORBH` privato |

## SPCALLLI e Call Lightning

La precedente richiesta di SPCALLLI era una verifica di un candidato per nome,
non un'attribuzione dimostrata. Il controllo ora la esclude: nei file forniti
SPPR302 non richiama SPCALLLI, AMCALL o CALLLIGH.
SPCALLLI è richiamato dai controller AMCALL.VVC/CALLLIGH.VVC dei due giochi;
in EET anche da BDZAP.SPL direttamente e da SPIN656/SPIN721 tramite CALLLIGH.
Questi riferimenti non provano un collegamento alla spell originale SPPR302.
L'identità byte per byte tra i due BAM esclude comunque una nuova grafica IWDEE.

IESDP distingue [SKYBOLT da SPCALLLI](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op215)
e documenta [le catene Call Lightning 81–91](https://gibberlings3.github.io/iesdp/files/ids/bgee/missile.htm).
SPPR302 EET usa 81–85, IWDEE 85–91. Nei rispettivi PROJECTL.IDS mancano i nomi
PRO per quelle catene: sono gestite dal motore. SKYBOLT.PRO EET usa il BAM
SKYBOLT ma ha MISSILE 23, non gli indici selezionati da SPPR302.
Nell'export IWDEE non è presente un riferimento binario letterale a SKYBOLT.
L'attribuzione alla catena deriva dunque dalla documentazione del motore,
non da un percorso SPL → PRO presente nei file.

SKYBOLT IWDEE è diverso dal BAM EET e dai BAM SR selezionati; è ora registrato
come candidato per SPPR302 con tale limite esplicito. Non viene sovrascritto
globalmente: resta da verificare nel gioco la risoluzione della catena, il suo
uso condiviso e l'impatto del passaggio da 6 a 23 frame sulla sincronizzazione.
Non mancano altri export BAM per questo confronto; manca la prova nel motore.

## I due effetti di colpo integrati

IWDEE richiama SLIVINH.VVC direttamente da SPPR511 e SSORBH.VVC da SPPR614:
sono effetti sul bersaglio. EET invece crea le armi temporanee SLAYLIVE e SORB
tramite opcode 111. La beta.8 sostituisce l'animazione nel loro effetto di colpo,
senza aggiungerla al caster e senza importare armi/meccaniche IWDEE.

Il patcher legge la spell principale senza modificarla e accetta solo il
richiamo 111 riconosciuto (bersaglio caster, p1=1, p2=0, durata positiva,
timing 0). Poi valida firma ITM V1, header da 56 byte, blocchi effetti,
bersaglio, timing e singolo visuale riconosciuto. File assenti, armi scollegate,
cue aggiuntivi o configurazioni diverse vengono saltati.
SORB conserva il proprio opcode 215 e modalità non collegata al bersaglio;
SLAYLIVE cambia il cue grafico 141/39 in 215 non collegato (modalità 0), come
il cue sorgente IWDEE. Tutti gli altri byte dei due oggetti restano identici:
danni, salvezze, probabilità, effetti condizionali, icone, header e proiettili.
Le due root SPL restano byte-identiche.

`SSORBT` non è incluso: è il BAM di viaggio di SSORB.PRO IWDEE. SORB EET
usa invece PFIRE3 (MISSILE 258); compatibilità di flag, orientamento, palette
e tempi del viaggio non ancora verificata. Includere SSORBH non equivale
quindi a importare tutte le fasi dell'incantesimo.

## Verifica

PASS: installazione indipendente/insieme a SR su 44 SPL e 2 ITM EET reali,
reinstallazione stabile e disinstallazione byte-esatta. PASS: 30 casi delle
armi temporanee, comprese condizioni separate, root repurpose/assenti,
visuali sconosciuti, bersagli errati, ritardi e file malformati.
Web e Abi-Dalzim restano byte-identici e senza asset privati installati.
Totale pacchetto: 40 BAM, 38 VVC, 1.316 frame fisici; 13 anteprime esistenti.
Confronto completo: 248 BAM IWDEE, 387 EET e 224 SR (859 in totale).
Restano 40 candidati distinti non integrati, 6 esclusioni esplicite e le fasi
non associate di BAM già inclusi. Nessun nuovo overlap SR per i due impatti.
**Nessuna partita EET è stata avviata: la resa finale deve essere verificata.**

Hash e risultati: [new_export_validation.json](new_export_validation.json),
[item_validation.json](item_validation.json), [IWD_validation.json](IWD_validation.json),
[iwd_item_mapping.json](iwd_item_mapping.json),
[source_archive_inventory.json](source_archive_inventory.json).
