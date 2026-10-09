# Arcane Visions — Spell Effect Animations

**Animazioni degli effetti dopo il lancio delle spell originali di BG, per EET/BG2EE.**
Versione **v0.2.0-beta.5**, di **Sauler89**. Spell Revisions e IWDification non servono.

| Componente | Contenuto |
|---|---|
| **0 — SR** | 14 BAM e 12 VVC da SR; 16 SPL originali patchati, più sostituzioni di grafica nativa |
| **10 — IWDEE** | 26 BAM e 26 VVC per 30 altre spell originali; duplicati grafici esclusi, varianti di colore distinte |

Puoi installarli insieme o separatamente. Non si importano icone, nuove spell,
meccaniche, proiettili, creature o armi. I dati non visivi delle spell restano
quelli installati nel tuo gioco. La lista completa e le 14 anteprime GIF sono
nel [README principale](README.md#animation-examples).

## Installazione

Estrai tutto nella cartella EET/BG2EE con `chitin.key`, avvia
`setup-sr_original_spell_animations.exe` e scegli Italiano. Installa i componenti
0 e/o 10 dopo **EET_end** e i mod che modificano gli incantesimi. Gli export
IWDEE/EET non vanno copiati nel gioco. Windows WeiDU 251 è incluso; su
Linux/macOS usa WeiDU nativo. Disinstalla con lo stesso installer.

## Cosa sapere

- `SPMAGGLO` è una grafica condivisa: cambia anche l'aspetto di spell/oggetti
  di altri mod che la usano. Lo stesso vale per i BAM nativi di Intralciare
  e Globo cromatico.
- Il componente IWD salta le abilità con una configurazione visiva diversa
  da quella riconosciuta e lo segnala. Quello SR sostituisce i visuali 141/215
  delle spell selezionate, conservando gli effetti non visivi.
- I nomi privati vengono controllati prima della copia: una collisione con
  un altro mod interrompe quel componente senza sovrascriverne le risorse.
- Le sequenze non ripetute possono finire; Barriera di lame, Mantello e
  Falsa alba conservano le rispettive regole di durata visiva.
- La beta.3 aveva aggiunto Sanctuary, Protection from Arrows e i due Globi IWDEE.
  Non si sovrappongono ai BAM SR o EET confrontati. Gli opcode di stato,
  le durate, condizioni e protezioni restano quelli della spell installata.
- La beta.4 recupera Glitterdust, Ragnatela sul bersaglio, Sfera elastica di
  Otiluke, Resurrezione, Guarigione e Rallentare veleno. Corregge le esclusioni
  basate sulla sola sagoma. Restano 45 candidati distinti ancora da integrare.
- La beta.5 aggiunge Miscast Magic (`MMAGICH`) e collega `CONFUSH`, già incluso,
  alle due Confusion e a Chaos. Per Chaos conserva entrambi i cue, con
  condizioni separate; durata e timing esistenti restano invariati.
- Non sono importati tutti i BAM IWDEE. Call Lightning richiede ancora i BAM
  `SKYBOLT` IWDEE ed EET per verifica; altri candidati dipendono da proiettili,
  aree e sottospell. [Esclusioni e ricontrollo](sr_original_spell_animations/docs/IWD_SELECTION_RECHECK.it.md).

## Ricontrollo

Verificati tutti i 40 BAM e 38 VVC. Passati i test WeiDU su 46 SPL EET reali (incluse due sottospell)
esportate: installazione, reinstallazione stabile e disinstallazione con
ripristino byte per byte. Passati anche 28 casi aggiuntivi di regressione e
i test dei layout SR e dei profili EET/BG2EE. Aggiunti e superati 54 test
specifici degli overlay persistenti, comprese le condizioni di Sanctuary.
Superati sei nuovi casi per i cue doppi di Chaos, incluse configurazioni
sconosciute che devono essere saltate. Superati anche 12 casi delle sottospell: si modificano solo se richiamate dalla
spell principale, conservando le condizioni e senza modificare la root.
[Rapporto completo IWDEE e SR](sr_original_spell_animations/docs/FULL_SOURCE_AUDIT.it.md).

Correzioni della beta.2: sequenza di Implosione non troncata, controller singoli
lasciati terminare, indice globale inutilizzato accettato quando non ci sono
effetti globali, avvisi per risorse IWD mancanti e protezione contro collisioni.
Le anteprime sono sequenze dei BAM, con blending illustrativo, non schermate
catturate dal gioco. **La resa nel gioco deve ancora essere verificata.**

[Ricontrollo rigoroso](sr_original_spell_animations/docs/RIGOROUS_AUDIT.md) ·
[Crediti e termini degli asset](CREDITS.md)
