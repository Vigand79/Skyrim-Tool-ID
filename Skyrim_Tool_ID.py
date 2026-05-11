import os, time, pyautogui, pyperclip, psutil, sys, winreg, json
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

def get_path(relative_path):
    try:
        # Percorso per l'eseguibile compilato
        base_path = sys._MEIPASS
    except Exception:
        # Percorso per lo script Python normale
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SkyrimTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Skyrim Tool ID - by VIGAND")
        try:
            self.root.iconbitmap(get_path("logo.ico"))
        except: pass
        self.root.geometry("1000x800") 
        self.root.configure(bg='#0c0c0c')
        # Rileva la cartella reale dove si trova lo script o l'eseguibile
        if getattr(sys, 'frozen', False):
            # Se è un EXE compilato
            self.current_dir = os.path.dirname(sys.executable)
        else:
            # Se è lo script .py in esecuzione
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gold = "#c4a45d"
        self.bg_dark = "#0c0c0c"
        
        header = tk.Frame(root, bg=self.bg_dark)
        header.pack(fill='x', pady=(20, 10))
        tk.Label(header, text="SKYRIM TOOL ID", font=("Impact", 42), bg=self.bg_dark, fg=self.gold).pack()
        tk.Label(header, text="ULTIMATE DATABASE UTILITY BY VIGAND", font=("Segoe UI", 10, "bold"), bg=self.bg_dark, fg="#555").pack()

        f_btns = tk.Frame(root, bg=self.bg_dark)
        f_btns.pack(fill='x', padx=200, pady=20)
        f_btns.grid_columnconfigure(0, weight=1, uniform="top_btns")
        f_btns.grid_columnconfigure(1, weight=1, uniform="top_btns")
        self.btn_main(f_btns, "1. GENERA DATABASE", self.start_incolla).grid(row=0, column=0, padx=8, sticky="nsew")
        self.btn_main(f_btns, "2. PULISCI FILE", self.pulisci_temp).grid(row=0, column=1, padx=8, sticky="nsew")

        tk.Label(root, text="SELEZIONA UNA CATEGORIA", font=("Segoe UI", 11, "bold"), bg=self.bg_dark, fg="#888").pack(pady=(10, 5))
        
        cat_container = tk.Frame(root, bg=self.bg_dark)
        cat_container.pack(fill='x', padx=200, pady=10)
        cat_container.grid_columnconfigure(0, weight=1, uniform="group1")
        cat_container.grid_columnconfigure(1, weight=1, uniform="group1")

        self.cats = [("PERSONAGGI", "NPC_"), ("ARMI", "WEAP"), ("ARMATURE", "ARMO"), ("POZIONI", "POTION"), ("INGREDIENTI", "INGR"), ("CIBO", "FOOD"), ("LIBRI", "BOOK"), ("OGGETTI VARI", "MISC"), ("INCANTESIMI", "SPEL"), ("CREATURE / MOSTRI", "MONS")]
        for i, (testo, filtro) in enumerate(self.cats):
            row, col = divmod(i, 2)
            btn = tk.Button(cat_container, text=testo, font=("Segoe UI", 10, "bold"), bg="#1a1a1a", fg=self.gold, activebackground=self.gold, activeforeground="#000", relief='flat', cursor="hand2", pady=10, command=lambda f=filtro, t=testo: self.open_db(f, t))
            btn.grid(row=row, column=col, padx=8, pady=5, sticky="nsew")

        console_frame = tk.Frame(root, bg=self.bg_dark)
        console_frame.pack(fill='x', padx=210, pady=(20, 10))
        tk.Button(console_frame, text="💻 COMANDI CONSOLE", font=("Segoe UI", 11, "bold"), bg="#c44d4d", fg="#fff", relief='flat', cursor="hand2", pady=12, command=self.open_console_cmds).pack(fill='both')
        self.status = tk.Label(root, text="SISTEMA PRONTO", bg=self.bg_dark, fg=self.gold, font=("Segoe UI", 10, "bold"))
        self.status.pack(side="bottom", pady=10)

    def get_skyrim_path(self):
        conf_path = os.path.join(self.current_dir, "tool_config.json")
        
        # 1. Carica il percorso dal file JSON se esiste
        if os.path.exists(conf_path):
            try:
                with open(conf_path, "r") as f:
                    data = json.load(f)
                    p = data.get("sky_p")
                    if p and os.path.exists(p):
                        return str(p)
            except: pass

        # 2. Cerca automaticamente (Processi o Registro)
        found = None
        for p in psutil.process_iter(['name', 'exe']):
            try:
                if p.info['name'] and p.info['name'].lower() in ["skyrimse.exe", "skyrim.exe"]:
                    found = os.path.dirname(p.info['exe'])
                    break
            except: continue
        
        if not found:
            reg_keys = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 489830", 
                        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 489830"]
            for rk in reg_keys:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rk) as k:
                        found, _ = winreg.QueryValueEx(k, "InstallLocation")
                        if found: break
                except: continue

        # 3. Se non trovato o non valido, CHIEDI MANUALMENTE
        if not found or not os.path.exists(found):
            messagebox.showinfo("Configurazione", "Seleziona la cartella principale di Skyrim (dove c'è SkyrimSE.exe)")
            found = filedialog.askdirectory(title="Seleziona cartella di Skyrim")
            
        # 4. Se l'utente ha scelto qualcosa, SALVA e RITORNA
        if found:
            self.save_config(found, "sky_p")
            return str(found)
        
        # Fallback estremo: cartella del tool
        return str(self.current_dir)

    def get_sseedit_path(self):
        conf = os.path.join(self.current_dir, "tool_config.json")
        if os.path.exists(conf):
            try:
                with open(conf, "r") as f:
                    path = json.load(f).get("sseedit_p")
                    if path: return path
            except: pass

        messagebox.showinfo("Configurazione", "Seleziona la cartella dove è installato SSEEdit.exe")
        path = filedialog.askdirectory()
        if path:
            current_conf = {}
            if os.path.exists(conf):
                try:
                    with open(conf, "r") as f: current_conf = json.load(f)
                except: pass
            current_conf["sseedit_p"] = path
            with open(conf, "w") as f: json.dump(current_conf, f)
            return path
        return None

    def save_config(self, new_path, key):
        conf_p = os.path.join(self.current_dir, "tool_config.json")
        existing_data = {}
        
        # Legge il file esistente per non perdere le altre chiavi (es. sse_p)
        if os.path.exists(conf_p):
            try:
                with open(conf_p, "r") as f:
                    existing_data = json.load(f)
            except: pass
            
        existing_data[key] = new_path
        
        # Scrive il file aggiornato
        try:
            with open(conf_p, "w") as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            print(f"Errore salvataggio config: {e}")

    def copy_console(self, cmd, label):
        pyperclip.copy(cmd)
        label.config(text=f"✅ COPIATO: {cmd}", fg=self.gold)
        label.after(2000, lambda: label.config(text="SELEZIONA UN COMANDO", fg="#555"))

    def copy_h(self, fid, mode, nome_oggetto, target_label=None):
        fid = str(fid).strip()
        # Ottieni il percorso e assicurati che sia una stringa valida
        sky_p = self.get_skyrim_path()
        if not sky_p:
            sky_p = str(self.current_dir)

        file_p = os.path.join(sky_p, "toolid.txt")
        cmds = []
        
        # Quantità intelligente
        q = 10 if (mode in ['POTION', 'INGR', 'FOOD'] or "[MUNIZIONI]" in str(nome_oggetto).upper()) else 1
        
        if mode == 'DA_TE': cmds = [f"prid {fid}", "moveto player", "enable"]
        elif mode == 'VAI': cmds = [f"player.moveto {fid}"]
        elif mode == 'KILL': cmds = [f"prid {fid}", "kill"]
        elif mode == 'RES': cmds = [f"prid {fid}", "resurrect 1", "enable"]
        elif mode == 'ENABLE': cmds = [f"prid {fid}", "enable"]
        elif mode == 'CLONE': cmds = [f"player.placeatme {fid} 1"]
        else: cmds = [f"player.additem {fid} {q}"]

        try:
            label = target_label if target_label else self.status
            if mode not in ['NPC_', 'MONS', 'DA_TE', 'VAI', 'KILL', 'RES', 'ENABLE', 'CLONE']:
                pyperclip.copy(cmds)
                msg = f"✅ {q}x {fid} COPIATO!"
            else:
                with open(file_p, "w") as f:
                    f.write("\n".join(cmds))
                pyperclip.copy("bat toolid")
                msg = f"✅ BATCH PRONTO: bat toolid, fai Ctrl + v nella console di Skyrim"
            
            label.config(text=msg, fg=self.gold)
            label.after(4000, lambda: label.config(text="PRONTO", fg="#555"))
        except Exception as e:
            pyperclip.copy(fid)
            if label:
                label.config(text="⚠️ ERRORE SCRITTURA FILE!", fg="orange")

    def btn_main(self, master, txt, cmd):
        return tk.Button(master, text=txt, font=("Segoe UI", 9, "bold"), bg=self.gold, fg="#000", relief='flat', padx=20, pady=8, cursor="hand2", command=cmd)

    def is_sseedit_running(self):
        return any("sseedit" in p.name().lower() for p in psutil.process_iter())

    def start_incolla(self):
        # 1. Recupera il percorso di SSEEdit
        sse_path = self.get_sseedit_path()
        if not sse_path:
            return

        # 2. Verifica/Crea la cartella Edit Scripts
        script_dir = os.path.join(sse_path, "Edit Scripts")
        if not os.path.exists(script_dir):
            try:
                os.makedirs(script_dir)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile creare la cartella Edit Scripts: {e}")
                return

        file_pas = os.path.join(script_dir, "ExportToolID.pas")
        # Prepariamo il percorso del tool per il Pascal (doppio backslash per compatibilità)
        path_fix = self.current_dir.replace("\\", "\\\\")

        # 3. Lo Script Pascal Integrale con tutti i tuoi filtri (Razza, Cibo, Anti-Junk)
        pascal_code = f"""unit ExportToolID;

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
  
  f1.Add('REF,BASE,Nome'); f10.Add('REF,BASE,Nome');
  f2.Add('ID,Nome'); f3.Add('ID,Nome'); f4.Add('ID,Nome');
  f5.Add('ID,Nome'); f6.Add('ID,Nome'); f7.Add('ID,Nome');
  f8.Add('ID,Nome'); f9.Add('ID,Nome');
end;

function Process(e: IInterface): Integer;
var 
  s, n, id_ref, id_base, l, race: string; 
  base_rec, race_rec: IInterface;
  isUmano: Boolean;
begin
  if not IsWinningOverride(e) then Exit;
  s := Signature(e);
  
  if s = 'ACHR' then begin
    base_rec := BaseRecord(e);
    if not Assigned(base_rec) then Exit;
    if Signature(base_rec) <> 'NPC_' then Exit;

    race_rec := LinksTo(ElementByPath(base_rec, 'RNAM - Race'));
    if Assigned(race_rec) then
      race := GetElementEditValues(race_rec, 'FULL')
    else
      race := GetElementEditValues(base_rec, 'RNAM - Race');

    if (Pos('Default', race) > 0) or (race = '') or (Pos('Marker', race) > 0) then Exit;
    if Pos(' [', race) > 0 then race := Copy(race, 1, Pos(' [', race) - 1);

    race := StringReplace(race, 'NordRace', 'Nord', [rfReplaceAll]);
    race := StringReplace(race, 'Imperial', 'Imperiale', [rfReplaceAll]);
    race := StringReplace(race, 'Breton', 'Bretone', [rfReplaceAll]);
    race := StringReplace(race, 'Wood Elf', 'Bosmer', [rfReplaceAll]);
    race := StringReplace(race, 'Dark Elf', 'Dunmer', [rfReplaceAll]);
    race := StringReplace(race, 'High Elf', 'Altmer', [rfReplaceAll]);
    race := StringReplace(race, 'Orc', 'Orco', [rfReplaceAll]);
    race := StringReplace(race, 'Argonian', 'Argoniano', [rfReplaceAll]);

    n := GetElementEditValues(base_rec, 'FULL');
    if n = '' then n := GetElementEditValues(base_rec, 'EDID');

    if (n = '') or (Length(n) < 3) or 
       (Pos('Corpse', n) > 0) or (Pos('Treas', n) > 0) or 
       (Pos('Lvl', n) = 1) or (Pos('dun', n) = 1) or 
       (Pos('Vaso', n) > 0) or (Pos('Mannequin', n) > 0) or 
       (Pos('Statua', n) > 0) or (Pos('Marker', n) > 0) or 
       (Pos('Trigger', n) > 0) or (Pos('FX', n) > 0) then Exit;

    id_ref := IntToHex(FixedFormID(e), 8);
    id_base := IntToHex(FixedFormID(base_rec), 8);
    n := StringReplace(n, ',', ' ', [rfReplaceAll]);
    n := StringReplace(n, '"', '', [rfReplaceAll]);
    
    isUmano := False;
    if ElementExists(base_rec, 'Head Parts') then isUmano := True;
    if (Pos('Nord', race) > 0) or (Pos('Bretone', race) > 0) or 
       (Pos('Imperiale', race) > 0) or (Pos('Orco', race) > 0) or
       (Pos('Dunmer', race) > 0) or (Pos('Altmer', race) > 0) or
       (Pos('Bosmer', race) > 0) or (Pos('Argoniano', race) > 0) or
       (Pos('Guard', n) > 0) or (Pos('Guardia', n) > 0) then isUmano := True;

    l := id_ref + ',' + id_base + ',' + Trim(n) + ' [' + Trim(race) + ']';
    if isUmano then f1.Add(l) else f10.Add(l);
  end 
  else if s = 'NPC_' then Exit 
  else begin
    n := GetElementEditValues(e, 'FULL');
    if (n = '') or (Length(n) < 2) then Exit;
    id_base := IntToHex(FixedFormID(e), 8);
    n := StringReplace(n, ',', ' ', [rfReplaceAll]);
    n := StringReplace(n, '"', '', [rfReplaceAll]);
    l := id_base + ',' + Trim(n);
    
    if s = 'WEAP' then f2.Add(l)
    else if s = 'AMMO' then f2.Add(id_base + ',[MUNIZIONI] ' + Trim(n))
    else if s = 'ARMO' then f3.Add(l)
    else if s = 'INGR' then f5.Add(l)
    else if s = 'BOOK' then f7.Add(l)
    else if s = 'MISC' then f8.Add(l)
    else if s = 'SPEL' then f9.Add(l)
    else if s = 'ALCH' then begin
      if (Pos('PANE', UpperCase(n)) > 0) or (Pos('CARNE', UpperCase(n)) > 0) or
         (Pos('COTTO', UpperCase(n)) > 0) or (Pos('COTTA', UpperCase(n)) > 0) or 
         (Pos('COTTE', UpperCase(n)) > 0) or (Pos('COTTI', UpperCase(n)) > 0) or
         (Pos('CRUDE', UpperCase(n)) > 0) or (Pos('CRUDO', UpperCase(n)) > 0) or 
         (Pos('CRUDA', UpperCase(n)) > 0) or (Pos('PASTO', UpperCase(n)) > 0) or 
         (Pos('IMPASTO', UpperCase(n)) > 0) or (Pos('PASTICCI', UpperCase(n)) > 0) or 
         (Pos('SUCCO', UpperCase(n)) > 0) or (Pos('CUCINATE', UpperCase(n)) > 0) or 
         (Pos('CUCINATO', UpperCase(n)) > 0) or (Pos('PESCE', UpperCase(n)) > 0) or 
         (Pos('IDROMELE', UpperCase(n)) > 0) or (Pos('SKOOMA', UpperCase(n)) > 0) or 
         (Pos('DOLCE', UpperCase(n)) > 0) or (Pos('CIBO', UpperCase(n)) > 0) or 
         (Pos('ZUPPA', UpperCase(n)) > 0) or (Pos('MELA', UpperCase(n)) > 0) or 
         (Pos('FORMAGGIO', UpperCase(n)) > 0) or (Pos('SALE', UpperCase(n)) > 0) or 
         (Pos('CARAFFA', UpperCase(n)) > 0) or (Pos('STUFATO', UpperCase(n)) > 0) or 
         (Pos('PORRIDGE', UpperCase(n)) > 0) or (Pos('CREMA', UpperCase(n)) > 0) or 
         (Pos('MARINATA', UpperCase(n)) > 0) or (Pos('STUFATE', UpperCase(n)) > 0) or 
         (Pos('RAGU', UpperCase(n)) > 0) or (Pos('FONDUTA', UpperCase(n)) > 0) or 
         (Pos('VINO', UpperCase(n)) > 0) or (Pos('BIRRA', UpperCase(n)) > 0) or
         (Pos('UOVA', UpperCase(n)) > 0) or (Pos('CAROTA', UpperCase(n)) > 0) or
         (Pos('PATATA', UpperCase(n)) > 0) or (Pos('PORRO', UpperCase(n)) > 0) or
         (Pos('TORTA', UpperCase(n)) > 0) or (Pos('LATTE', UpperCase(n)) > 0) or
         (Pos('BRANDY', UpperCase(n)) > 0) or (Pos('UMIDO', UpperCase(n)) > 0) or
         (Pos('ARROSTITO', UpperCase(n)) > 0) or (Pos('GRIGLIATO', UpperCase(n)) > 0) or
         (Pos('MARMELLATA', UpperCase(n)) > 0) or (Pos('TÈ', UpperCase(n)) > 0) or
         (Pos('TE ', UpperCase(n)) > 0) or (Pos('SALSICCIA', UpperCase(n)) > 0) or
         (Pos('PANCETTA', UpperCase(n)) > 0) or (Pos('SIDRO', UpperCase(n)) > 0) or
         (Pos('SUJAMMA', UpperCase(n)) > 0) or (Pos('MAZTE', UpperCase(n)) > 0) or
         (Pos('SHEIN', UpperCase(n)) > 0) or (Pos('FLIN', UpperCase(n)) > 0) or
         (Pos('BURRO', UpperCase(n)) > 0) or (Pos('FARINA', UpperCase(n)) > 0) or
         (Pos('VINSANGUE', UpperCase(n)) > 0) or (Pos('RAPA', UpperCase(n)) > 0) or
         (Pos('CAVOLO', UpperCase(n)) > 0) or (Pos('PISELLI', UpperCase(n)) > 0) or
         (Pos('MIRTILLI', UpperCase(n)) > 0) or (Pos('ZUCCA', UpperCase(n)) > 0) or
         (Pos('CIPOLLA', UpperCase(n)) > 0) or (Pos('BRODO', UpperCase(n)) > 0) or
         (Pos('ACETO', UpperCase(n)) > 0) or (Pos('OLIO', UpperCase(n)) > 0) or
         (Pos('ZUCCHERO', UpperCase(n)) > 0) or (Pos('CONDIMENTO', UpperCase(n)) > 0) or
         (Pos('ZUCCHINA', UpperCase(n)) > 0) or (Pos('MIELE', UpperCase(n)) > 0) or
         (Pos('RUM', UpperCase(n)) > 0) or (Pos('SALMONE', UpperCase(n)) > 0) or
         (Pos('MERLUZZO', UpperCase(n)) > 0) or (Pos('BRANZINO', UpperCase(n)) > 0) or
         (Pos('CARPA', UpperCase(n)) > 0) or (Pos('CALDO', UpperCase(n)) > 0) or
         (Pos('CALDA', UpperCase(n)) > 0) or (Pos('FAME', UpperCase(n)) > 0) or
         (Pos('FATICA', UpperCase(n)) > 0) or (Pos('MARINATO', UpperCase(n)) > 0) or
         (Pos('BISTECCA', UpperCase(n)) > 0) or (Pos('SALATO', UpperCase(n)) > 0) or
         (Pos('INVOLTINO', UpperCase(n)) > 0) or (Pos('MORA TAPINELLA', UpperCase(n)) > 0) or
         (Pos('RANA PESCATRICE', UpperCase(n)) > 0) or (Pos('ESTRATTO', UpperCase(n)) > 0) then f6.Add(l) 
      else 
        f4.Add(l); // Qui finiscono Nettare, Welkynd, Veleni e oggetti di mod
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
  AddMessage('DATABASE CREATI CON SUCCESSO!');
end;
end."""

        # 4. Scrittura fisica del file
        try:
            with open(file_pas, "w", encoding="utf-8") as f:
                f.write(pascal_code)
            
            messagebox.showinfo("VIGAND", f"Script 'ExportToolID.pas' generato con successo!\n\nLo trovi in: {script_dir}\n\nISTRUZIONI:\n1. Apri SSEEdit\n2. Seleziona tutte le mod\n3. Tasto Destro -> Apply Script\n4. Seleziona 'ExportToolID'")
            self.status.config(text="✅ SCRIPT PRONTO IN SSEEDIT", fg=self.gold)
            self.root.after(3000, lambda: self.status.config(text="SISTEMA PRONTO", fg=self.gold))
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile creare il file Pascal: {e}")

    def pulisci_temp(self):
        file_cancellati = 0
        file_config = os.path.join(self.current_dir, "tool_config.json")
        
        # Lista dei file da cercare nella cartella del tool
        for nome_file in os.listdir(self.current_dir):
            # Cancella i database CSV e il file di configurazione
            if (nome_file.startswith("db_") and nome_file.endswith(".csv")) or nome_file == "tool_config.json":
                percorso_completo = os.path.join(self.current_dir, nome_file)
                try:
                    os.remove(percorso_completo)
                    file_cancellati += 1
                except Exception as e:
                    print(f"Impossibile cancellare {nome_file}: {e}")

        if file_cancellati > 0:
            messagebox.showinfo("VIGAND", f"PULIZIA COMPLETATA!\nRimossi {file_cancellati} file.\n\nAl prossimo avvio dovrai riconfigurare i percorsi.")
        else:
            messagebox.showinfo("VIGAND", "Nessun file trovato da pulire.")
    def open_db(self, filtro, titolo):
        file_path = os.path.join(self.current_dir, f"db_{filtro}.csv")
        if not os.path.exists(file_path):
            messagebox.showerror("Errore", "Database mancante! Usa il tasto 1."); return
        
        raw_data = []
        with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
            next(f)
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2: raw_data.append(parts)

        visti = set(); data = []
        for p in raw_data:
            nome_chiave = p[-1].upper().strip()
            if nome_chiave not in visti: data.append(p); visti.add(nome_chiave)

        win = tk.Toplevel(self.root); win.title(titolo); win.geometry("1200x900"); win.configure(bg='#0a0a0a')
        tk.Label(win, text=titolo, font=("Impact", 32), bg="#0a0a0a", fg=self.gold, pady=10).pack()

        # LABEL DI STATO LOCALE (In fondo)
        local_status = tk.Label(win, text="PRONTO", bg="#0a0a0a", fg="#555", font=("Segoe UI", 10, "bold"))
        local_status.pack(side="bottom", pady=5)

        s_var = tk.StringVar(); s_bar = tk.Entry(win, textvariable=s_var, bg='#1a1a1a', fg='#ccc', font=("Segoe UI", 14), relief='flat', highlightthickness=1, highlightbackground=self.gold, insertbackground='white')
        s_bar.insert(0, "Cerca Nome o ID..."); s_bar.pack(fill='x', padx=50, pady=20)
        s_bar.bind('<FocusIn>', lambda e: (s_bar.delete(0, "end"), s_bar.config(fg='white')) if s_bar.get() == "Cerca Nome o ID..." else None)

        nav = tk.Frame(win, bg='#0a0a0a'); nav.pack(fill='x', padx=50)
        self.current_page = 0; self.page_size = 50
        cont = tk.Frame(win, bg='#0a0a0a'); cont.pack(fill='both', expand=True, padx=20)
        canv = tk.Canvas(cont, bg='#0a0a0a', highlightthickness=0); scr = tk.Scrollbar(cont, orient="vertical", command=canv.yview)
        scroll_f = tk.Frame(canv, bg='#0a0a0a')
        scroll_f.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv_win = canv.create_window((0, 0), window=scroll_f, anchor="nw")
        canv.bind('<Configure>', lambda e: canv.itemconfig(canv_win, width=e.width))
        canv.configure(yscrollcommand=scr.set); win.bind_all("<MouseWheel>", lambda e: canv.yview_scroll(int(-1*(e.delta/120)), "units"))
        canv.pack(side="left", fill="both", expand=True); scr.pack(side="right", fill="y")

        def draw():
            for w in scroll_f.winfo_children(): w.destroy()
            for w in nav.winfo_children(): w.destroy()
            q = s_var.get().upper().strip()
            filt = [d for d in data if any(q in str(p).upper() for p in d)] if q and q != "CERCA NOME O ID..." else data
            tot_i = len(filt); tp = (tot_i // self.page_size) + 1
            if tot_i % self.page_size == 0 and tot_i > 0: tp -= 1
            st, en = self.current_page * self.page_size, (self.current_page + 1) * self.page_size

            if tp > 1:
                tk.Button(nav, text="◀ PREV", bg="#333", fg="#fff", relief='flat', cursor="hand2", command=lambda: ch(-1, tp)).pack(side='left')
                tk.Label(nav, text=f"PAGINA {self.current_page+1}/{tp} - TOTALE: {tot_i}", bg="#0a0a0a", fg=self.gold, font=("Segoe UI", 10, "bold")).pack(side='left', expand=True)
                tk.Button(nav, text="NEXT ▶", bg="#333", fg="#fff", relief='flat', cursor="hand2", command=lambda: ch(1, tp)).pack(side='right')

            for row_data in filt[st:en]:
                r = tk.Frame(scroll_f, bg='#151515', pady=6); r.pack(fill='x', pady=2, padx=5)
                
                # --- LOGICA NPC / MOSTRI (3 COLONNE) ---
                if filtro in ['NPC_', 'MONS']:
                    ref = row_data[0]; base = row_data[1]; nome = row_data[2]
                    l_ref = tk.Label(r, text=f"REF: {ref}", fg=self.gold, bg="#151515", width=14, font=("Consolas", 9, "bold"))
                    l_ref.pack(side='left', padx=10)
                    #l_ref.bind("<Button-1>", lambda e, i=ref: self.copy_h(i, 'DA_TE', local_status))
                    
                    l_base = tk.Label(r, text=f"BASE: {base}", fg="#777", bg="#151515", width=14, font=("Consolas", 9))
                    l_base.pack(side='left')
                    #l_base.bind("<Button-1>", lambda e, i=base: self.copy_h(i, 'CLONE', local_status))

                    l_nome = tk.Label(r, text=nome, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w', width=55)
                    l_nome.pack(side='left', padx=15)
                    #l_nome.bind("<Button-1>", lambda e, i=ref: self.copy_h(i, 'DA_TE', local_status))

                    opzioni = {"Vieni da me": "DA_TE", "Vai da lui": "VAI", "Uccidi": "KILL", "Resuscita": "RES", "Abilita": "ENABLE", "Clona": "CLONE"}
                    sel_v = tk.StringVar(win); sel_v.set("Scegli Azione")

                    def applica_npc(v_str, r_id, b_id, s_var, n_obj):
                        scelta = v_str.get()
                        if scelta == "Scegli Azione": 
                            local_status.config(text="⚠️ SELEZIONA UN'AZIONE!", fg="red")
                            return
                        modo = opzioni[scelta]
                        # Passiamo anche n_obj (il nome) per soddisfare i 4 parametri
                        self.copy_h(b_id if modo == 'CLONE' else r_id, modo, n_obj, local_status)
                        s_var.set("Scegli Azione")

                    # Aggiorna il comando del pulsante APPLICA per passare il nome 'nome'
                    tk.Button(r, text="APPLICA", bg="#2e4d4d", fg="#fff", font=("Segoe UI", 7, "bold"), relief='flat', width=10, 
                              command=lambda s=sel_v, ri=ref, bi=base, sv=sel_v, no=nome: applica_npc(s, ri, bi, sv, no)).pack(side='right', padx=10)
                    
                    opt = tk.OptionMenu(r, sel_v, *opzioni.keys())
                    opt.config(bg="#1a1a1a", fg=self.gold, font=("Segoe UI", 8, "bold"), relief='flat', highlightthickness=0, width=15)
                    opt["menu"].config(bg="#1a1a1a", fg=self.gold); opt.pack(side='right', padx=5)

                # --- LOGICA STANDARD (2 COLONNE: ARMI, ARMATURE, ECC.) ---
                else:
                    fid = row_data[0]; nome = row_data[1]
                    l_id = tk.Label(r, text=fid, fg=self.gold, bg="#151515", width=14, font=("Consolas", 10, "bold"))
                    l_id.pack(side='left', padx=10)
                    #l_id.bind("<Button-1>", lambda e, i=fid: self.copy_h(i, 'ADD', local_status))
                    
                    l_n = tk.Label(r, text=nome, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w')
                    l_n.pack(side='left', padx=20, fill='x', expand=True)
                    #l_n.bind("<Button-1>", lambda e, i=fid: self.copy_h(i, 'ADD', local_status))
                    
                    tk.Button(r, text="COPIA", 
                                bg="#c4a45d", fg="#000", # Forza il colore ORO
                                font=("Segoe UI", 8, "bold"), relief='flat', width=12,
                                command=lambda i=fid, n=nome: self.copy_h(i, filtro, n, local_status)
                                ).pack(side='right', padx=10)

        def ch(d, tp):
            if 0 <= self.current_page + d < tp: self.current_page += d; draw(); canv.yview_moveto(0)

        self.after_id = None
        def reset_and_draw(*args):
            if self.after_id: win.after_cancel(self.after_id)
            self.after_id = win.after(1000, lambda: [setattr(self, 'current_page', 0), draw()])
        s_var.trace_add("write", reset_and_draw); draw()

    def open_console_cmds(self):
        win = tk.Toplevel(self.root)
        win.title("LISTA COMANDI CONSOLE")
        win.geometry("1200x900")
        win.configure(bg='#0a0a0a')

        # TITOLO IMPACT
        tk.Label(win, text="CONSOLE COMMANDS DATABASE", font=("Impact", 32), bg="#0a0a0a", fg=self.gold, pady=10).pack()

        # LABEL DI STATO LOCALE (In fondo alla finestra)
        con_status = tk.Label(win, text="SELEZIONA UN COMANDO", bg="#0a0a0a", fg="#555", font=("Segoe UI", 10, "bold"))
        con_status.pack(side="bottom", pady=5)

        # --- DATABASE INTEGRALE ---
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
        
        canv = tk.Canvas(cont, bg='#0a0a0a', highlightthickness=0)
        scr = tk.Scrollbar(cont, orient="vertical", command=canv.yview)
        scroll_f = tk.Frame(canv, bg='#0a0a0a')
        
        scroll_f.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv_win = canv.create_window((0, 0), window=scroll_f, anchor="nw")
        canv.bind('<Configure>', lambda e: canv.itemconfig(canv_win, width=e.width))
        canv.configure(yscrollcommand=scr.set)
        
        canv.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")

        def draw_console():
            for w in scroll_f.winfo_children(): w.destroy()
            for w in nav.winfo_children(): w.destroy()
            
            tot = len(console_data)
            tp = (tot // self.c_size) + 1
            st, en = self.c_page * self.c_size, (self.c_page + 1) * self.c_size
            
            if tp > 1:
                tk.Button(nav, text="◀ PREV", bg="#333", fg="#fff", relief='flat', cursor="hand2",
                          command=lambda: ch_c(-1, tp)).pack(side='left')
                tk.Label(nav, text=f"PAGINA {self.c_page + 1}/{tp} - {tot} COMANDI", 
                         bg="#0a0a0a", fg=self.gold, font=("Segoe UI", 9, "bold")).pack(side='left', expand=True)
                tk.Button(nav, text="NEXT ▶", bg="#333", fg="#fff", relief='flat', cursor="hand2",
                          command=lambda: ch_c(1, tp)).pack(side='right')

            for cmd, desc in console_data[st:en]:
                r = tk.Frame(scroll_f, bg='#151515', pady=10); r.pack(fill='x', pady=2, padx=5)
                tk.Label(r, text=cmd, fg=self.gold, bg="#151515", width=36, font=("Consolas", 10, "bold"), anchor='w').pack(side='left', padx=15)
                tk.Label(r, text=desc, fg="#eee", bg="#151515", font=("Segoe UI", 10), anchor='w').pack(side='left', padx=10, fill='x', expand=True)
                
                # Feedback locale nella label con_status
                tk.Button(r, text="COPIA", bg=self.gold, fg="#000", font=("Segoe UI", 8, "bold"), relief='flat', padx=15, 
                          command=lambda c=cmd: [pyperclip.copy(c), con_status.config(text=f"✅ COPIATO: {c}", fg=self.gold), 
                                                 win.after(4000, lambda: con_status.config(text="SELEZIONA UN COMANDO", fg="#555"))]).pack(side='right', padx=15)

        def ch_c(d, tp):
            if 0 <= self.c_page + d < tp:
                self.c_page += d; draw_console(); canv.yview_moveto(0)
        
        draw_console()

if __name__ == "__main__":
    root = tk.Tk(); app = SkyrimTool(root); root.mainloop()