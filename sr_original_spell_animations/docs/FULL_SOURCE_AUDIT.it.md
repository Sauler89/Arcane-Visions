# Ricontrollo completo delle sorgenti — v0.2.0-beta.5

Ricontrollo del 9 ottobre 2026. Il controllo precedente aveva davvero omesso
alcuni effetti IWDEE. La beta.4 ha corretto sei omissioni; la beta.5 ne corregge altre quattro
nei collegamenti alle spell. Il rapporto distingue
i duplicati dalle varianti di colore e dalle fasi ancora da integrare.

## Sorgenti controllate

Verificati i sei ZIP forniti: SR v4.21, export degli effetti IWDEE, due pacchetti
BAM IWDEE e due pacchetti EET. Il confronto con i CRC degli ZIP conferma
**9.600 risorse locali identiche alle sorgenti**, comprese le risorse SR di
supporto. Le sorgenti non sono state modificate né copiate nel gioco.

| Sorgente | BAM decodificati | Frame fisici |
|---|---:|---:|
| IWDEE | 246 | 10.243 |
| EET esportata | 386 | 17.848 |
| Archivio SR completo | 224 | 3.661 |

Inventario e hash: [source_archive_inventory.json](source_archive_inventory.json),
[source_BAM_inventory.csv](source_BAM_inventory.csv).
Il grafo distingue effetti di lancio e dopo il lancio, sottospell, EFF,
VVC/VEF, proiettili e armi temporanee. Conserva i nomi originali senza supporre
che uno stesso numero di projectile significhi la stessa risorsa nei due giochi.

## Sei omissioni corrette nella beta.4

| Spell originale | BAM IWDEE | Risorsa EET modificata | Motivo dell'omissione precedente |
|---|---|---|---|
| Glitterdust | `GLDUSTA` | `SPWI224.SPL` | Controller `GLDUSTH.VVC` distinto dal nome del BAM; selezione incompleta |
| Web / Ragnatela sul bersaglio | `WEBC` | `SPWI215.SPL` | Overlay di stato 157, non un semplice effetto 141/215 |
| Otiluke's Resilient Sphere | `ORSPHEC` | `SPWI413A.SPL`, richiamata da `SPWI413` | Animazione in una sottospell |
| Resurrection | `RESURRH` | `SPPR712A.SPL`, richiamata da `SPPR712` | Animazione in una sottospell |
| Heal / Guarigione | `HEALH` | `SPPR607.SPL` | Variante di colore esclusa erroneamente per sagoma condivisa |
| Slow Poison / Rallentare veleno | `SPOISOH` | `SPPR212.SPL` | Variante di colore esclusa erroneamente per sagoma condivisa |

Sono sei BAM byte-identici a quelli IWDEE e sei VVC privati. **Non sono
duplicati dei BAM SR selezionati per le spell originali.** Non si importano
le SPL IWDEE, né nuove spell o meccaniche. I quattro overlay della beta.3
(Sanctuary, Protection from Arrows e i due Globi) restano inclusi.

Glitterdust conserva la fase 2 del vero controller IWDEE. Web conserva
introduzione 1 e ciclo ripetuto 2 del suo `WEBC.VVC`; l'opcode 157, lo stato
di immobilizzazione, durata, salvezza e condizioni EET restano invariati.
La Sfera usa `#OTILUKE.VVC` e Resurrezione usa `RESURRH.VVC`, con riferimenti
privati e audio rimosso. Le due sottospell vengono patchate solo se la spell
principale le richiama ancora attraverso un opcode di lancio riconosciuto.
Le spell principali restano byte-identiche. I BAM delle aree di Web non sono
inclusi da questa aggiunta: cambia l'overlay sul bersaglio.

La beta.5 contiene **40 BAM, 38 VVC e 1.279 frame fisici**, con **46 SPL EET
patchate** nei test: 16 SR e 30 IWDEE, incluse le due sottospell.

## Ulteriore controllo: quattro binding recuperati nella beta.5

| Spell originale | BAM IWDEE | Risorsa EET modificata | Omissione |
|---|---|---|---|
| Miscast Magic | `MMAGICH` | `SPPR310.SPL` | Cue diretto 215 classificato erroneamente come fase PRO; variante di colore distinta |
| Confusion sacerdotale | `CONFUSH` | `SPPR709.SPL` | BAM incluso per Sphere of Chaos, ma questa spell non era collegata |
| Confusion arcana | `CONFUSH` | `SPWI401.SPL` | Stessa omissione del binding |
| Chaos | `CONFUSH` | `SPWI508.SPL` | Stessa omissione; due cue per abilità, con condizioni separate |

Non sono overlap SR. `MMAGICH` è un nuovo BAM incluso, identico alla sorgente;
`CONFUSH` viene riutilizzato senza aggiungere copie ridondanti. Miscast Magic
sostituisce il cue EET 141/9. Per le altre tre spell si modificano solo gli
otto byte del resref dei cue 215: timing, durata, bersaglio, probabilità,
salvezza e tutti gli effetti meccanici restano identici. Il controller
IWDEE `CONFUSH.VVC` resta non ripetuto: cambia l'aspetto rispetto alla
vecchia animazione persistente EET, senza rimuovere lo stato di confusione.

