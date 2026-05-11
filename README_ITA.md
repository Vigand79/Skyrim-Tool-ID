# 🐉 Skyrim Tool ID (v1.1)
**L'Utility Definitiva per Database ID e Comandi Console (Skyrim SE & AE)**

👤 **Autore:** [VIGAND](https://github.com) | 🎮 **Gioco:** [Skyrim Special Edition / Anniversary Edition](https://nexusmods.com)

---

## 🚀 Cos'è Skyrim Tool ID?
**Skyrim Tool ID** non è una semplice lista statica. È un'applicazione intelligente che scansiona in tempo reale il **TUO specifico ordine di caricamento**. 

Le liste online spesso forniscono ID che non funzionano a causa dei plugin attivi. Questo tool estrae i dati direttamente dai tuoi file di gioco tramite **SSEEdit**, garantendo che ogni ID (incluse le armi, le magie e gli NPC delle mod) sia **funzionante al 100%** nella tua partita attuale.

---

## ✨ Novità della Versione 1.1

*   **📦 Sistema Batch Universale:** Basta errori di copia-incolla! Il tool genera automaticamente un file `toolid.txt` nella cartella di gioco. In console dovrai solo scrivere `bat toolid` per eseguire azioni complesse all'istante.
*   **🖱️ Menu Azioni NPC:** Un nuovo menu a tendina per ogni personaggio o creatura:
    *   **Vieni da me / Vai da lui:** Teletrasporto sicuro e immediato.
    *   **Uccidi / Resuscita / Abilita:** Gestione completa dello stato degli NPC.
    *   **Clona:** Crea una copia perfetta (BaseID) dell'NPC.
*   **🌍 Localizzazione Universale:** Il tool trova automaticamente Skyrim (Steam, GOG, Epic) o permette la selezione manuale, salvando il percorso per i futuri utilizzi.
*   **🇮🇹 Razze in Italiano:** Grazie a un nuovo algoritmo, le razze appaiono tradotte (es: [Nord], [Imperiale], [Orco]) e i nomi sono puliti da codici tecnici fastidiosi.
*   **📜 Gestione Script .PAS Professionale:** Il tool scrive fisicamente il file `ExportToolID.pas` nella cartella di SSEEdit. Niente più codici da incollare a mano.
*   **⚡ Quantità Intelligenti:** Il tool capisce cosa stai copiando: 1 unità per armi e armature, 10 unità per frecce, pozioni, ingredienti e cibo.

---

## 🛠️ Istruzioni per l'uso

### 1. Generazione del Database
1. Avvia il tool e clicca su **"1. GENERA DATABASE"**.
2. Seleziona la cartella dove hai installato **SSEEdit.exe** quando richiesto.
3. Apri SSEEdit, seleziona tutti i tuoi plugin -> Tasto Destro -> **Apply Script**.
4. Cerca e seleziona lo script **ExportToolID** e premi OK.
5. Una volta terminato, chiudi SSEEdit: il tuo database personalizzato è pronto!

### 2. Utilizzo in Gioco
*   **Oggetti:** Cerca l'oggetto, clicca su **COPIA** e usa `CTRL+V` nella console di Skyrim.
*   **NPC/Creature:** Scegli l'azione dal menu a tendina, clicca su **APPLICA** e nella console di Skyrim usa `CTRL+V` o scrivi semplicemente: `bat toolid`.

---

## 🛡️ Nota sulla Sicurezza
Il tool è **Open Source** e il codice sorgente è verificabile in questo repository. 
L'eseguibile è compilato con **PyInstaller**. Alcuni antivirus potrebbero segnalare un "Falso Positivo" a causa della libreria `pyautogui` (che simula l'automazione della tastiera). Il software è sicuro, pulito e creato esclusivamente per il modding di Skyrim.

---

## 👨‍💻 Sviluppatore
Creato con passione da **VIGAND**. Se il tool ti piace, lascia un **Endorse** su Nexus Mods!