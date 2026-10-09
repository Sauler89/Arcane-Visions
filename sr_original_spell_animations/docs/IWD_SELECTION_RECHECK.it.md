# Ricontrollo delle esclusioni IWDEE — beta.3

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

Il confronto comprende 246 BAM IWDEE, 386 EET e 14 SR. I quattro BAM aggiunti
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

## Tutti i BAM sono ora inclusi?

**No.** La beta.3 contiene 19 BAM IWDEE per 20 spell originali, oltre al
componente SR. Il [CSV completo](iwd_selection_recheck.csv) riclassifica
ciascuno dei 246 BAM forniti:

| Stato | BAM |
|---|---:|
| Inclusi | 19 |
| Grafica o sagoma già presente nei BAM EET confrontati | 174 |
| Spell già coperta da SR, con grafica distinta non selezionata | 5 |
| Nessuna corrispondenza tracciata con una spell originale BG | 6 |
| Candidati distinti ancora da integrare | 42 |

I 42 candidati **non sono esclusi per overlap SR**. Comprendono, per esempio,
`WEBC`, `GREASEB/C`, `ORSPHEC`, `RESURRH`, `LIGHTNT`, `CLIGHTT`, `DISINTT`
e molte animazioni di nubi/aree. Richiedono l'analisi della relativa fase,
sottospell, arma o PRO già installato. Alcuni riferimenti nell'audit originario
sono dichiarati ma non provati attivi: la presenza di un BAM nel grafo non
basta a dimostrare che venga mostrato. Non vengono aggiunti a un caster o a
un bersaglio arbitrario solo per renderli visibili.

La classificazione delle corrispondenze è più ampia del precedente conteggio
163 identici + 1 ciclo: comprende anche le sagome ricolorate e i RGB emessi.
È riferita agli export forniti, non a tutti i BAM di ogni possibile EET.

## Verifica

PASS: componente IWDEE da solo e insieme a SR, 20 SPL IWD + 16 SPL SR reali
esportate, reinstallazione stabile e disinstallazione con ripristino byte
per byte. PASS: 44 nuovi casi per i quattro overlay, oltre ai 22 precedenti.
Sono mantenuti stato, durata, condizioni, icone, proiettili, effetti globali
e meccaniche. Sono provati riferimenti sconosciuti, visuali aggiuntivi,
collisioni, layout malformati e il Globo maggiore preesistente in opcode 215.

Risultati: [overlay_validation.json](overlay_validation.json),
[IWD_validation.json](IWD_validation.json),
[riepilogo selezione](iwd_selection_recheck.json).
**La resa dentro una partita EET non è ancora stata verificata.**
