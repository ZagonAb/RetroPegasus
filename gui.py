import json
import os
import platform
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import core


APP_TITLE        = "RetroPegasus Converter Tool"
PEGASUS_DEFAULT  = os.path.join(os.path.expanduser("~"), "pegasus-frontend")
LOG_EXTRA_HEIGHT = 220

PREFS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          ".retropegasus_prefs.json")

_PLATFORM = platform.system()


THEMES = {
    "light": {
        "bg":        "#eff0f1",
        "fg":        "#232629",
        "fg_dim":    "#7f8c8d",
        "entry_bg":  "#fcfcfc",
        "entry_fg":  "#232629",
        "log_bg":    "#fcfcfc",
        "log_fg":    "#232629",
        "accent":    "#3daee9",
        "accent_fg": "#ffffff",
        "select_bg": "#3daee9",
        "select_fg": "#ffffff",
        "warn_fg":   "#c0392b",
        "ok_fg":     "#27ae60",
    },
    "dark": {
        "bg":        "#31363b",
        "fg":        "#eff0f1",
        "fg_dim":    "#a0a8b0",
        "entry_bg":  "#232629",
        "entry_fg":  "#eff0f1",
        "log_bg":    "#1b1e20",
        "log_fg":    "#c8d0d8",
        "accent":    "#3daee9",
        "accent_fg": "#ffffff",
        "select_bg": "#3daee9",
        "select_fg": "#ffffff",
        "warn_fg":   "#e74c3c",
        "ok_fg":     "#2ecc71",
    },
}

THEME_OPTIONS = [("☀  Light", "light"), ("☾  Dark", "dark")]

