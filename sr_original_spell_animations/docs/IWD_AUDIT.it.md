> Aggiornamento beta.7: Orrido avvizzimento (`SPWI812`) è escluso su richiesta.

> Rapporto storico della prima selezione. La beta.4 corregge anche le
> esclusioni per sagoma: [ricontrollo completo aggiornato](FULL_SOURCE_AUDIT.it.md).

> Historical review of beta.1. The overlay exclusions below are superseded by beta.3: see [IWD_SELECTION_RECHECK.it.md](IWD_SELECTION_RECHECK.it.md) and [RIGOROUS_AUDIT.md](RIGOROUS_AUDIT.md).

# Componente IWDEE: ricontrollo e integrazione

Versione 0.2.0-beta.1. Il componente 0 SR resta invariato nei suoi asset e
nelle patch. Il nuovo componente 10 contiene 15 BAM e 15 VVC isolati, per
16 spell originali di BG. I due componenti si possono installare insieme
o separatamente. Non richiedono Spell Revisions né IWDification.

## Confronto completato

Analizzati 246 BAM IWDEE, 386 BAM EET e i 14 BAM del componente SR. Per EET
sono inclusi gli alias richiesti nel secondo filtro e tutte le 17 palette
BMP richieste. Il CHITIN.KEY contiene 19.841 nomi BAM; i tre nomi non
esportati (NONE, SPAURAFD, SPENTAXL) non vi compaiono. Non servono ulteriori
esportazioni per questo componente.

| Esito sui BAM IWDEE | Numero |
|---|---:|
| Identici a risorse EET, anche rinominate o ricompresse | 163 |
| Immagini di un ciclo già presenti, con struttura differente | 1 |
| Nessuna corrispondenza completa/ciclo trovata negli export confrontati | 82 |

Gli 82 non sono automaticamente 82 nuovi effetti installabili. La selezione
finale usa 15 BAM senza corrispondenze complete, immagini ritagliate, sagome
o RGB emessi dei cicli rispetto ai 386 EET e 14 SR confrontati. Nessuna
spell già coperta dal componente SR viene modificata da quello IWD.
È una distinzione rispetto alle risorse esportate della tua EET, che include
IWDification v11, SCS e Made in Heaven, non una prova di esclusività rispetto
a tutti i BAM di tutte le installazioni e di tutti i mod possibili.

## Spell incluse

| Spell originale | SPL BG/EET | BAM IWDEE |
|---|---|---|
| Rimuovi paralisi | `SPPR308` | `RPARALH` |
| Veleno | `SPPR411` | `POISONH` |
| Ristorazione minore | `SPPR417` | `LRESTORH` |
| Cura ferite critiche | `SPPR502` | `CCWOUNH` |
| Barriera di lame | `SPPR603` | `BBARRH1`, `BBARRH2` |
| Dito della morte (divino) | `SPPR708` | `FODEATH` |
| Rigenerazione | `SPPR711` | `REGENERH` |
| Ristorazione maggiore | `SPPR713` | `GRESTORH` |
| Tempesta di vendetta | `SPPR722` | `FODEATH` |
| Incantesimo della morte | `SPWI605` | `DSPELLH` |
| Parola del potere: silenzio | `SPWI612` | `PWSILEH` |
| Sfera del caos | `SPWI711` | `CONFUSH` |
| Dito della morte (arcano) | `SPWI713` | `FODEATH` |
| Parola del potere: stordimento | `SPWI715` | `PWSTUNH` |
| Soffio del drago | `SPWI922` | `SPDRGNBR` |

I 15 BAM sono copiati senza modificare un byte; Dito della morte divino,
arcano e la grafica d'impatto di Tempesta di vendetta condividono una sola
copia di FODEATH. Barriera di lame usa due controller e due BAM. I nomi
installati, i controller e gli hash sono nei JSON di mapping e manifest.

## Patch solo grafiche