Il patcher ora riconosce anche una coppia dello stesso cue. Una coppia con
un secondo visuale sconosciuto, un solo cue, un terzo visuale, un secondo
cue ritardato o un bersaglio diverso viene saltata. Sei regressioni aggiunte
verificano questi casi e condizioni indipendenti per i due cue.

Controllati anche i BAM già inclusi per cercare spell senza collegamento,
e i resref grafici presenti in tutte le SPL/EFF fornite, oltre al grafo.
I riferimenti 296 sono immunità al visuale, non richiami di animazioni;
i nomi residui negli opcode di colore/testo non sono binding grafici.
I riferimenti omonimi 177/232 e quelli degli oggetti vengono risolti nel
loro tipo di risorsa, senza trattarli come BAM. Non è emerso un altro BAM
SR attivo da aggiungere alle spell originali nella selezione tracciata.

Il generatore produce ora le motivazioni dei candidati dal percorso reale
ed elenca separatamente [i binding mancanti di BAM già inclusi](iwd_unbound_included_art.csv).
Rimane `HEALH` nella fase aggiuntiva differita di Regeneration IWDEE:
la baseline EET ha solo il cue iniziale già sostituito con `REGENERH`.
La fase aggiuntiva non viene introdotta senza un binding corrispondente.
Le 45 risorse candidate non esauriscono ogni possibile fase ancora assente.

## Errori del filtro e del codice

- **Una sagoma comune non prova una grafica duplicata.** Il vecchio filtro
  aveva escluso dieci BAM con sagome condivise ma colori/grafica differenti:
  `CLOUDKX`, `FIREBAA`, `FIREBAR`, `FIREBAT`, `FIREBAX`, `GREASEX`, `HEALH`,
  `MMAGICH`, `SPOISOH`, `SSORBT`. Heal e Slow Poison sono ora integrati;
  Miscast Magic viene integrato nella beta.5; gli altri sette restano
  candidati, senza essere etichettati come duplicati.
- **Un ciclo condiviso non basta a escludere tutti gli altri cicli del BAM.**
  Il nuovo confronto separa file/grafica completa, tutti i cicli visibili,
  corrispondenze parziali e sagome puramente diagnostiche.
- Il patcher dei cue diretti contava solo gli opcode 141/215. Poteva quindi
  modificare una spell anche in presenza di un overlay aggiuntivo 153–158.
  Ora li rileva e salta l'abilità; sei regressioni provano questi casi.
- Il generatore ora risolve i nomi delle sorgenti senza distinguere maiuscole
  e minuscole. `gldusth.VVC`, `webc.VVC` e altri nomi reali vengono letti
  correttamente anche su Linux; il nome del controller può differire dal BAM.
- Il controllo del grafo non segue un campo PRO secondary quando il flag
  è disattivo o le ray lo sopprimono. I campi dichiarati e gli indici annidati
  non confermati non vengono presentati come prova di una fase visibile.

## Classificazione completa IWDEE

| Esito | BAM |
|---|---:|
| Inclusi | 26 |
| File o grafica completa già presenti in EET | 163 |
| Tutti i cicli visibili con la stessa grafica, senza richiedere gli stessi ancoraggi | 1 |
| Spell già coperta da SR, variante IWDEE non selezionata | 5 |
| Nessuna corrispondenza dopo il lancio con una spell BG originale tracciata | 6 |
| Candidati distinti ancora da integrare | 45 |

Il precedente conteggio di 42 candidati non era definitivo: vengono
riammessi dieci BAM esclusi per sagoma e integrati sei nella beta.4, quindi erano 46. Con Miscast Magic nella beta.5
restano **45**. Questi 45 **non sono esclusi per overlap con SR**. Sono documentati uno per
uno, con root, percorso e motivo, in
[iwd_pending_candidates.csv](iwd_pending_candidates.csv).

Comprendono Lightning Bolt (`LIGHTNT`), Chain Lightning (`CLIGHTT`),
Disintegrate (`DISINTT`), Agannazar's Scorcher (`ASCORCT`), nubi, aree,
anelli e fasi di viaggio/colpo. Non sono tutti fasi già provate attive:
un resref compilato in un PRO può essere disattivato dai suoi flag. Servono
patch dei rispettivi binding già installati e verifiche di controller,
palette, orientamento e durata, invece di aggiungere un VVC sul caster.

Grease `GREASEB/C` usa sottospell condizionali IWDEE assenti nella baseline
EET, che ha invece l'overlay 158. Non viene forzata una delle due varianti
senza ricostruire le condizioni. Slay Living e Sol's Searing Orb in EET
creano armi temporanee: `SLIVINH` e `SSORBH/T` non vanno messi sul caster
al posto dell'effetto del colpo. La fase Heal aggiuntiva/differita di
Regeneration resta una fase non importata; `HEALH` è ora usato da Heal.