STRINGS = {
    "en": {
        "lang_label":           "Language:",
        "theme_label":          "Theme:",
        "section_retroarch":    "1. RetroArch Installation",
        "btn_auto_detect":      "Auto-detect",
        "btn_browse":           "Browse...",
        "section_output":       "2. Output folder (pegasus-frontend)",
        "out_hint_valid":       "✓ Folder exists — content will be overwritten",
        "out_hint_new":         "New folder will be created",
        "out_hint_invalid":     "⚠ Parent path does not exist",
        "section_media":        "3. Image handling (boxart, snaps, etc.)",
        "media_absolute":       "Use absolute paths (recommended, no files copied)",
        "media_copy":           "Copy media files into the Pegasus folder (portable, slower)",
        "media_skip":           "No images",
        "section_systems":      "4. Systems to migrate",
        "btn_select_all":       "Select all",
        "btn_deselect_all":     "Deselect all",
        "lbl_systems_hint":     "(load a RetroArch installation first)",
        "lbl_systems_found":    "{n} systems found",
        "btn_start":            "Start migration",
        "btn_cancel":           "Cancel",
        "btn_show_log":         "▸ Show log",
        "btn_hide_log":         "▾ Hide log",
        "log_frame":            "Log",
        "log_searching":        "Searching for RetroArch installations...",
        "warn_no_retroarch":    "No RetroArch installation was found automatically.\nUse 'Browse...' to select the folder manually.",
        "win_choose_title":     "Choose an installation",
        "lbl_multiple_found":   "Multiple RetroArch installations were found:",
        "btn_use_this":         "Use this",
        "browse_retroarch":     "Select the RetroArch installation folder",
        "err_invalid_ra":       "The selected folder is not a valid RetroArch installation:\n\n",
        "log_ra_set":           "RetroArch path set: {path}",
        "browse_output":        "Select where to create the pegasus-frontend folder",
        "warn_no_ra_selected":  "Please select a valid RetroArch installation first.",
        "warn_no_systems":      "Select at least one system to migrate.",
        "warn_no_output":       "Please specify an output folder.",
        "err_output_invalid":   "The output path's parent folder does not exist.\nPlease choose a valid location.",
        "err_create_output":    "Could not create the output folder:\n",
        "confirm_cancel_title": "Cancel migration?",
        "confirm_cancel_msg":   "The migration is still running.\n\nIf you cancel now, partially written files may remain in:\n{path}\n\nCancel anyway?",
        "log_cancelled":        "Migration cancelled by user.",
        "log_done":             "✓ Migration complete: {processed} collections, {total_games} games.",
        "log_media":            "Media copied: {copied} (errors: {errors})",
        "log_skipped":          "Unrecognized systems (skipped): ",
        "dlg_done_title":       "Migration complete",
        "dlg_done_msg":         "Migration complete.\n\nCollections processed: {processed}\nTotal games: {total_games}",
        "dlg_done_media":       "\nMedia copied: {copied} (errors: {errors})",
        "log_error":            "ERROR: {msg}",
        "err_migration":        "An error occurred during migration:\n",
    },
    "es": {
        "lang_label":           "Idioma:",
        "theme_label":          "Tema:",
        "section_retroarch":    "1. Instalación de RetroArch",
        "btn_auto_detect":      "Auto-detectar",
        "btn_browse":           "Elegir carpeta...",
        "section_output":       "2. Carpeta de salida (pegasus-frontend)",
        "out_hint_valid":       "✓ La carpeta existe — su contenido será sobreescrito",
        "out_hint_new":         "Se creará una carpeta nueva",
        "out_hint_invalid":     "⚠ La carpeta padre no existe",
        "section_media":        "3. Manejo de imágenes (boxart, snaps, etc.)",
        "media_absolute":       "Usar rutas absolutas (recomendado, no copia archivos)",
        "media_copy":           "Copiar archivos de medios a la carpeta de Pegasus (portable, más lento)",
        "media_skip":           "Sin imágenes",
        "section_systems":      "4. Sistemas a migrar",
        "btn_select_all":       "Seleccionar todos",
        "btn_deselect_all":     "Deseleccionar todos",
        "lbl_systems_hint":     "(cargá una instalación de RetroArch primero)",
        "lbl_systems_found":    "{n} sistemas encontrados",
        "btn_start":            "Iniciar migración",
        "btn_cancel":           "Cancelar",
        "btn_show_log":         "▸ Mostrar registro",
        "btn_hide_log":         "▾ Ocultar registro",
        "log_frame":            "Registro",
        "log_searching":        "Buscando instalaciones de RetroArch...",
        "warn_no_retroarch":    "No se encontró ninguna instalación de RetroArch automáticamente.\nUsá 'Elegir carpeta...' para indicarla manualmente.",
        "win_choose_title":     "Elegí una instalación",
        "lbl_multiple_found":   "Se encontraron varias instalaciones de RetroArch:",
        "btn_use_this":         "Usar esta",
        "browse_retroarch":     "Seleccioná la carpeta de instalación de RetroArch",
        "err_invalid_ra":       "La carpeta seleccionada no es una instalación válida de RetroArch:\n\n",
        "log_ra_set":           "RetroArch path establecido: {path}",
        "browse_output":        "Seleccioná dónde crear la carpeta pegasus-frontend",
        "warn_no_ra_selected":  "Primero seleccioná una instalación válida de RetroArch.",
        "warn_no_systems":      "Seleccioná al menos un sistema para migrar.",
        "warn_no_output":       "Indicá una carpeta de salida.",
        "err_output_invalid":   "La carpeta padre de la ruta de salida no existe.\nElegí una ubicación válida.",
        "err_create_output":    "No se pudo crear la carpeta de salida:\n",
        "confirm_cancel_title": "¿Cancelar migración?",
        "confirm_cancel_msg":   "La migración todavía está en curso.\n\nSi cancelás ahora, pueden quedar archivos parciales en:\n{path}\n\n¿Cancelar de todas formas?",
        "log_cancelled":        "Migración cancelada por el usuario.",
        "log_done":             "✓ Migración completada: {processed} colecciones, {total_games} juegos.",
        "log_media":            "Medios copiados: {copied} (errores: {errors})",
        "log_skipped":          "Sistemas no reconocidos (omitidos): ",
        "dlg_done_title":       "Migración completada",
        "dlg_done_msg":         "Migración completada.\n\nColecciones procesadas: {processed}\nJuegos totales: {total_games}",
        "dlg_done_media":       "\nMedios copiados: {copied} (errores: {errors})",
        "log_error":            "ERROR: {msg}",
        "err_migration":        "Ocurrió un error durante la migración:\n",
    },
    "pt": {
        "lang_label":           "Idioma:",
        "theme_label":          "Tema:",
        "section_retroarch":    "1. Instalação do RetroArch",
        "btn_auto_detect":      "Auto-detectar",
        "btn_browse":           "Escolher pasta...",
        "section_output":       "2. Pasta de saída (pegasus-frontend)",
        "out_hint_valid":       "✓ A pasta existe — o conteúdo será substituído",
        "out_hint_new":         "Uma nova pasta será criada",
        "out_hint_invalid":     "⚠ A pasta pai não existe",
        "section_media":        "3. Gestão de imagens (boxart, snaps, etc.)",
        "media_absolute":       "Usar caminhos absolutos (recomendado, sem copiar arquivos)",
        "media_copy":           "Copiar arquivos de mídia para a pasta do Pegasus (portável, mais lento)",
        "media_skip":           "Sem imagens",
        "section_systems":      "4. Sistemas a migrar",
        "btn_select_all":       "Selecionar todos",
        "btn_deselect_all":     "Desmarcar todos",
        "lbl_systems_hint":     "(carregue uma instalação do RetroArch primeiro)",
        "lbl_systems_found":    "{n} sistemas encontrados",
        "btn_start":            "Iniciar migração",
        "btn_cancel":           "Cancelar",
        "btn_show_log":         "▸ Mostrar registro",
        "btn_hide_log":         "▾ Ocultar registro",
        "log_frame":            "Registro",
        "log_searching":        "Procurando instalações do RetroArch...",
        "warn_no_retroarch":    "Nenhuma instalação do RetroArch foi encontrada automaticamente.\nUse 'Escolher pasta...' para indicá-la manualmente.",
        "win_choose_title":     "Escolha uma instalação",
        "lbl_multiple_found":   "Várias instalações do RetroArch foram encontradas:",
        "btn_use_this":         "Usar esta",
        "browse_retroarch":     "Selecione a pasta de instalação do RetroArch",
        "err_invalid_ra":       "A pasta selecionada não é uma instalação válida do RetroArch:\n\n",
        "log_ra_set":           "Caminho do RetroArch definido: {path}",
        "browse_output":        "Selecione onde criar a pasta pegasus-frontend",
        "warn_no_ra_selected":  "Selecione primeiro uma instalação válida do RetroArch.",
        "warn_no_systems":      "Selecione pelo menos um sistema para migrar.",
        "warn_no_output":       "Indique uma pasta de saída.",
        "err_output_invalid":   "A pasta pai do caminho de saída não existe.\nEscolha um local válido.",
        "err_create_output":    "Não foi possível criar a pasta de saída:\n",
        "confirm_cancel_title": "Cancelar migração?",
        "confirm_cancel_msg":   "A migração ainda está em curso.\n\nSe cancelar agora, arquivos parciais podem permanecer em:\n{path}\n\nCancelar mesmo assim?",
        "log_cancelled":        "Migração cancelada pelo usuário.",
        "log_done":             "✓ Migração concluída: {processed} coleções, {total_games} jogos.",
        "log_media":            "Mídias copiadas: {copied} (erros: {errors})",
        "log_skipped":          "Sistemas não reconhecidos (ignorados): ",
        "dlg_done_title":       "Migração concluída",
        "dlg_done_msg":         "Migração concluída.\n\nColeções processadas: {processed}\nTotal de jogos: {total_games}",
        "dlg_done_media":       "\nMídias copiadas: {copied} (erros: {errors})",
        "log_error":            "ERRO: {msg}",
        "err_migration":        "Ocorreu um erro durante a migração:\n",
    },
    "fr": {
        "lang_label":           "Langue :",
        "theme_label":          "Thème :",
        "section_retroarch":    "1. Installation de RetroArch",
        "btn_auto_detect":      "Détection auto",
        "btn_browse":           "Choisir dossier...",
        "section_output":       "2. Dossier de sortie (pegasus-frontend)",
        "out_hint_valid":       "✓ Le dossier existe — son contenu sera écrasé",
        "out_hint_new":         "Un nouveau dossier sera créé",
        "out_hint_invalid":     "⚠ Le dossier parent n'existe pas",
        "section_media":        "3. Gestion des images (jaquettes, captures, etc.)",
        "media_absolute":       "Utiliser des chemins absolus (recommandé, aucun fichier copié)",
        "media_copy":           "Copier les fichiers médias dans le dossier Pegasus (portable, plus lent)",
        "media_skip":           "Sans images",
        "section_systems":      "4. Systèmes à migrer",
        "btn_select_all":       "Tout sélectionner",
        "btn_deselect_all":     "Tout désélectionner",
        "lbl_systems_hint":     "(chargez d'abord une installation de RetroArch)",
        "lbl_systems_found":    "{n} systèmes trouvés",
        "btn_start":            "Démarrer la migration",
        "btn_cancel":           "Annuler",
        "btn_show_log":         "▸ Afficher le journal",
        "btn_hide_log":         "▾ Masquer le journal",
        "log_frame":            "Journal",
        "log_searching":        "Recherche des installations de RetroArch...",
        "warn_no_retroarch":    "Aucune installation de RetroArch n'a été trouvée automatiquement.\nUtilisez 'Choisir dossier...' pour la sélectionner manuellement.",
        "win_choose_title":     "Choisir une installation",
        "lbl_multiple_found":   "Plusieurs installations de RetroArch ont été trouvées :",
        "btn_use_this":         "Utiliser celle-ci",
        "browse_retroarch":     "Sélectionnez le dossier d'installation de RetroArch",
        "err_invalid_ra":       "Le dossier sélectionné n'est pas une installation valide de RetroArch :\n\n",
        "log_ra_set":           "Chemin RetroArch défini : {path}",
        "browse_output":        "Sélectionnez où créer le dossier pegasus-frontend",
        "warn_no_ra_selected":  "Veuillez d'abord sélectionner une installation valide de RetroArch.",
        "warn_no_systems":      "Sélectionnez au moins un système à migrer.",
        "warn_no_output":       "Veuillez indiquer un dossier de sortie.",
        "err_output_invalid":   "Le dossier parent du chemin de sortie n'existe pas.\nVeuillez choisir un emplacement valide.",
        "err_create_output":    "Impossible de créer le dossier de sortie :\n",
        "confirm_cancel_title": "Annuler la migration ?",
        "confirm_cancel_msg":   "La migration est toujours en cours.\n\nSi vous annulez maintenant, des fichiers partiels peuvent rester dans :\n{path}\n\nAnnuler quand même ?",
        "log_cancelled":        "Migration annulée par l'utilisateur.",
        "log_done":             "✓ Migration terminée : {processed} collections, {total_games} jeux.",
        "log_media":            "Médias copiés : {copied} (erreurs : {errors})",
        "log_skipped":          "Systèmes non reconnus (ignorés) : ",
        "dlg_done_title":       "Migration terminée",
        "dlg_done_msg":         "Migration terminée.\n\nCollections traitées : {processed}\nTotal de jeux : {total_games}",
        "dlg_done_media":       "\nMédias copiés : {copied} (erreurs : {errors})",
        "log_error":            "ERREUR : {msg}",
        "err_migration":        "Une erreur s'est produite pendant la migration :\n",
    },
}

