# Ricontrollo completo del repository — beta.10

Ricontrollo del 12 ottobre 2026, sulla beta.9 pubblicata e sulla correzione
beta.10. Tutte le risorse dichiarate dal mod sono presenti e valide.
È stato riprodotto e corretto un errore dell’installer; conteggi, README,
rapporti e istruzioni sono stati riallineati. Nessuna partita EET è stata avviata.

## Errore riprodotto e corretto

Se PROJECTL.IDS conteneva già SRIOSORB, ma SRIOSORB.PRO era assente,
ADD_PROJECTILE saltava la creazione. La beta.9 completava l’installazione
e assegnava comunque quell’indice a SORB: nell’esempio riprodotto 7778,
con il file PRO mancante. Il normale controllo FILE_EXISTS_IN_GAME non
rilevava questa collisione, perché il nome era occupato solo nella tabella IDS.

La beta.10 controlla SRIOSORB sia in PROJECTL.IDS sia in MISSILE.IDS,
senza distinzione maiuscole/minuscole, prima di copiare asset o modificare
spell/armi. Una collisione interrompe il solo componente IWDEE con un
messaggio esplicito. Non riutilizza il nome o l’indice occupato e non lascia
l’arma con un collegamento inesistente. Tre nuovi casi coprono la presenza
solo in PROJECTL, solo in MISSILE e in entrambe le tabelle, senza alcun PRO.

## Verifiche completate

| Controllo | Esito |
|---|---|
| Tutti i 42 BAM, 1.429 frame, palette, RLE e cicli | PASS |
| Tutti i 38 VVC: dipendenze, indici delle fasi, nomi e corrispondenza alle sorgenti | PASS |
| Tutte le 15 GIF e relativi hash degli asset | PASS |
| 44 SPL e 2 ITM EET esportati: installazione singola/insieme a SR | PASS |
| Reinstallazione stabile e disinstallazione byte-esatta | PASS |
| Ordine SR → IWDEE e IWDEE → SR: stessi file finali | PASS |
| Disinstallazione IWDEE mantenendo SR: risorse SR conservate | PASS |
| Installer English e Italiano, TLK invariato | PASS |
| 24 casi dei proiettili, incluse collisioni IDS senza PRO | PASS |
| 30 casi delle armi temporanee, 44 overlay, 12 sottospell, 28 regressioni | PASS |
| Sei casi dei cue doppi di Chaos con condizioni distinte | PASS |
| Profili sintetici EET/BG2EE e layout SPL originali SR | PASS |
| Generatore IWDEE: asset, mapping, librerie e TP2 riprodotti byte per byte | PASS |
| Windows installer: identico al weidu.exe ufficiale della release 251 | PASS, hash; non eseguito su Windows |
| Tutti gli 861 BAM sorgenti: 249 IWDEE, 388 EET, 224 SR | PASS, decisioni identiche alla beta.9 |
| Otto archivi sorgente: hash e provenienza | PASS |
| Web e Abi-Dalzim: SPL invariate e asset privati assenti | PASS |

Il clone di Sol’s Searing Orb conserva tutti i byte del PRO installato
tranne flags BAM, riferimento grafico e orientamento. Solo l’arma SORB
cambia indice per usare il clone; PFIRE3 e la root SPPR614 restano identici.
Call Lightning cambia il BAM condiviso SKYBOLT; tutte le SPL/PRO e gli indici
delle catene restano invariati. CALLLIH/SKYBOLT IWDEE sono un solo asset fisico.
Le immagini di icone e le meccaniche SR/IWDEE non sono importate.

## Coerenza corretta

- Uniformati versione, date e conteggi dei rapporti. I rapporti delle vecchie
  beta restano identificati come storici.
- Corrette le affermazioni generiche sugli indici dei proiettili: SORB è
  l’eccezione esplicita che usa un clone generato dal PRO EET.
- Riallineato il messaggio dell’installer all’ordine indicato nei README:
  dopo i mod delle spell e, per EET, dopo EET_end.
- Verificata l’uguaglianza dei due README inglesi dopo la normalizzazione
  dei link, e la presenza di ogni spell/child/overlay/arma nelle tabelle.
- Il riepilogo dell’audit legge ora la versione direttamente dal TP2,
  evitando una versione numerica separata che potrebbe restare vecchia.

## Cosa resta fuori dalla verifica

Questa è una selezione documentata: **38 BAM distinti IWDEE restano da
integrare**, più **tre fasi di BAM già inclusi** (HEALH differito in
Regeneration e GLDUSTA di area, diffusione/anello). Non è emersa una nuova
omissione attiva dimostrata nella selezione SR o negli asset dichiarati.
Le sei risorse di Web/Abi-Dalzim restano esclusioni richieste, non omissioni.

I test eseguono WeiDU su copie degli export con KEY/TLK minimi. Non provano
la resa effettiva nel motore EET né la compatibilità con ogni futura modlist.
Posizione, blending e sincronizzazione vanno verificati nel gioco;
in particolare le catene hard-coded di Call Lightning. Non viene dichiarata
una prova visiva che non è stata eseguita.

[Riepilogo verificabile](repository_recheck_validation.json),
[test EET](IWD_validation.json), [proiettili](projectile_validation.json),
[integrità](integrity_validation.json),
[installer Windows](windows_installer_validation.json),
[selezione completa IWDEE](iwd_selection_recheck.csv),
[candidati](iwd_pending_candidates.csv),
[fasi non integrate](iwd_unbound_included_art.csv).