Tutte le 246 decisioni e i confronti contro l'intero archivio SR sono in
[iwd_selection_recheck.csv](iwd_selection_recheck.csv). Una corrispondenza
con un'icona o una nuova spell SR non equivale all'overlap con il componente SR.
Le esclusioni senza root includono risorse orfane o di magie IWDEE non BG;
non vengono collegate arbitrariamente a spell con nomi simili.

## Ricontrollo SR completo

| Esito dei BAM nell'archivio SR | File |
|---|---:|
| Animazioni incluse | 14 |
| Icone | 178 |
| Grafica di ali/avatar/equipaggiamento | 17 |
| Nuove spell, sostituzioni con nuove spell o grafica di oggetti | 8 |
| Non installati o controller senza richiamo visivo attivo trovato | 6 |
| Grafica di strumenti non usata come effetto di spell | 1 |

**Non è emerso un altro BAM SR con un binding attivo dimostrato alle spell
originali da aggiungere.** Le 224 decisioni conservano hash, COPY diretti,
riferimenti grafici e iconici in [sr_source_selection.csv](sr_source_selection.csv).
Controllati anche i 28 script BCS forniti: nessun richiamo letterale ai VVC
di SR introduce un altro collegamento grafico.

`a#shope/a#ishope` e `a#spain/a#ispain` vengono copiati, ma nei file e
nel codice attivo forniti non è stato trovato un richiamo ai rispettivi
controller. `dvholya1/2` appartengono al blocco d'installazione commentato;
`spdimndr` non viene installato; `spccoldl` usa COPY_EXISTING sul BAM del gioco,
non quello nell'archivio. `mestsh`, `dvsburst`, `spstorms`, `icelance` e
`dvvtrsph/dvvtrtra` appartengono a nuove spell o sostituzioni fuori ambito.
La copia `dvsburst` compare in due cartelle, entrambe inventariate.

## File ancora utili

- **Call Lightning:** IWDEE `SKYBOLT.BAM` e `SPCALLLI.BAM` se presenti;
  EET `SKYBOLT.BAM`. Il BAM EET `SPCALLLI` è già disponibile. La catena è
  hard-coded e non si confonde con Lightning Bolt o Chain Lightning.
- **Effetti di colpo delle armi temporanee:** EET `SLAYLIVE.ITM` e `SORB.ITM`.
  Dopo la lettura potranno essere richieste solo le loro eventuali dipendenze
  effettive. Non servono altre esportazioni generiche di tutte le SPL/PRO.

Gli [export mancanti nel grafo EET](missing_EET_dependencies.csv) e
[IWDEE](missing_IWDEE_dependencies.csv) includono anche oggetti e riferimenti
fuori ambito: non sono una richiesta di esportarli tutti. I rami annidati
con indici non confermati restano segnalati come tali.

## Verifiche e limiti

- PASS sui 46 SPL EET esportati, componente IWDEE indipendente e insieme a SR:
  reinstallazione stabile, ripristino byte per byte dopo disinstallazione.
- PASS: sei nuovi casi della coppia Chaos, 54 casi degli overlay,
  28 regressioni generali e 12 casi delle
  sottospell, comprese root assenti, scollegate, troncate o riproposte come
  immunità anziché lancio.
- PASS: byte delle condizioni/meccaniche, effetti globali, icone, indici
  dei proiettili; tutti i BAM identici alle sorgenti e tutte le dipendenze
  VVC risolte. Fasi, coordinate e flag dei VVC IWDEE conservati dalle sorgenti.
- PASS: SR originale, profili sintetici EET/BG2EE, nomi privati, RLE/cicli,
  14 GIF e relativi hash, collegamenti locali dei README.

Una risorsa dell'export EET, `CDDETECT.SPL`, ha una firma `ITM V1  `:
segnalata nel CSV degli input, ma estranea al mod e non modificata.
Gli indici hard-coded senza PRO e le assegnazioni dinamiche SR sono limiti
espliciti del grafo, non errori di installazione del nostro pacchetto.

I test usano copie isolate delle risorse esportate e KEY/TLK minimi, non
l'intera installazione del proprietario. **Nessuna partita è stata avviata**:
posizione, blending e sincronizzazione effettiva richiedono controllo in gioco.
La selezione dipende dagli export forniti; non copre tutti i BAM del KEY EET
né risorse IWDEE non esportate. Crediti e termini delle sorgenti sono mantenuti.

Risultati: [source_coverage_summary.json](source_coverage_summary.json),
[IWD_validation.json](IWD_validation.json),
[overlay_validation.json](overlay_validation.json),
[regression_validation.json](regression_validation.json),
[child_validation.json](child_validation.json),
[integrity_validation.json](integrity_validation.json).

Riferimenti tecnici: [IESDP opcode 157](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op157),
[VVC](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm),
[PRO](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/pro_v1.htm).