Si sostituiscono in posizione gli effetti visivi 141/215 riconosciuti negli
ability header. Nessun effetto viene aggiunto, rimosso o riordinato. Restano
identici gli header SPL, i globali di lancio, le icone, gli indici dei
proiettili, tutti gli effetti non visivi, bersagli, probabilità, salvezze,
resistenza alla magia, dissoluzione e potenza. Non si importano SPL, EFF,
PRO, ITM o CRE da IWDEE.

Per i cue singoli si usa un VVC non ripetuto e si lascia finire la sequenza,
senza il limite di 1–3 secondi delle vecchie animazioni EET. La durata delle
meccaniche resta identica. Per Barriera di lame si conserva la durata e la
modalità temporale dei due effetti visivi EET; le sequenze di introduzione,
ripetizione e fine derivano dai VVC IWDEE. I VVC non aggiungono suoni. Per
LRESTORH, GRESTORH e REGENERH, richiamati come BAM direttamente in IWDEE,
si genera un controller non ripetuto con il template visuale IWDEE.

Il patcher richiede risorse e configurazioni note. Se un altro mod cambia
il bersaglio, il riferimento, il numero di effetti visivi, inserisce una
visuale aggiuntiva o usa un layout non valido/condiviso, l'abilità viene
saltata con messaggio. Non si sovrappone una nuova grafica a quella ignota.
Questo permette l'installazione condizionale su BG2EE/EET; non garantisce
che tutte le spell siano sostituite in ogni possibile modlist.

## Esclusioni deliberate

- 163 copie già presenti e SPGLYPTI, che condivide un ciclo: esclusi.
- SPOISOH, MMAGICH e HEALH: esclusi dalla selezione perché condividono
  sagome con grafica EET, pur avendo colori diversi.
- Nuove spell IWD, icone, avatar, armi e grafica di pre-lancio: esclusi.
- Grafica dei proiettili, nubi, traiettorie e aree: non importata; un PRO
  completo potrebbe cambiare portata, collisioni, esplosioni e gameplay.
- Slay Living/Sol's Searing Orb: nessuna patch al cast quando l'impatto
  appartiene all'arma o al proiettile; evita un cue sul caster sbagliato.
- Confusion/Chaos: non si cancella l'indicatore persistente di confusione
  per sostituirlo con un flash. CONFUSH è usato solo per l'impatto diretto
  originale di Sfera del caos.
- Globo di invulnerabilità e altri overlay gestiti dal motore: non si
  disabilitano meccaniche o overlay hard-coded per forzare un BAM.

## Verifica

WeiDU 251, sulle SPL EET reali esportate, in una cartella di prova isolata
con KEY/TLK minimi. PASS per tutti i 16 SPL IWD e i 16 SPL SR: componente
IWD da solo, SR + IWD, reinstallazione stabile e disinstallazione con
ripristino byte per byte. Verificati tutti i frame/cicli dei 15 nuovi BAM,
le dipendenze e sequenze dei 15 VVC. Provato anche il salto di una spell
con una visuale aggiuntiva sconosciuta. Il cache ADD_SPELL.IDS, eliminato
da WeiDU indipendentemente dal mod, è escluso dallo snapshot. Nessuna
installazione del gioco è stata toccata o avviata. Posizione, blending e
sincronizzazione visiva devono ancora essere verificati giocando.

`IWD_validation.json` contiene l'esito per ogni spell. I test riproducibili
sono in `tests/verify_iwd_on_export.py`. Il builder in `tools/` richiede gli
export IWDEE del proprietario del gioco; non serve per installare il ZIP.

Fonti tecniche: [IESDP VVC](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/vvc_v1.htm),
[IESDP BAM](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/bam_v1.htm),
[Near Infinity BamV1Decoder](https://github.com/Argent77/NearInfinity/blob/master/src/org/infinity/resource/graphics/BamV1Decoder.java).
Il confronto ignora la compressione BAMC, verifica frame/cicli/centri e
confronta anche immagini ritagliate, sagome e contributo RGB. I run RLE
finali vengono limitati alla dimensione del frame come in Near Infinity.
