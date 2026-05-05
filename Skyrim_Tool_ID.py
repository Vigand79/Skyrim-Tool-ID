import os, time, pyautogui, pyperclip, psutil
import tkinter as tk
from tkinter import messagebox, ttk
import sys

# Funzione per trovare il percorso corretto sia in script che in EXE
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SkyrimTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Skyrim Tool ID - by VIGAND")
        try:
            self.root.iconbitmap(get_path("logo.ico"))
        except:
            pass
        self.root.geometry("1000x800") 
        self.root.configure(bg='#0c0c0c')
        self.current_dir = os.getcwd()

        self.gold = "#c4a45d"
        self.bg_dark = "#0c0c0c"
        
        header = tk.Frame(root, bg=self.bg_dark)
        header.pack(fill='x', pady=(20, 10))
        tk.Label(header, text="SKYRIM TOOL ID", font=("Impact", 42), bg=self.bg_dark, fg=self.gold).pack()
        tk.Label(header, text="ULTIMATE DATABASE UTILITY BY VIGAND", font=("Segoe UI", 10, "bold"), bg=self.bg_dark, fg="#555").pack()

         # --- 1. PULSANTI SUPERIORI (SIMMETRICI) ---
        f_btns = tk.Frame(root, bg=self.bg_dark)
        # Usiamo padx=200 per lo stesso allineamento della griglia
        f_btns.pack(fill='x', padx=200, pady=20)
        f_btns.grid_columnconfigure(0, weight=1, uniform="top_btns")
        f_btns.grid_columnconfigure(1, weight=1, uniform="top_btns")

        self.btn_main(f_btns, "1. GENERA DATABASE", self.start_incolla).grid(row=0, column=0, padx=8, sticky="nsew")
        self.btn_main(f_btns, "2. PULISCI FILE", self.pulisci_temp).grid(row=0, column=1, padx=8, sticky="nsew")

        tk.Label(root, text="SELEZIONA UNA CATEGORIA", font=("Segoe UI", 11, "bold"), bg=self.bg_dark, fg="#888").pack(pady=(5, 5))
        
# --- GRIGLIA CATEGORIE (2 COLONNE PER SIMMETRIA TOTALE) ---
        cat_container = tk.Frame(root, bg=self.bg_dark)
        cat_container.pack(fill='x', padx=200, pady=10)
        # Forza le due colonne ad essere identiche
        cat_container.grid_columnconfigure(0, weight=1, uniform="group1")
        cat_container.grid_columnconfigure(1, weight=1, uniform="group1")

        self.cats = [
            ("PERSONAGGI", "NPC_"), ("ARMI", "WEAP"), ("ARMATURE", "ARMO"),
            ("POZIONI", "POTION"), ("INGREDIENTI", "INGR"), ("CIBO", "FOOD"),
            ("LIBRI", "BOOK"), ("OGGETTI VARI", "MISC"), ("INCANTESIMI", "SPEL"),
            ("CREATURE / MOSTRI", "MONS")
        ]

        # Configuriamo 2 colonne
        for i, (testo, filtro) in enumerate(self.cats):
            row, col = divmod(i, 2)
            btn = tk.Button(cat_container, text=testo, 
                            font=("Segoe UI", 10, "bold"), # Font leggermente ridotto
                            bg="#1a1a1a", fg=self.gold, 
                            activebackground=self.gold, activeforeground="#000", 
                            relief='flat', 
                            pady=10, # Altezza ridotta da 15 a 10
                            command=lambda f=filtro, t=testo: self.open_db(f, t))
            btn.grid(row=row, column=col, padx=8, pady=5, sticky="nsew")

