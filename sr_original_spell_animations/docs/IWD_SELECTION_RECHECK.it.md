# Ricontrollo delle esclusioni IWDEE — aggiornamento beta.7

Il pacchetto precedente **non importava tutti gli effetti distinti IWDEE**.
I 15 BAM erano una selezione di cue diretti riconosciuti nelle spell EET.
Il filtro per gli opcode 141/215 aveva trascurato gli overlay persistenti.
L'esclusione dei Globi nel vecchio README riguardava correttamente le icone
SR, ma non giustificava l'esclusione delle loro vere animazioni IWDEE.

## Effetti segnalati e correzioni

| Spell originale BG | BAM IWDEE | Overlap SR/EET confrontati | Esito beta.3 |
|---|---|---|---|
| Sanctuary, `SPPR109` | `SANCTRY` | Nessuna corrispondenza completa, ciclo, immagini, sagome o RGB emessi | Incluso come `sriosanc`; opcode 153 mantenuto |
| Protection from Arrows / Normal Missiles, `SPWI311` | `PFNMISC` | Nessuna | Incluso come `srioarrw`; opcode 156 mantenuto |
| Minor Globe of Invulnerability, `SPWI406` | `MGOINVC` | Nessuna | Incluso come `sriomglb`; opcode 155 mantenuto |
| Globe of Invulnerability, `SPWI602` | `GOINVUC` | Nessuna | Incluso come `sriogglb`; opcode 155 EET o 215 preesistente mantenuto |
| Call Lightning, `SPPR302` | Fulmine verticale da identificare/confrontare | Non determinabile: BAM assente dagli export | In attesa dei BAM IWDEE/EET `SKYBOLT`; non escluso per overlap SR |

Il confronto beta.3 comprendeva 246 BAM IWDEE, 386 EET e 14 SR;
la beta.4 ricontrolla tutti i 224 BAM dell'archivio SR. I quattro BAM aggiunti
sono byte-identici agli originali IWDEE. Ognuno ha un ciclo di 16 frame.
Protection from Arrows usa il controller IWDEE `#PRONM`; il Globo maggiore
usa `#GLOBINV`. Sanctuary e Globo minore, richiamati direttamente come BAM
in IWDEE, hanno un wrapper ripetuto derivato da `#PRONM`, compatibile con il
loro singolo ciclo. Nessun suono, palette esterna o alpha BAM viene importato.

## Come vengono mantenute le meccaniche

Non si elimina l'opcode Sanctuary e non si trasforma la spell in una semplice
animazione. L'opcode 153 resta 153, con gli stessi bersagli, durata, potenza,
probabilità, tiri salvezza e flag di dissoluzione/resistenza. Gli opcode 155
e 156 restano anch'essi invariati. Si modifica solo la scelta della grafica
personalizzata (parametro 2) e il suo riferimento. Gli effetti 83/102 e gli
altri effetti che danno realmente le protezioni restano byte-identici.

La modalità grafica personalizzata è documentata da
[IESDP opcode 153](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op153),
[155](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op155) e
[156](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op156).
I controller girano finché dura l'effetto già installato. I due Globi hanno
risorse private distinte; `MINORGLB`, gli oggetti e altre spell non vengono
sovrascritti globalmente. Una configurazione sconosciuta viene saltata.

## Call Lightning: cosa manca

Le SPL IWDEE esportate usano i valori projectile 85–91; quelle EET 81–85.
Sono le catene hard-coded di Call Lightning, non i proiettili di Lightning
Bolt (`LIGHTNT`) o Chain Lightning (`CLIGHTT`). Gli export non contengono un
PRO risolto per queste catene, né i BAM IWDEE `SKYBOLT`/`SPCALLLI`.
L'EET esportata contiene `SKYBOLT.PRO`, il cui campo grafico punta a
`SKYBOLT.BAM`; il CHITIN.KEY EET conferma il nome, ma il BAM non è stato
esportato. `SPCALLLI.BAM` EET è invece già disponibile.

Per completare il confronto servono, in cartelle separate:

- **IWDEE:** `SKYBOLT.BAM`; anche `SPCALLLI.BAM` se presente.
- **EET:** `SKYBOLT.BAM`.

I nomi sono candidati da verificare nell'installazione IWDEE; il fatto che
SKYBOLT sia presente nel KEY EET non prova che la catena IWDEE usi lo stesso
asset o che sia esclusivo. Non viene forzata un'animazione senza tale prova.
Non si importano numero di fulmini, ritardi, selezione dei bersagli o danni IWDEE.

## Ricontrollo completo beta.4

La beta.4 aggiunge anche `GLDUSTA`, `ORSPHEC`, `RESURRH`, `HEALH` e
`SPOISOH`: omissioni dei cue, degli overlay, delle sottospell e delle varianti
ricolorate. [Rapporto completo](FULL_SOURCE_AUDIT.it.md).

La tabella beta.3 di esclusioni è stata sostituita: la sola sagoma non prova
un duplicato. Su 246 BAM: 24 inclusi, 163 corrispondenze grafiche complete EET,
1 corrispondenza di tutti i cicli visibili, 5 spell già coperte da SR,
6 senza root originale tracciata, 6 esclusi su richiesta e **41 candidati ancora da integrare**.
Questi 41 non sono esclusi per overlap SR. [Tutte le decisioni](iwd_selection_recheck.csv),
[candidati e motivi](iwd_pending_candidates.csv), [tutti i BAM SR](sr_source_selection.csv).

PASS: 44 SPL EET reali, 44 casi overlay, 28 regressioni e 12 casi sottospell.
Nessun test visivo dentro una partita. Vedere il rapporto completo per le
richieste mirate di file e i limiti dei riferimenti PRO dichiarati.

## Ulteriore controllo beta.5

Aggiunto `MMAGICH` per Miscast Magic: era un cue diretto erroneamente
classificato come fase PRO. `CONFUSH`, già incluso per Sphere of Chaos,
ora copre anche Confusion sacerdotale e arcana e Chaos. Chaos conserva
due cue con condizioni separate e la durata/timing EET. Sei casi aggiuntivi
verificano la coppia riconosciuta e il salto delle coppie sconosciute.

Il rapporto distingue anche BAM inclusi da binding ancora assenti:
[iwd_unbound_included_art.csv](iwd_unbound_included_art.csv). Vi restano la
fase HEALH differita di Regeneration e due fasi GLDUSTA di area
Glitterdust, senza binding EET equivalenti.

## Esclusione richiesta nella beta.6

Web (`SPWI215`) è rimosso dalla selezione: nessuna patch di spell o
proiettile, nessun BAM/VVC privato, nessuna anteprima. `WEBA`, `WEBC` e
`WEBX` restano inventariati come esclusioni del proprietario.

Il ricontrollo rileva due campi di area `GLDUSTA` in IWDEE `GLDUST.PRO`
(diffusione e anello). Il cue sul bersaglio è incluso; quelle fasi non
lo sono. EET usa invece `SPARGONP.PRO`, condiviso e con campi grafici diversi.
Non è emerso un altro BAM SR attivo da aggiungere alle spell tracciate.

## Esclusione richiesta nella beta.7

Orrido avvizzimento di Abi-Dalzim (`SPWI812`) mantiene la grafica installata
in BG2EE/EET. Rimossi il cue privato `sriowilt`, il relativo BAM/VVC e la
patch. `ADHWILH`, `ADHWILA` e `ADHWILX` sono esclusioni del proprietario,
non omissioni. I test verificano che la SPL resti byte-identica sia col
componente IWDEE da solo, sia insieme al componente SR.
