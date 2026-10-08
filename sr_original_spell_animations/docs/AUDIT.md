> Historical review of the previous beta. For the current installer see [RIGOROUS_AUDIT.md](RIGOROUS_AUDIT.md).

# Ricontrollo completo — 8 ottobre 2026

Pacchetto aggiornato da **0.1.0-beta.1** a **0.1.0-beta.2**.
Il contenuto resta: **14 BAM di animazioni, 12 VVC, 16 SPL originali patchati**,
piu le sostituzioni native per Entangle, Chromatic Orb e l'overlay SPMAGGLO.
Spell Revisions non e necessario.

| Area | Esito del controllo |
|---|---|
| Selezione degli asset | Confermati i BAM installati dal codice attivo di SR per le magie originali; escluse icone, avatar, magie nuove e risorse inutilizzate. Nessun asset aggiunto. |
| Integrita BAM | Tutti identici ai sorgenti SR; verificati 324 frame, cicli, indici, palette, decompressione e dati RLE. |
| Dipendenze VVC | Tutti i BAM richiesti presenti; nessuna dipendenza grafica o sonora esterna rimasta. |
| Falsa Alba | Il riferimento alla sequenza 3 e valido: i VVC usano indici da 1, quindi seleziona il terzo ciclo BAM. Nessuna correzione al VVC necessaria. |
| Animazioni degli elementali | Corretto target 2 in target 1 (caster), mantenendo play-on-point. Un punto vuoto non fornisce una creatura destinataria. Rimosso il taglio arbitrario a due secondi: ora la sequenza non ciclica viene riprodotta interamente. |
| Aura di Mantello | Corretta la scelta della durata: segue opcode 120, la protezione dalle armi, anziche qualunque effetto piu lungo. Eredita anche destinatario, potenza, probabilita, salvezza e comportamento di dissoluzione/resistenza della protezione. |
| Mantello non standard | Se manca una protezione temporizzata diretta, usa la durata della vecchia aura; in assenza di entrambe usa 24 secondi e stampa un messaggio. Buff delegati a EFF/subspell richiedono verifica nel gioco. |
| Validazione SPL | Aggiunti controlli sugli effetti globali di lancio e sui blocchi condivisi, sovrapposti o fuori ordine. I layout non supportati vengono saltati, senza riscrivere il file. |
| Gameplay e icone | Effetti non grafici conservati byte per byte nei test; invariati icone, livelli, proiettili, effetti globali, EFF di evocazione e creature. |
| Installazione | Verificati EET/BG2EE, Italiano/Inglese, reinstallazione stabile, risorse mancanti, file malformati e guardia per giochi non supportati. |
| Disinstallazione | Ripristino dei byte precedenti e rimozione di tutte le risorse introdotte verificati. |
| Documentazione | Versione, lista, esclusioni, limiti e istruzioni aggiornati; aggiunti test riproducibili. DVmeteor escluso perche usa il BAM originale SPFSTRMI. |

La verifica dei VVC ha considerato anche le fasi iniziale, continua e finale,
non soltanto la prima sequenza mostrata nella GIF. I VVC mantengono le
impostazioni di rendering di SR; cambiano soltanto i riferimenti ai nomi
isolati e la rimozione dei riferimenti sonori.

Le risorse native sono condivise dal motore: sostituire SPMAGGLO modifica
anche altre magie o oggetti che usano quell'overlay. Le patch sostituiscono
gli effetti grafici 215/141 negli incantesimi selezionati, comprese eventuali
varianti visive introdotte da altri mod. Se un mod cambia completamente la
magia associata a uno slot originale, serve una verifica specifica.

**Non e stata eseguita una prova dentro un'installazione EET reale.**
Restano da verificare posizione e fusione visiva dei BAM, resa durante
l'invisibilita, dissoluzione delle aure e sincronizzazione degli elementali.
Le prove automatizzate verificano i dati e l'installer, non il rendering del
motore. Non dimostrano compatibilita universale con qualunque combinazione
di altri mod. Vedi VALIDATION.md per i dettagli e README.md per i crediti e
le condizioni di ridistribuzione indicate dal sorgente SR.