# --- 3. PULSANTE CONSOLE (PERFETTAMENTE COINCIDENTE) ---
        console_frame = tk.Frame(root, bg=self.bg_dark)
        # Usiamo padx=210 e fill='x' per farlo largo quanto la griglia sopra
        console_frame.pack(fill='x', padx=210, pady=(20, 10))
        
        tk.Button(console_frame, text="💻 COMANDI CONSOLE", font=("Segoe UI", 11, "bold"), 
                  bg="#c44d4d", fg="#fff", relief='flat', pady=12,
                  command=self.open_console_cmds).pack(fill='both') # fill='both' lo adegua al frame

        self.status = tk.Label(root, text="SISTEMA PRONTO", bg=self.bg_dark, fg=self.gold, font=("Segoe UI", 10, "bold"))
        self.status.pack(side="bottom", pady=10)

    def btn_main(self, master, txt, cmd):
        return tk.Button(master, text=txt, font=("Segoe UI", 9, "bold"), bg=self.gold, fg="#000", 
                         relief='flat', padx=20, pady=8, command=cmd, activebackground="#fff")

    def open_console_cmds(self):
        win = tk.Toplevel(self.root); win.title("LISTA COMANDI CONSOLE"); win.geometry("1000x860"); win.configure(bg='#0a0a0a')
        top = tk.Frame(win, bg="#111", pady=10); top.pack(fill='x')
        tk.Label(top, text="CONSOLE COMMANDS DATABASE", font=("Impact", 24), bg="#111", fg=self.gold).pack()
        
        # --- DATABASE INTEGRALE COMANDI CONSOLE (140+ COMANDI BASE) ---
        console_data = [
            # --- SISTEMA, VISUALIZZAZIONE E DEBUG ---
            ("tgm", "God Mode: Salute, stamina, magicka e munizioni infinite"),
            ("tim", "Toggle Immortal Mode: Non muori mai, ma la salute scende"),
            ("tcl", "Toggle Collision: No-clip, vola attraverso gli oggetti"),
            ("tfc", "Toggle Free Camera: Telecamera libera"),
            ("tfc 1", "Free Camera + Pause: Blocca il tempo per screenshot"),
            ("tm", "Toggle Menus: Nasconde HUD e menu di gioco"),
            ("tmm 1", "Toggle Map Markers: Sblocca tutti i luoghi sulla mappa"),
            ("tai", "Toggle AI: Disattiva l'intelligenza artificiale globale"),
            ("tcai", "Toggle Combat AI: Disattiva l'intelligenza di combattimento"),
            ("tdetect", "Toggle Detection: Disattiva il rilevamento del furto/omicidio"),
            ("twf", "Toggle Wireframe: Visualizza i poligoni (mesh)"),
            ("tg", "Toggle Grass: Attiva/disattiva la generazione dell'erba"),
            ("tt", "Toggle Trees: Attiva/disattiva gli alberi"),
            ("ts", "Toggle Sky: Attiva/disattiva il cielo"),
            ("twp", "Toggle Water Pause: Blocca il movimento dell'acqua"),
            ("tll", "Toggle LOD: Disattiva i dettagli distanti"),
            ("teofis", "Toggle Fog of War: Disattiva effetti nebbia/luce pesanti"),
            ("sucsm [X]", "Speed Camera: Cambia velocità tfc (es: sucsm 10)"),
            ("fov [X]", "Field of View: Cambia angolo di visuale (default 75)"),
            ("showracemenu", "Race Menu: Riapre l'editor del personaggio"),
            ("qqq", "Quick Quit: Chiude il gioco immediatamente"),
            ("help [testo]", "Help: Cerca codici ID (es: help 'ebano' 4)"),
            ("clear", "Clear: Pulisce la cronologia dei comandi in console"),

            # --- GIOCATORE: ATTRIBUTI E LIVELLI ---
            ("player.advlevel", "Advance Level: Aumenta il livello di 1"),
            ("player.setlevel [X]", "Set Level: Imposta il livello a X"),
            ("player.setav health [X]", "Set Health: Imposta la salute massima"),
            ("player.setav magicka [X]", "Set Magicka: Imposta la magicka massima"),
            ("player.setav stamina [X]", "Set Stamina: Imposta il vigore massimo"),
            ("player.modav carryweight [X]", "Carry Weight: Aggiunge X al peso massimo"),
            ("player.setav speedmult [X]", "Speed: Velocità movimento (default 100)"),
            ("player.setav shoutrecoverymult 0", "No Shout Cooldown: Urli infiniti"),
            ("player.setav attackspeedmult [X]", "Attack Speed: Moltiplicatore velocità armi"),
            ("player.setav weaponskillmult [X]", "Weapon Skill: Danno armi fisiche"),
            ("player.setav leftweaponskillmult [X]", "Left Weapon Skill: Danno arma sinistra"),
            ("player.setav healrate [X]", "Heal Rate: Velocità rigenerazione vita"),
            ("player.setav staminarate [X]", "Stamina Rate: Velocità rigenerazione vigore"),
            ("player.setav magickarate [X]", "Magicka Rate: Velocità rigenerazione magia"),
            ("player.setav unarmeddamage [X]", "Unarmed: Danno a mani nude"),
            ("player.setav damage抵抗 [X]", "Resistenza: Imposta resistenza ai danni"),
            ("player.addperk [ID]", "Add Perk: Sblocca un talento specifico"),
            ("player.removeperk [ID]", "Remove Perk: Rimuove un talento"),
            ("player.addspell [ID]", "Add Spell: Impara una magia o urlo"),
            ("player.removespell [ID]", "Remove Spell: Dimentica una magia"),
            ("psb", "Player Spell Book: Sblocca TUTTI gli incantesimi e urli"),
            ("sexchange", "Sex Change: Cambia sesso al personaggio"),
            ("player.setcrimegold 0", "No Bounty: Rimuove la taglia sulla testa"),
            ("player.payfine", "Pay Fine: Paga la taglia e vieni teletrasportato"),

            # --- OGGETTI E INVENTARIO ---
            ("player.additem 0000000f [X]", "Add Gold: Aggiunge X monete d'oro"),
            ("player.additem 0000000a [X]", "Add Lockpicks: Aggiunge X grimaldelli"),
            ("player.showinventory", "Show Inventory: Elenca ID di tutto ciò che hai"),
            ("player.removeallitems", "Strip Player: Rimuove tutto l'inventario"),
            ("player.drop [ID] [X]", "Drop Item: Lascia cadere X unità di un oggetto"),
            ("player.equipitem [ID]", "Equip: Forza il PG a indossare un oggetto"),
            ("player.unequipitem [ID]", "Unequip: Forza il PG a togliere un oggetto"),
            ("player.additem [ID] [X]", "Add Item: Aggiunge X quantità dell'oggetto ID"),

            # --- NPC E BERSAGLI (DA SELEZIONARE CON MOUSE) ---
            ("kill", "Kill: Uccide l'NPC selezionato"),
            ("killall", "Kill All: Uccide tutti gli NPC nell'area"),
            ("resurrect", "Resurrect: Resuscita l'NPC morto selezionato"),
            ("resurrect 1", "Clean Resurrect: Resuscita e resetta l'inventario"),
            ("unlock", "Unlock: Apre porte o bauli selezionati"),
            ("lock [X]", "Lock: Chiude (X 0-100 definisce la difficoltà)"),
            ("disable", "Disable: Fa sparire l'oggetto o l'NPC selezionato"),
            ("enable", "Enable: Fa riapparire l'oggetto disabilitato"),
            ("markfordelete", "Delete: Elimina l'oggetto definitivamente al reload"),
            ("setscale [X]", "Set Scale: Cambia grandezza (default 1, max 10)"),
            ("getscale", "Get Scale: Mostra la grandezza dell'oggetto"),
            ("stopcombat", "Stop Combat: L'NPC smette di attaccarti"),
            ("setghost 1", "Ghost Mode: L'NPC diventa incorporeo/immortale"),
            ("inv", "Show Inventory NPC: Elenca gli oggetti dell'NPC"),
            ("removeallitems", "Strip NPC: Rimuove tutto dall'NPC selezionato"),
            ("openactorcontainer 1", "Open Inventory: Scambia oggetti con l'NPC"),
            ("setrelationshiprank player 4", "Friendship: Rende l'NPC un alleato"),
            ("addfac 0005c84d 1", "Add Follower: Rende l'NPC reclutabile"),
            ("addfac 00019809 1", "Marriage: Rende l'NPC sposabile"),
            ("resetai", "Reset AI: Ripristina la routine dell'NPC"),
            ("evp", "Update Packages: Forza l'NPC a ricalcolare cosa fare"),
            ("moveto player", "Move To Player: Teletrasporta l'NPC da te"),
            ("player.moveto [ID]", "Move To NPC: Teletrasporta te dall'NPC"),
            ("pushactoraway [ID] [X]", "Ragdoll: Scaraventa via l'NPC (forza X)"),

            # --- MISSIONI (QUEST) ---
            ("sqt", "Show Quest Targets: Elenca le quest attive"),
            ("sqo", "Show Quest Objectives: Elenca obiettivi quest"),
            ("saq", "Start All Quests: Avvia tutte le quest (rischioso!)"),
            ("caqs", "Complete All Quest Stages: Completa ogni missione"),
            ("getstage [ID]", "Get Stage: Mostra a che punto sei della quest"),
            ("setstage [ID] [X]", "Set Stage: Salta alla fase X della missione"),
            ("resetquest [ID]", "Reset Quest: Ricomincia la missione da capo"),
            ("completequest [ID]", "Complete Quest: Termina la missione"),
            ("movetoqt [ID]", "Move To Target: Teletrasporto all'obiettivo quest"),
            ("sqs [ID]", "Show Stages: Elenca tutte le fasi di una missione"),

            # --- MONDO E AMBIENTE ---
            ("set timescale to [X]", "Timescale: Velocità tempo (default 20, 1=reale)"),
            ("sw [ID]", "Set Weather: Cambia il meteo (ID cercabile con help)"),
            ("fw [ID]", "Force Weather: Forza il meteo istantaneamente"),
            ("setweather [ID] 1", "Lock Weather: Blocca il meteo scelto"),
            ("set gameday to [X]", "Set Day: Cambia il giorno del mese"),
            ("set gamemonth to [X]", "Set Month: Cambia il mese"),
            ("set gamehour to [X]", "Set Hour: Cambia l'ora (es: 22 per notte)"),

            # --- TELETRASPORTO (COC) ---
            ("coc qasmoke", "Testing Hall: La stanza con tutti gli oggetti"),
            ("coc whiterunorigin", "Whiterun: Ingresso principale"),
            ("coc whiterundragonsreach", "Whiterun: Palazzo dello Jarl"),
            ("coc riverwood", "Riverwood: Centro villaggio"),
            ("coc riftenorigin", "Riften: Ingresso principale"),
            ("coc solitudeorigin", "Solitude: Ingresso principale"),
            ("coc windhelmorigin", "Windhelm: Ingresso principale"),
            ("coc markarthorigin", "Markarth: Ingresso principale"),
            ("coc falkreathorigin", "Falkreath: Ingresso principale"),
            ("coc dawnstarorigin", "Dawnstar: Centro città"),
            ("coc morthalorigin", "Morthal: Centro città"),
            ("coc winterholdorigin", "Winterhold: Centro città"),
            ("coc rorikstead", "Rorikstead: Villaggio"),
            ("coc ivarstead", "Ivarstead: Villaggio"),
            ("coc highhrothgar", "High Hrothgar: I Barbagrigia"),
            ("coc darkness", "Area Segreta: Una stanza vuota e buia"),

            # --- FAZIONI E RELAZIONI ---
            ("player.addfac [ID] 1", "Join Faction: Entra in una fazione"),
            ("player.removefromallfactions", "Leave All Factions: Diventa neutrale"),
            ("setpve 1", "Vampire: Diventa Vampiro (stage 1)"),
            ("setpve 0", "Cure Vampire: Cura il vampirismo"),

            # --- COMANDI AVANZATI ---
            ("setpv [parametro] [valore]", "Set Variable: Modifica variabili interne script"),
            ("prid [RefID]", "Pick Reference: Seleziona NPC via ID (senza mouse)"),
            ("player.placeatme [ID] [X]", "Spawn NPC: Crea X copie di un NPC vicino a te"),
            ("showinventory", "Inspect NPC: Vedi tutto ciò che ha addosso l'NPC"),
            ("setscale [X]", "Resize: Cambia dimensioni agli oggetti selezionati"),
            ("getpos [x,y,z]", "Get Position: Mostra coordinate correnti"),
            ("setpos [x,y,z] [X]", "Set Position: Sposta l'oggetto alle coordinate X"),
            ("getangle [x,y,z]", "Get Angle: Mostra rotazione oggetto"),
            ("setangle [x,y,z] [X]", "Set Angle: Ruota l'oggetto"),
            ("bat [nomefile]", "Execute Batch: Esegue un file di comandi .txt"),
            ("outputlocalmap", "Export Map: Esporta la mappa locale in un file"),
            ("setpnpc [ID]", "Set Player NPC: Rendi il PG un NPC controllato"),
            ("player.setcrimegold 0 [IDfazione]", "Clear Bounty: Rimuove taglia di una fazione"),
            ("coc [ID]", "Center On Cell: Comando universale di teletrasporto"),
        ]

        self.c_page = 0
        self.c_size = 14 
        nav = tk.Frame(win, bg='#0a0a0a'); nav.pack(fill='x', padx=50, pady=10)
        cont = tk.Frame(win, bg='#0a0a0a'); cont.pack(fill='both', expand=True, padx=50)
        canv = tk.Canvas(cont, bg='#0a0a0a', highlightthickness=0); scr = tk.Scrollbar(cont, orient="vertical", command=canv.yview)
        scroll_f = tk.Frame(canv, bg='#0a0a0a')
        scroll_f.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv_win = canv.create_window((0, 0), window=scroll_f, anchor="nw")
        canv.bind('<Configure>', lambda e: canv.itemconfig(canv_win, width=e.width))
        canv.configure(yscrollcommand=scr.set); win.bind("<MouseWheel>", lambda e: canv.yview_scroll(int(-1*(e.delta/120)), "units"))
        canv.pack(side="left", fill="both", expand=True); scr.pack(side="right", fill="y")

        def draw_console():
            for w in scroll_f.winfo_children(): w.destroy()
            for w in nav.winfo_children(): w.destroy()
            tot = len(console_data); tp = (tot // self.c_size) + 1
            st, en = self.c_page * self.c_size, (self.c_page + 1) * self.c_size
            if tp > 1:
                tk.Button(nav, text="◀ PREV", bg="#333", fg="#fff", command=lambda: ch_c(-1, tp)).pack(side='left')
                tk.Label(nav, text=f"PAGINA {self.c_page + 1}/{tp} - {tot} COMANDI", bg="#0a0a0a", fg=self.gold, font=("Segoe UI", 9, "bold")).pack(side='left', expand=True)
                tk.Button(nav, text="NEXT ▶", bg="#333", fg="#fff", command=lambda: ch_c(1, tp)).pack(side='right')
            for cmd, desc in console_data[st:en]:
                r = tk.Frame(scroll_f, bg='#151515', pady=10); r.pack(fill='x', pady=2, padx=5)
                tk.Label(r, text=cmd, fg=self.gold, bg="#151515", width=36, font=("Consolas", 10, "bold"), anchor='w').pack(side='left', padx=15)
                tk.Label(r, text=desc, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w').pack(side='left', padx=10, fill='x', expand=True)
                tk.Button(r, text="COPIA", bg=self.gold, fg="#000", font=("Segoe UI", 8, "bold"), relief='flat', padx=15, command=lambda c=cmd: pyperclip.copy(c)).pack(side='right', padx=15)

        def ch_c(d, tp):
            if 0 <= self.c_page + d < tp:
                self.c_page += d; draw_console(); canv.yview_moveto(0)
        draw_console()

    def is_sseedit_running(self):
        return any("sseedit" in p.name().lower() for p in psutil.process_iter())

    def start_incolla(self):
        if not self.is_sseedit_running():
            messagebox.showerror("Errore", "SSEEdit non è aperto!")
            return
        
        path_fix = self.current_dir.replace("\\", "\\\\")
        
        pascal_script = f"""unit ExportVigand;

interface
  function Initialize: Integer;
  function Process(e: IInterface): Integer;
  function Finalize: Integer;

var
  f1, f2, f3, f4, f5, f6, f7, f8, f9, f10: TStringList;

implementation

function Initialize: Integer;
begin
  f1 := TStringList.Create; f2 := TStringList.Create; f3 := TStringList.Create;
  f4 := TStringList.Create; f5 := TStringList.Create; f6 := TStringList.Create;
  f7 := TStringList.Create; f8 := TStringList.Create; f9 := TStringList.Create;
  f10 := TStringList.Create;
  
  // Header per i file CSV
  f1.Add('REF,BASE,Nome'); f2.Add('ID,Nome'); f3.Add('ID,Nome');
  f4.Add('ID,Nome'); f5.Add('ID,Nome'); f6.Add('ID,Nome');
  f7.Add('ID,Nome'); f8.Add('ID,Nome'); f9.Add('ID,Nome');
  f10.Add('REF,BASE,Nome');
end;

function Process(e: IInterface): Integer;
var 
  s, n, id_ref, id_base, l: string; 
  base_rec: IInterface;
begin
  // Evita i duplicati: prende solo l'ultima versione caricata (winning override)
  if not IsWinningOverride(e) then Exit;

  s := Signature(e);
  
  // GESTIONE PERSONAGGI E CREATURE (RefID)
  if s = 'ACHR' then begin
    base_rec := BaseRecord(e);
    if not Assigned(base_rec) then Exit;
    
    // Recupero Nome (Fallback su EditorID se manca il nome completo)
    n := GetElementEditValues(base_rec, 'FULL');
    if n = '' then n := GetElementEditValues(base_rec, 'EDID');
    if (n = '') or (Length(n) < 2) then Exit;

    id_ref := IntToHex(FixedFormID(e), 8);
    id_base := IntToHex(FixedFormID(base_rec), 8);
    
    // Pulizia caratteri speciali per il CSV
    n := StringReplace(n, ',', ' ', [rfReplaceAll]);
    n := StringReplace(n, '"', '', [rfReplaceAll]);
    l := id_ref + ',' + id_base + ',' + Trim(n);
    
    // SEPARAZIONE: Se ha "Head Parts" è un Umano (f1), altrimenti è un Mostro (f10)
    if ElementExists(base_rec, 'Head Parts') then 
      f1.Add(l)
    else 
      f10.Add(l);
  end 
  
  // Ignoriamo i record base NPC_ per non avere cloni senza posizione nel mondo
  else if s = 'NPC_' then Exit 
  
  // GESTIONE TUTTI GLI ALTRI OGGETTI (BaseID)
  else begin
    n := GetElementEditValues(e, 'FULL');
    if (n = '') or (Length(n) < 2) then Exit;
    
    id_base := IntToHex(FixedFormID(e), 8);
    n := StringReplace(n, ',', ' ', [rfReplaceAll]);
    n := StringReplace(n, '"', '', [rfReplaceAll]);
    l := id_base + ',' + Trim(n);
    
    if s = 'WEAP' then f2.Add(l)
    else if s = 'ARMO' then f3.Add(l)
    else if s = 'INGR' then f5.Add(l)
    else if s = 'BOOK' then f7.Add(l)
    else if s = 'MISC' then f8.Add(l)
    else if s = 'SPEL' then f9.Add(l)
    else if s = 'ALCH' then begin
      if (Pos('PANE', UpperCase(n)) > 0) or (Pos('CARNE', UpperCase(n)) > 0) or (Pos('CIBO', UpperCase(n)) > 0) then f6.Add(l)
      else f4.Add(l);
    end;
  end;
end;

function Finalize: Integer;
var p: string;
begin
  p := '{path_fix}\\\\'; 
  f1.SaveToFile(p + 'db_NPC_.csv'); f2.SaveToFile(p + 'db_WEAP.csv');
  f3.SaveToFile(p + 'db_ARMO.csv'); f4.SaveToFile(p + 'db_POTION.csv');
  f5.SaveToFile(p + 'db_INGR.csv'); f6.SaveToFile(p + 'db_FOOD.csv');
  f7.SaveToFile(p + 'db_BOOK.csv'); f8.SaveToFile(p + 'db_MISC.csv');
  f9.SaveToFile(p + 'db_SPEL.csv'); f10.SaveToFile(p + 'db_MONS.csv');
  
  f1.Free; f2.Free; f3.Free; f4.Free; f5.Free; f6.Free; f7.Free; f8.Free; f9.Free; f10.Free;
  AddMessage('✅ DATABASE CREATI CON SUCCESSO!');
end;

end."""
        pyperclip.copy(pascal_script); self.countdown(10)

    def countdown(self, count):
        if count > 0:
            self.status.config(text=f"🔴 INCOLLO IN {count} SECONDI...", fg="#ff4444")
            self.root.after(1000, self.countdown, count-1)
        else:
            pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace'); pyautogui.hotkey('ctrl', 'v'); pyautogui.press('enter')
            self.status.config(text="✅ SCRIPT INCOLLATO", fg="#00ff00")

    def open_db(self, filtro, titolo):
        file_path = os.path.join(self.current_dir, f"db_{filtro}.csv")
        if not os.path.exists(file_path):
            messagebox.showerror("Errore", "Database mancante! Usa il tasto 1."); return
        data = []
        with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
            next(f)
            for line in f:
                split_n = 2 if filtro in ['NPC_', 'MONS'] else 1
                p = line.strip().split(',', split_n)
                if len(p) >= 2: data.append(p)

        win = tk.Toplevel(self.root); win.title(titolo); win.geometry("1100x850"); win.configure(bg='#0a0a0a')
        top = tk.Frame(win, bg="#111", pady=10); top.pack(fill='x')
        tk.Label(top, text=titolo, font=("Impact", 24), bg="#111", fg=self.gold).pack()
        s_var = tk.StringVar(); s_bar = tk.Entry(win, textvariable=s_var, bg='#1a1a1a', fg='#ccc', font=("Segoe UI", 14), relief='flat', highlightthickness=1, highlightbackground=self.gold, insertbackground='white')
        s_bar.insert(0, "Cerca Nome o ID..."); s_bar.pack(fill='x', padx=50, pady=20)
        s_bar.bind('<FocusIn>', lambda e: (s_bar.delete(0, "end"), s_bar.config(fg='white')) if s_bar.get() == "Cerca Nome o ID..." else None)

        nav = tk.Frame(win, bg='#0a0a0a'); nav.pack(fill='x', padx=50); self.current_page = 0; self.page_size = 50
        cont = tk.Frame(win, bg='#0a0a0a'); cont.pack(fill='both', expand=True, padx=50)
        canv = tk.Canvas(cont, bg='#0a0a0a', highlightthickness=0); scr = tk.Scrollbar(cont, orient="vertical", command=canv.yview)
        scroll_f = tk.Frame(canv, bg='#0a0a0a'); scroll_f.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv_win = canv.create_window((0, 0), window=scroll_f, anchor="nw")
        canv.bind('<Configure>', lambda e: canv.itemconfig(canv_win, width=e.width))
        canv.configure(yscrollcommand=scr.set); win.bind_all("<MouseWheel>", lambda e: canv.yview_scroll(int(-1*(e.delta/120)), "units"))
        canv.pack(side="left", fill="both", expand=True); scr.pack(side="right", fill="y")

        def copy_h(fid, mode):
            if mode == 'REF': cmd = f"prid {fid}; moveto player"
            elif mode == 'CLONE': cmd = f"player.placeatme {fid} 1"
            else: cmd = f"player.additem {fid} 1"
            pyperclip.copy(cmd); self.status.config(text="Comando copiato!")

        def draw():
            for w in scroll_f.winfo_children(): w.destroy()
            for w in nav.winfo_children(): w.destroy()
            q = s_var.get().upper()
            filt = [d for d in data if any(q in part.upper() for part in d)] if q and q != "CERCA NOME O ID..." else data
            tot = len(filt); tp = (tot // self.page_size) + 1
            if tot % self.page_size == 0 and tot > 0: tp -= 1
            st, en = self.current_page * self.page_size, (self.current_page + 1) * self.page_size
            if tp > 1:
                tk.Button(nav, text="◀ PREV", bg="#333", fg="#fff", command=lambda: ch(-1, tp)).pack(side='left')
                tk.Label(nav, text=f"PAGINA {self.current_page+1}/{tp} - TOTALE: {tot}", bg="#0a0a0a", fg=self.gold, font=("Segoe UI", 9, "bold")).pack(side='left', expand=True)
                tk.Button(nav, text="NEXT ▶", bg="#333", fg="#fff", command=lambda: ch(1, tp)).pack(side='right')
            for row_data in filt[st:en]:
                r = tk.Frame(scroll_f, bg='#151515', pady=5); r.pack(fill='x', pady=1, padx=5)
                if filtro in ['NPC_', 'MONS']:
                    ref_id, base_id, r_nome = row_data[0], row_data[1], row_data[2]
                    tk.Label(r, text=f"REF: {ref_id}", fg=self.gold, bg="#151515", width=15, font=("Consolas", 10, "bold")).pack(side='left')
                    tk.Label(r, text=f"BASE: {base_id}", fg="#888", bg="#151515", width=15, font=("Consolas", 10)).pack(side='left')
                    tk.Label(r, text=r_nome, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w').pack(side='left', padx=10, fill='x', expand=True)
                    if ref_id != '-':
                        tk.Button(r, text="TELEPORT", bg="#296729", fg="#fff", font=("Segoe UI", 8, "bold"), relief='flat', width=10, command=lambda i=ref_id: copy_h(i, 'REF')).pack(side='right', padx=5)
                    tk.Button(r, text="CLONE", bg="#8b1f1f", fg="#fff", font=("Segoe UI", 8, "bold"), relief='flat', width=10, command=lambda i=base_id: copy_h(i, 'CLONE')).pack(side='right', padx=5)
                else:
                    r_id, r_nome = row_data[0], row_data[1]
                    tk.Label(r, text=r_id, fg="#888", bg="#151515", width=12, font=("Consolas", 10)).pack(side='left')
                    tk.Label(r, text=r_nome, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w').pack(side='left', padx=20, fill='x', expand=True)
                    tk.Button(r, text="COPIA", bg=self.gold, font=("Segoe UI", 8, "bold"), relief='flat', command=lambda i=r_id: copy_h(i, 'STD')).pack(side='right', padx=10)

        def ch(d, tp):
            if 0 <= self.current_page + d < tp: self.current_page += d; draw(); canv.yview_moveto(0)

        self.after_id = None
        def reset_and_draw(*args):
            if self.after_id: win.after_cancel(self.after_id)
            self.after_id = win.after(2000, lambda: [setattr(self, 'current_page', 0), draw()])
        s_var.trace_add("write", reset_and_draw); draw()

    def pulisci_temp(self):
        for f in os.listdir(self.current_dir):
            if f.startswith("db_") and f.endswith(".csv"): os.remove(f)
        messagebox.showinfo("VIGAND", "PULIZIA OK!")

if __name__ == "__main__":
    root = tk.Tk(); app = SkyrimTool(root); root.mainloop()