LANG_OPTIONS = [
    ("English",   "en"),
    ("Español",   "es"),
    ("Português", "pt"),
    ("Français",  "fr"),
]

def load_prefs():
    try:
        with open(PREFS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_prefs(prefs: dict):
    try:
        with open(PREFS_PATH, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
    except Exception:
        pass


def _enable_dpi_awareness():
    if _PLATFORM == "Windows":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

class RetroPegasusGUI(tk.Tk):

    def __init__(self):
        _enable_dpi_awareness()
        super().__init__()
        self.title(APP_TITLE)

        prefs = load_prefs()

        self.retroarch_path = tk.StringVar(value=prefs.get("retroarch_path", ""))
        self.output_path    = tk.StringVar(value=PEGASUS_DEFAULT)
        self.media_mode     = tk.StringVar(value="1")
        self.lang_code      = tk.StringVar(value=prefs.get("lang", "en"))
        self.theme_code     = tk.StringVar(value=prefs.get("theme", "light"))

        self.playlists_path  = None
        self.thumbnails_path = None
        self.system_vars     = {}
        self.log_visible     = False
        self._migration_output_path = ""

        self.worker_thread = None
        self.cancel_flag   = threading.Event()
        self.ui_queue      = queue.Queue()

        self._build_layout()
        self._apply_theme()
        self._apply_language()
        self._validate_output_path()

        saved_ra = prefs.get("retroarch_path", "")
        if saved_ra and os.path.isdir(saved_ra):
            self.after(200, lambda: self._set_retroarch_path(saved_ra, silent=True))

        lang_codes = [c for _, c in LANG_OPTIONS]
        if self.lang_code.get() in lang_codes:
            self.lang_combo.current(lang_codes.index(self.lang_code.get()))

        theme_codes = [c for _, c in THEME_OPTIONS]
        if self.theme_code.get() in theme_codes:
            self.theme_combo.current(theme_codes.index(self.theme_code.get()))

        self.update_idletasks()
        width  = max(self.winfo_reqwidth(), 780)
        height = self.winfo_reqheight()
        self.geometry(f"{width}x{height}")
        self.minsize(660, height)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.after(100, self._poll_queue)

    def _t(self, key, **kw):
        lang  = self.lang_code.get()
        table = STRINGS.get(lang, STRINGS["en"])
        text  = table.get(key, STRINGS["en"].get(key, key))
        return text.format(**kw) if kw else text

    def _th(self, key):
        return THEMES[self.theme_code.get()][key]

    def _on_close(self):
        save_prefs({
            "lang":           self.lang_code.get(),
            "theme":          self.theme_code.get(),
            "retroarch_path": self.retroarch_path.get(),
        })
        self.destroy()

    def _build_layout(self):
        pad = {"padx": 10, "pady": 6}

        self.top_bar = tk.Frame(self)
        self.top_bar.pack(fill="x", padx=10, pady=(8, 2))

        self.lbl_lang = tk.Label(self.top_bar, text="Language:")
        self.lbl_lang.pack(side="left")

        self._lang_labels = [lbl for lbl, _ in LANG_OPTIONS]
        self._lang_codes  = [code for _, code in LANG_OPTIONS]
        self.lang_combo = ttk.Combobox(
            self.top_bar, values=self._lang_labels, width=11, state="readonly")
        self.lang_combo.current(0)
        self.lang_combo.pack(side="left", padx=(4, 16))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.lbl_theme = tk.Label(self.top_bar, text="Theme:")
        self.lbl_theme.pack(side="left")

        self._theme_labels = [lbl for lbl, _ in THEME_OPTIONS]
        self._theme_codes  = [code for _, code in THEME_OPTIONS]
        self.theme_combo = ttk.Combobox(
            self.top_bar, values=self._theme_labels, width=10, state="readonly")
        self.theme_combo.current(0)
        self.theme_combo.pack(side="left", padx=(4, 0))
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)

        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(fill="x", padx=10, pady=(4, 0))

        self.frame_ra = tk.LabelFrame(self, text="")
        self.frame_ra.pack(fill="x", **pad)

        self.entry_ra = tk.Entry(self.frame_ra, textvariable=self.retroarch_path)
        self.entry_ra.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=8)

        self.btn_auto_detect = tk.Button(
            self.frame_ra, text="", command=self._auto_detect, relief="flat", padx=8)
        self.btn_auto_detect.pack(side="left", padx=4, pady=8)

        self.btn_browse_ra = tk.Button(
            self.frame_ra, text="", command=self._browse_retroarch, relief="flat", padx=8)
        self.btn_browse_ra.pack(side="left", padx=(4, 8), pady=8)

        self.frame_out = tk.LabelFrame(self, text="")
        self.frame_out.pack(fill="x", **pad)

        self.entry_out = tk.Entry(self.frame_out, textvariable=self.output_path)
        self.entry_out.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=(8, 2))

        self.btn_browse_out = tk.Button(
            self.frame_out, text="", command=self._browse_output, relief="flat", padx=8)
        self.btn_browse_out.pack(side="left", padx=(4, 8), pady=8)

        self.lbl_out_hint = tk.Label(self.frame_out, text="", anchor="w", font=("", 8))
        self.lbl_out_hint.pack(side="bottom", fill="x", padx=8, pady=(0, 6))

        self.output_path.trace_add("write", lambda *_: self._validate_output_path())

        self.frame_media = tk.LabelFrame(self, text="")
        self.frame_media.pack(fill="x", **pad)

        self.rb_absolute = tk.Radiobutton(
            self.frame_media, text="", variable=self.media_mode, value="1")
        self.rb_absolute.pack(anchor="w", padx=8, pady=2)

        self.rb_copy = tk.Radiobutton(
            self.frame_media, text="", variable=self.media_mode, value="2")
        self.rb_copy.pack(anchor="w", padx=8, pady=2)

        self.rb_skip = tk.Radiobutton(
            self.frame_media, text="", variable=self.media_mode, value="3")
        self.rb_skip.pack(anchor="w", padx=8, pady=2)

        self.frame_actions = tk.Frame(self)
        self.frame_actions.pack(fill="x", side="bottom", **pad)

        self.btn_start = tk.Button(
            self.frame_actions, text="", command=self._start_migration,
            relief="flat", padx=12, pady=4)
        self.btn_start.pack(side="left")

        self.btn_cancel = tk.Button(
            self.frame_actions, text="", command=self._cancel_migration,
            relief="flat", padx=12, pady=4, state="disabled")
        self.btn_cancel.pack(side="left", padx=8)

        self.progress = ttk.Progressbar(self.frame_actions, mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=10)

        self.frame_log_container = tk.Frame(self)
        self.frame_log_container.pack(fill="x", side="bottom", padx=10, pady=(0, 6))

        self.btn_toggle_log = tk.Button(
            self.frame_log_container, text="", command=self._toggle_log,
            relief="flat", anchor="w")
        self.btn_toggle_log.pack(anchor="w")

        self.frame_log = tk.LabelFrame(self, text="")

        self.log_text = tk.Text(
            self.frame_log, height=10, state="disabled", wrap="word", relief="flat")
        log_scroll = ttk.Scrollbar(
            self.frame_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        log_scroll.pack(side="right", fill="y", pady=8)

        self.frame_sys = tk.LabelFrame(self, text="")
        self.frame_sys.pack(fill="both", expand=True, **pad)

        self.sys_toolbar = tk.Frame(self.frame_sys)
        self.sys_toolbar.pack(fill="x", padx=8, pady=(8, 0))

        self.btn_select_all = tk.Button(
            self.sys_toolbar, text="", command=lambda: self._set_all(True),
            relief="flat", padx=8)
        self.btn_select_all.pack(side="left")

        self.btn_deselect_all = tk.Button(
            self.sys_toolbar, text="", command=lambda: self._set_all(False),
            relief="flat", padx=8)
        self.btn_deselect_all.pack(side="left", padx=6)

        self.lbl_systems_count = tk.Label(self.sys_toolbar, text="")
        self.lbl_systems_count.pack(side="left", padx=10)

        canvas_frame = tk.Frame(self.frame_sys)
        canvas_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.canvas = tk.Canvas(
            canvas_frame, borderwidth=0, highlightthickness=0, height=180)
        sys_scroll = ttk.Scrollbar(
            canvas_frame, orient="vertical", command=self.canvas.yview)
        self.checkboxes_frame = tk.Frame(self.canvas)

        self.checkboxes_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.checkboxes_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=sys_scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sys_scroll.pack(side="right", fill="y")

        self._bind_mousewheel()


    def _bind_mousewheel(self):
        def _on_wheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                delta = event.delta
                if _PLATFORM == "Darwin":
                    self.canvas.yview_scroll(-int(delta), "units")
                else:
                    self.canvas.yview_scroll(-int(delta / 120), "units")

        for seq in ("<Button-4>", "<Button-5>"):
            self.canvas.bind(seq, _on_wheel)
            self.checkboxes_frame.bind(seq, _on_wheel)

        self.canvas.bind("<MouseWheel>", _on_wheel)
        self.checkboxes_frame.bind("<MouseWheel>", _on_wheel)

        self._wheel_handler = _on_wheel

    def _bind_wheel_to_children(self):
        handler = self._wheel_handler
        for child in self.checkboxes_frame.winfo_children():
            child.bind("<Button-4>",    handler)
            child.bind("<Button-5>",    handler)
            child.bind("<MouseWheel>",  handler)


    def _validate_output_path(self):
        path = self.output_path.get().strip()
        if not path:
            self.lbl_out_hint.config(text="", fg=self._th("fg_dim"))
            return

        if os.path.exists(path):
            is_empty = os.path.isdir(path) and not os.listdir(path)
            if is_empty:
                self.lbl_out_hint.config(
                    text=self._t("out_hint_new"), fg=self._th("ok_fg"))
            else:
                self.lbl_out_hint.config(
                    text=self._t("out_hint_valid"), fg=self._th("warn_fg"))
        else:
            parent = os.path.dirname(path.rstrip("/\\"))
            if parent and os.path.isdir(parent):
                self.lbl_out_hint.config(
                    text=self._t("out_hint_new"), fg=self._th("ok_fg"))
            else:
                self.lbl_out_hint.config(
                    text=self._t("out_hint_invalid"), fg=self._th("warn_fg"))


    def _dialog(self, kind, title, message, *, buttons=None):
        if buttons is None:
            buttons = [("OK", True)]

        bg        = self._th("bg")
        fg        = self._th("fg")
        fg_dim    = self._th("fg_dim")
        accent    = self._th("accent")
        accent_fg = self._th("accent_fg")
        entry_bg  = self._th("entry_bg")

        icon_map  = {"info": "ℹ", "warning": "⚠", "error": "✖"}
        icon_col  = {"info": accent, "warning": "#e67e22", "error": "#e74c3c"}

        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=bg)
        win.resizable(False, False)
        win.grab_set()
        win.focus_set()

        self.update_idletasks()
        pw, ph = self.winfo_width(), self.winfo_height()
        px, py = self.winfo_rootx(), self.winfo_rooty()

        result = [None]

        frame_top = tk.Frame(win, bg=bg)
        frame_top.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        tk.Label(frame_top, text=icon_map.get(kind, "ℹ"),
                 bg=bg, fg=icon_col.get(kind, accent),
                 font=("", 24)).pack(side="left", anchor="n", padx=(0, 14))

        tk.Label(frame_top, text=message, bg=bg, fg=fg,
                 justify="left", wraplength=380,
                 font=("", 10)).pack(side="left", anchor="nw")

        sep = tk.Frame(win, bg=fg_dim, height=1)
        sep.pack(fill="x", padx=0, pady=(6, 0))

        frame_btn = tk.Frame(win, bg=bg)
        frame_btn.pack(fill="x", padx=16, pady=12)

        def make_cmd(val):
            def cmd():
                result[0] = val
                win.destroy()
            return cmd

        for i, (lbl, val) in enumerate(buttons):
            is_primary = (i == len(buttons) - 1)
            btn = tk.Button(
                frame_btn, text=lbl, command=make_cmd(val),
                relief="flat", padx=14, pady=5,
                bg=accent if is_primary else entry_bg,
                fg=accent_fg if is_primary else fg,
                activebackground=fg_dim,
                activeforeground=fg,
                highlightthickness=1,
                highlightbackground=fg_dim,
                cursor="hand2",
            )
            btn.pack(side="right", padx=(6, 0))

        win.update_idletasks()
        ww = win.winfo_reqwidth()
        wh = win.winfo_reqheight()
        wx = px + (pw - ww) // 2
        wy = py + (ph - wh) // 2
        win.geometry(f"{ww}x{wh}+{wx}+{wy}")

        win.bind("<Return>", lambda e: make_cmd(buttons[-1][1])())
        win.bind("<Escape>", lambda e: win.destroy())

        win.wait_window()
        return result[0]

    def _ask(self, title, message):
        yes_lbl = {"en": "Yes", "es": "Sí", "pt": "Sim", "fr": "Oui"}.get(
            self.lang_code.get(), "Yes")
        no_lbl  = {"en": "No",  "es": "No", "pt": "Não", "fr": "Non"}.get(
            self.lang_code.get(), "No")
        return self._dialog(
            "warning", title, message,
            buttons=[(no_lbl, False), (yes_lbl, True)],
        )

    def _apply_theme(self):
        bg       = self._th("bg")
        fg       = self._th("fg")
        fg_dim   = self._th("fg_dim")
        entry_bg = self._th("entry_bg")
        entry_fg = self._th("entry_fg")
        log_bg   = self._th("log_bg")
        log_fg   = self._th("log_fg")
        accent   = self._th("accent")
        accent_fg= self._th("accent_fg")
        sel_bg   = self._th("select_bg")
        sel_fg   = self._th("select_fg")

        self.configure(bg=bg)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".",
            background=bg, foreground=fg,
            fieldbackground=entry_bg,
            selectbackground=sel_bg, selectforeground=sel_fg,
            troughcolor=bg, bordercolor=fg_dim,
            darkcolor=bg, lightcolor=bg,
        )
        style.configure("TCombobox",
            fieldbackground=entry_bg, foreground=entry_fg,
            selectbackground=sel_bg, selectforeground=sel_fg,
            background=bg,
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", entry_bg)],
            foreground=[("readonly", entry_fg)],
        )
        style.configure("TScrollbar",
            background=bg, troughcolor=bg, arrowcolor=fg)
        style.configure("TProgressbar",
            background=accent, troughcolor=entry_bg)
        style.configure("TSeparator", background=fg_dim)

        def paint(widget):
            cls = widget.winfo_class()
            try:
                if cls in ("Frame", "Labelframe"):
                    widget.configure(bg=bg)
                    if cls == "Labelframe":
                        widget.configure(fg=fg)
                elif cls == "Label":
                    widget.configure(bg=bg, fg=fg)
                elif cls == "Button":
                    widget.configure(
                        bg=bg, fg=fg,
                        activebackground=accent, activeforeground=accent_fg,
                        highlightbackground=fg_dim, highlightthickness=1,
                        disabledforeground=fg_dim,
                    )
                elif cls == "Entry":
                    widget.configure(
                        bg=entry_bg, fg=entry_fg,
                        insertbackground=fg,
                        selectbackground=sel_bg, selectforeground=sel_fg,
                        relief="flat", highlightthickness=1,
                        highlightbackground=fg_dim, highlightcolor=accent,
                    )
                elif cls == "Radiobutton":
                    widget.configure(
                        bg=bg, fg=fg,
                        activebackground=bg, activeforeground=accent,
                        selectcolor=entry_bg,
                    )
                elif cls == "Checkbutton":
                    widget.configure(
                        bg=bg, fg=fg,
                        activebackground=bg, activeforeground=accent,
                        selectcolor=entry_bg,
                    )
                elif cls == "Canvas":
                    widget.configure(bg=bg)
                elif cls == "Text":
                    widget.configure(
                        bg=log_bg, fg=log_fg,
                        insertbackground=fg,
                        selectbackground=sel_bg, selectforeground=sel_fg,
                    )
                elif cls == "Listbox":
                    widget.configure(
                        bg=entry_bg, fg=entry_fg,
                        selectbackground=sel_bg, selectforeground=sel_fg,
                    )
            except tk.TclError:
                pass
            for child in widget.winfo_children():
                paint(child)

        paint(self)

        self.checkboxes_frame.configure(bg=bg)
        for child in self.checkboxes_frame.winfo_children():
            try:
                child.configure(
                    bg=bg, fg=fg,
                    activebackground=bg, activeforeground=accent,
                    selectcolor=entry_bg,
                )
            except tk.TclError:
                pass

        try:
            self.btn_start.configure(
                bg=accent, fg=accent_fg,
                activebackground=sel_bg, activeforeground=accent_fg,
            )
        except Exception:
            pass

        self._validate_output_path()

    def _apply_language(self):
        t = self._t
        self.lbl_lang.config(text=t("lang_label"))
        self.lbl_theme.config(text=t("theme_label"))

        self.frame_ra.config(text=t("section_retroarch"))
        self.btn_auto_detect.config(text=t("btn_auto_detect"))
        self.btn_browse_ra.config(text=t("btn_browse"))

        self.frame_out.config(text=t("section_output"))
        self.btn_browse_out.config(text=t("btn_browse"))

        self.frame_media.config(text=t("section_media"))
        self.rb_absolute.config(text=t("media_absolute"))
        self.rb_copy.config(text=t("media_copy"))
        self.rb_skip.config(text=t("media_skip"))

        self.btn_start.config(text=t("btn_start"))
        self.btn_cancel.config(text=t("btn_cancel"))

        log_key = "btn_hide_log" if self.log_visible else "btn_show_log"
        self.btn_toggle_log.config(text=t(log_key))
        self.frame_log.config(text=t("log_frame"))

        self.frame_sys.config(text=t("section_systems"))
        self.btn_select_all.config(text=t("btn_select_all"))
        self.btn_deselect_all.config(text=t("btn_deselect_all"))

        if self.system_vars:
            self.lbl_systems_count.config(
                text=t("lbl_systems_found", n=len(self.system_vars)))
        else:
            self.lbl_systems_count.config(text=t("lbl_systems_hint"))

        self._validate_output_path()

    def _on_lang_change(self, _=None):
        self.lang_code.set(self._lang_codes[self.lang_combo.current()])
        self._apply_language()

    def _on_theme_change(self, _=None):
        self.theme_code.set(self._theme_codes[self.theme_combo.current()])
        self._apply_theme()
        accent    = self._th("accent")
        accent_fg = self._th("accent_fg")
        sel_bg    = self._th("select_bg")
        self.btn_start.configure(
            bg=accent, fg=accent_fg,
            activebackground=sel_bg, activeforeground=accent_fg,
        )

    def _toggle_log(self):
        self.log_visible = not self.log_visible
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x, y = self.winfo_x(), self.winfo_y()

        if self.log_visible:
            self.frame_log.pack(
                fill="both", expand=True, side="bottom", padx=10, pady=(0, 6))
            self.btn_toggle_log.config(text=self._t("btn_hide_log"))
            self.geometry(f"{w}x{h + LOG_EXTRA_HEIGHT}+{x}+{y}")
        else:
            self.frame_log.pack_forget()
            self.btn_toggle_log.config(text=self._t("btn_show_log"))
            new_h = max(h - LOG_EXTRA_HEIGHT, self.minsize()[1])
            self.geometry(f"{w}x{new_h}+{x}+{y}")

    def _log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_all(self, value):
        for var in self.system_vars.values():
            var.set(value)

    def _populate_systems(self, systems):
        for widget in self.checkboxes_frame.winfo_children():
            widget.destroy()
        self.system_vars = {}

        bg       = self._th("bg")
        fg       = self._th("fg")
        entry_bg = self._th("entry_bg")
        accent   = self._th("accent")

        for system_name in systems:
            var = tk.BooleanVar(value=True)
            cb  = tk.Checkbutton(
                self.checkboxes_frame, text=system_name, variable=var,
                bg=bg, fg=fg, activebackground=bg, activeforeground=accent,
                selectcolor=entry_bg, anchor="w",
            )
            cb.pack(anchor="w", padx=4, pady=1)
            self.system_vars[system_name] = var

        self.lbl_systems_count.config(
            text=self._t("lbl_systems_found", n=len(systems)))

        self._bind_wheel_to_children()

    def _auto_detect(self):
        self._log(self._t("log_searching"))
        candidates = core.find_retroarch_candidates(on_progress=self._log)

        if not candidates:
            self._dialog("warning", APP_TITLE, self._t("warn_no_retroarch"))
            return
        if len(candidates) == 1:
            self._set_retroarch_path(candidates[0])
        else:
            self._choose_among(candidates)

    def _choose_among(self, candidates):
        win = tk.Toplevel(self)
        win.title(self._t("win_choose_title"))
        win.configure(bg=self._th("bg"))
        win.geometry("520x200")
        tk.Label(win, text=self._t("lbl_multiple_found"),
                 bg=self._th("bg"), fg=self._th("fg")).pack(pady=10)

        listbox = tk.Listbox(
            win,
            bg=self._th("entry_bg"), fg=self._th("entry_fg"),
            selectbackground=self._th("select_bg"),
            selectforeground=self._th("select_fg"),
        )
        for c in candidates:
            listbox.insert("end", c)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        def confirm():
            sel = listbox.curselection()
            if sel:
                self._set_retroarch_path(candidates[sel[0]])
                win.destroy()

        tk.Button(
            win, text=self._t("btn_use_this"), command=confirm,
            bg=self._th("accent"), fg=self._th("accent_fg"),
            relief="flat", padx=10,
        ).pack(pady=8)

    def _browse_retroarch(self):
        path = filedialog.askdirectory(title=self._t("browse_retroarch"))
        if path:
            self._set_retroarch_path(path)

    def _set_retroarch_path(self, path, silent=False):
        is_valid, errors = core.verify_retroarch_folders(path)
        if not is_valid:
            if not silent:
                self._dialog("error", APP_TITLE, self._t("err_invalid_ra") + "\n".join(errors))
            return

        self.retroarch_path.set(path)
        self.thumbnails_path = core.find_thumbnails_path(path)
        self.playlists_path  = core.find_playlists_path(path)
        self._log(self._t("log_ra_set", path=path))
        self._populate_systems(core.list_playlists(self.playlists_path))

    def _browse_output(self):
        path = filedialog.askdirectory(title=self._t("browse_output"))
        if path:
            self.output_path.set(os.path.normpath(path))

    def _start_migration(self):
        if not self.playlists_path:
            self._dialog("warning", APP_TITLE, self._t("warn_no_ra_selected"))
            return

        selected_systems = [n for n, v in self.system_vars.items() if v.get()]
        if not selected_systems:
            self._dialog("warning", APP_TITLE, self._t("warn_no_systems"))
            return

        output_path = os.path.normpath(self.output_path.get().strip())
        if not output_path:
            self._dialog("warning", APP_TITLE, self._t("warn_no_output"))
            return

        parent = os.path.dirname(output_path)
        if parent and not os.path.isdir(parent):
            self._dialog("error", APP_TITLE, self._t("err_output_invalid"))
            return

        try:
            os.makedirs(output_path, exist_ok=True)
        except Exception as e:
            self._dialog("error", APP_TITLE, self._t("err_create_output") + str(e))
            return

        self._migration_output_path = output_path
        self.cancel_flag.clear()
        self.btn_start.config(state="disabled")
        self.btn_cancel.config(state="normal")
        self.progress.start(12)

        logger = core.setup_logging(output_path)
        logger.info("=== RetroPegasus Converter Tool Started (GUI) ===")

        media_choice    = self.media_mode.get()
        thumbnails_base = self.thumbnails_path if media_choice in ("1", "2") else None
        copy_media      = media_choice == "2"

        self.worker_thread = threading.Thread(
            target=self._run_migration_worker,
            args=(logger, selected_systems, output_path, thumbnails_base, copy_media,
                  self.retroarch_path.get()),
            daemon=True,
        )
        self.worker_thread.start()

    def _run_migration_worker(self, logger, selected_systems, output_path,
                               thumbnails_base, copy_media, retroarch_path):
        def on_progress(msg):
            self.ui_queue.put(("log", msg))
        try:
            result = core.generate_metadata(
                self.playlists_path, output_path, logger,
                retroarch_path=retroarch_path,
                selected_systems=selected_systems,
                thumbnails_base_path=thumbnails_base,
                copy_media=copy_media,
                on_progress=on_progress,
                should_cancel=lambda: self.cancel_flag.is_set(),
            )
            self.ui_queue.put(("done", result))
        except Exception as e:
            self.ui_queue.put(("error", str(e)))

    def _cancel_migration(self):
        confirmed = self._ask(
            self._t("confirm_cancel_title"),
            self._t("confirm_cancel_msg", path=self._migration_output_path),
        )
        if confirmed:
            self.cancel_flag.set()
            self.btn_cancel.config(state="disabled")
            self._log(self._t("log_cancelled"))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.ui_queue.get_nowait()
                if kind == "log":
                    self._log(payload)
                elif kind == "done":
                    self._on_migration_done(payload)
                elif kind == "error":
                    self._on_migration_error(payload)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _on_migration_done(self, result):
        self.progress.stop()
        self.btn_start.config(state="normal")
        self.btn_cancel.config(state="disabled")
        self._on_theme_change()

        self._log("")
        self._log(self._t("log_done",
                           processed=result["processed"],
                           total_games=result["total_games"]))
        if result.get("media_copied") or result.get("media_errors"):
            self._log(self._t("log_media",
                               copied=result["media_copied"],
                               errors=result["media_errors"]))
        if result["skipped"]:
            self._log(self._t("log_skipped") + ", ".join(result["skipped"]))

        summary = self._t("dlg_done_msg",
                          processed=result["processed"],
                          total_games=result["total_games"])
        if result.get("media_copied") or result.get("media_errors"):
            summary += self._t("dlg_done_media",
                                copied=result["media_copied"],
                                errors=result["media_errors"])
        self._dialog("info", self._t("dlg_done_title"), summary)

    def _on_migration_error(self, error_msg):
        self.progress.stop()
        self.btn_start.config(state="normal")
        self.btn_cancel.config(state="disabled")
        self._on_theme_change()
        self._log(self._t("log_error", msg=error_msg))
        self._dialog("error", APP_TITLE, self._t("err_migration") + error_msg)

def run():
    app = RetroPegasusGUI()
    app.mainloop()


if __name__ == "__main__":
    run()
