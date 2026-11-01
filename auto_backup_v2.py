import base64
import ctypes
import hashlib
import json
import os
import shutil
import sys
import threading
import time
import uuid
import zipfile
from datetime import datetime, timezone
from ctypes import wintypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import winsound

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO


APP_TITLE = "Auto Backup v2"
APP_VERSION = "v2"
LOGO_BASE64 = """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"""
DEFAULT_INTERVAL_MIN = 5
DEFAULT_MAX_BACKUPS = 10
BUILT_IN_SOUNDS = ["01.wav", "02.wav", "03.wav", "04.wav", "05.wav"]
CUSTOM_SOUND_OPTION = "Custom WAV"

# Dark CustomTkinter-style palette.
COLOR_HEADER = "#000000"
COLOR_BODY = "#000000"
COLOR_SURFACE = "#000000"
COLOR_ENTRY_BG = "#000000"
COLOR_FG = "#C2C2C2"
COLOR_MUTED = "#A0A0A0"
COLOR_BORDER = "#3F3F3F"
COLOR_ACCENT = "#B92121"
COLOR_ACCENT_HOVER = "#F11C1C"
COLOR_BUTTON = "#000000"
COLOR_BUTTON_HOVER = "#363636"
COLOR_RING_TRACK = "#343638"
COLOR_STATUS_OK = "#026825"
COLOR_TEXT_LIGHT = "#DCE4EE"
FONT_LABEL = "Pixel Operator"
FONT_TIMER = "Advanced LED Board-7"
TEXT_TITLE = 26
TEXT_INFO = 20
TEXT_BUTTON = 22
TEXT_SECONDARY = 16
TIMER_STOPPED = 19
TIMER_RUNNING = 42
BUTTON_HEIGHT = 46
BUTTON_CORNER_RADIUS = 2
BUTTON_BACKGROUND = COLOR_BUTTON
BUTTON_HOVER_BACKGROUND = COLOR_BUTTON
BUTTON_TEXT_COLOR = COLOR_TEXT_LIGHT
BUTTON_HOVER_TEXT_COLOR = COLOR_MUTED
BUTTON_ACTIVE_TEXT_COLOR = COLOR_ACCENT
BUTTON_FONT_SIZE = TEXT_BUTTON + 8
BUTTON_FONT_WEIGHT = "bold"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AutoBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLOR_BODY)

        self.running = False
        self.toggle_button_hovered = False
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.manual_thread = None
        self.project_lock_path = None
        self.project_lock_identity = None

        # UI-only timing state. It mirrors the automatic loop; it does not control it.
        self.next_backup_deadline = None
        self.current_interval_seconds = DEFAULT_INTERVAL_MIN * 60
        self.backup_in_progress = False

        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL_MIN))
        self.max_backups_var = tk.StringVar(value=str(DEFAULT_MAX_BACKUPS))
        self.status_var = tk.StringVar(value="Stopped")

        self.load_application_fonts()

        self.workspace_path = self.load_workspace()
        self.projects = self.load_projects() if self.workspace_path else {}
        self.reset_backup_history()
        self.selected_project_name = None
        if self.workspace_path:
            self.dest_var.set(str(self.workspace_path))
        else:
            self.status_var.set("Workspace not configured")

        self.build_ui()
        self.tabview.configure(command=self.on_tab_changed)
        self.on_tab_changed("Backup")
        if self.workspace_path:
            self.refresh_project_controls()
        else:
            self.show_workspace_setup()

        self.source_var.trace_add("write", self.update_start_button_state)
        self.dest_var.trace_add("write", self.update_start_button_state)
        self.update_start_button_state()

        self.update_countdown()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_application_fonts(self):
        if os.name != "nt":
            return

        font_root = Path(__file__).resolve().parent / "assets" / "fonts"
        add_font = ctypes.windll.gdi32.AddFontResourceExW
        add_font.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
        add_font.restype = ctypes.c_int
        for font_name in ("PixelOperator.ttf", "advanced_led_board-7.ttf"):
            font_path = font_root / font_name
            if font_path.is_file():
                add_font(str(font_path), 0x10, None)

    def build_ui(self):
        # Overall composition: dark Corrosion Labs header, light working area.
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        logo_image = Image.open(
            Path(__file__).resolve().parent / "logo.png"
        ).convert("RGBA")
        self.header_logo = ctk.CTkImage(
            light_image=logo_image,
            dark_image=logo_image,
            size=(36, 36)
        )

        ctk.CTkLabel(
            header,
            image=self.header_logo,
            text=""
        ).grid(row=0, column=0, padx=(18, 10), pady=10)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            title_row,
            text="AUTO BACKUP v2",
            text_color=COLOR_TEXT_LIGHT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).pack(side="left")

        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color=COLOR_BODY,
            segmented_button_fg_color=COLOR_BUTTON,
            segmented_button_selected_color=COLOR_HEADER,
            segmented_button_selected_hover_color=COLOR_HEADER,
            segmented_button_unselected_color=COLOR_BUTTON,
            segmented_button_unselected_hover_color=COLOR_BUTTON_HOVER
        )
        self.tabview.grid(row=1, column=0, sticky="nsew")
        self.tabview.add("Backup")
        self.tabview.add("Settings")
        self.tabview.add("Storage")
        self.tabview.add("Storage")

        backup_tab = self.tabview.tab("Backup")
        backup_tab.grid_columnconfigure(0, weight=1)
        backup_tab.grid_rowconfigure(0, weight=1)
        backup_tab.grid_rowconfigure(1, weight=0)
        backup_tab.grid_rowconfigure(2, weight=0)
        backup_tab.grid_rowconfigure(1, weight=0)
        backup_tab.grid_rowconfigure(2, weight=0)

        body = ctk.CTkFrame(
            backup_tab,
            fg_color=COLOR_BODY,
            corner_radius=0
        )
        body.grid(row=0, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        actions_bar = ctk.CTkFrame(
            backup_tab,
            fg_color=COLOR_BODY,
            corner_radius=0,
            height=54
        )
        actions_bar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 10))
        actions_bar.grid_propagate(False)
        actions_bar.grid_columnconfigure((0, 1), weight=1)

        # LEFT COLUMN -------------------------------------------------------
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(14, 8), pady=(12, 10))
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left,
            text="Project",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        project_row = ctk.CTkFrame(left, fg_color="transparent")
        project_row.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        project_row.grid_columnconfigure(0, weight=1)

        self.project_var = tk.StringVar()
        self.project_combo = ctk.CTkComboBox(
            project_row,
            variable=self.project_var,
            values=[],
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            button_color=COLOR_BUTTON,
            button_hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON),
            command=self.select_project
        )
        self.project_combo.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.new_project_button = self._select_button(
            project_row, self.create_project
        )
        self.new_project_button.configure(text="New")
        self.new_project_button.grid(row=0, column=1, sticky="ew", padx=(0, 6))

        self.rename_project_button = self._select_button(
            project_row, self.rename_project
        )
        self.rename_project_button.configure(text="Rename")
        self.rename_project_button.grid(row=0, column=2, sticky="ew")

        self._field_label(left, "Source folder", 2)
        source_row = ctk.CTkFrame(left, fg_color="transparent")
        source_row.grid(row=3, column=0, sticky="ew", pady=(4, 8))
        source_row.grid_columnconfigure(0, weight=1)

        ctk.CTkEntry(
            source_row,
            textvariable=self.source_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self._select_button(source_row, self.select_source).grid(
            row=0, column=1, sticky="ew"
        )

        self._field_label(left, "Destination folder", 4)
        dest_row = ctk.CTkFrame(left, fg_color="transparent")
        dest_row.grid(row=5, column=0, sticky="ew", pady=(4, 8))
        dest_row.grid_columnconfigure(0, weight=1)

        ctk.CTkEntry(
            dest_row,
            textvariable=self.dest_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self._select_button(dest_row, self.select_dest).grid(
            row=0, column=1, sticky="ew"
        )

        options = ctk.CTkFrame(left, fg_color="transparent")
        options.grid(row=6, column=0, sticky="ew", pady=(2, 10))
        options.grid_columnconfigure((0, 1), weight=0)

        self._field_label(options, "Interval (minutes)", 0, column=0, padx=(0, 8))
        self._field_label(options, "Copies to keep", 0, column=1, padx=(8, 0))

        ctk.CTkEntry(
            options,
            textvariable=self.interval_var,
            width=190,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(4, 0))

        ctk.CTkEntry(
            options,
            textvariable=self.max_backups_var,
            width=190,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(4, 0))

        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=7, column=0, sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(
            actions,
            text="▶   Start",
            command=self.start_backup,
            height=46,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON, weight="bold"),
            state="disabled"
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_button = ctk.CTkButton(
            actions,
            text="Stop",
            command=self.stop_backup,
            height=46,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON),
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # RIGHT COLUMN ------------------------------------------------------
        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 14), pady=(6, 10))
        right.grid_columnconfigure(0, weight=1)

        self.timer_canvas = tk.Canvas(
            right,
            width=375,
            height=375,
            bg=COLOR_BODY,
            highlightthickness=0,
            bd=0
        )
        self.timer_canvas.grid(row=0, column=0, pady=(0, 6))

        # Anti-aliased circular progress ring.
        self.timer_ring_image_id = self.timer_canvas.create_image(
            0, 0, anchor="nw"
        )
        self.timer_ring_photo = None
        self.draw_timer_ring(0.0)

        self.timer_text = self.timer_canvas.create_text(
            188, 188,
            text="STOPPED",
            fill=COLOR_FG,
            font=(FONT_TIMER, TIMER_STOPPED, "bold"),
            anchor="center"
        )

        self.manual_button = ctk.CTkButton(
            right,
            text="Create now",
            command=self.create_manual_backup,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=BUTTON_BACKGROUND,
            hover_color=BUTTON_HOVER_BACKGROUND,
            text_color=BUTTON_TEXT_COLOR,
            font=ctk.CTkFont(
                family=FONT_LABEL,
                size=BUTTON_FONT_SIZE,
                weight=BUTTON_FONT_WEIGHT
            )
        )
        manual_button = self.manual_button
        manual_button.bind(
            "<Enter>",
            lambda event, button=manual_button: button.configure(
                text_color=BUTTON_HOVER_TEXT_COLOR
            )
        )
        manual_button.bind(
            "<Leave>",
            lambda event, button=manual_button: button.configure(
                text_color=BUTTON_TEXT_COLOR
            )
        )
        self.manual_button.grid(
            row=1, column=0, pady=(0, 7)
        )
        self.manual_button.configure(width=200)

        self.uninstall_button = ctk.CTkButton(
            right,
            text="Uninstall",
            command=self.uninstall,
            height=32,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.uninstall_button.grid(row=2, column=0, pady=(0, 2))

        # FOOTER ------------------------------------------------------------
        footer = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_ENTRY_BG,
            corner_radius=0,
            height=38
        )
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)

        self.status_dot = ctk.CTkLabel(
            footer,
            text="●",
            text_color=COLOR_MUTED,
            width=20,
            font=ctk.CTkFont(size=TEXT_SECONDARY)
        )
        self.status_dot.grid(row=0, column=0, sticky="w", padx=(14, 4), pady=7)

        ctk.CTkLabel(
            footer,
            textvariable=self.status_var,
            text_color=COLOR_MUTED,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).grid(row=0, column=0, sticky="w", padx=(38, 0), pady=7)

        ctk.CTkLabel(
            footer,
            text="CORROSION LABS",
            text_color=COLOR_MUTED,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=0, column=1, sticky="e", padx=(0, 14), pady=7)

        self.build_settings_tab(self.tabview.tab("Settings"))

    def build_settings_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        settings_card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SURFACE,
            corner_radius=8,
            border_width=0,
            border_color=COLOR_BORDER
        )
        settings_card.grid(row=1, column=0, sticky="new", padx=24, pady=0)
        settings_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            settings_card,
            text="Project sound notifications",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(16, 14))

        self.sound_enabled_var = tk.BooleanVar(value=True)
        self.sound_switch = ctk.CTkSwitch(
            settings_card,
            text="Enable sounds",
            variable=self.sound_enabled_var,
            command=self.on_sound_enabled_changed,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.sound_switch.grid(row=1, column=0, columnspan=3, sticky="w", padx=18, pady=(0, 18))

        ctk.CTkLabel(
            settings_card,
            text="Backup completed sound",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).grid(row=2, column=0, sticky="w", padx=(18, 10), pady=(0, 8))

        self.sound_var = tk.StringVar()
        self.sound_combo = ctk.CTkComboBox(
            settings_card,
            variable=self.sound_var,
            values=BUILT_IN_SOUNDS + [CUSTOM_SOUND_OPTION],
            command=self.on_sound_selected,
            height=38,
            corner_radius=6,
            border_width=0,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            button_color=COLOR_BUTTON,
            button_hover_color=COLOR_BUTTON_HOVER,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.sound_combo.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(0, 10),
            pady=(0, 8)
        )

        self.custom_sound_button = ctk.CTkButton(
            settings_card,
            text="Select WAV",
            command=self.select_custom_sound,
            height=36,
            width=110,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.custom_sound_button.grid(
            row=2,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=(0, 8)
        )

        self.custom_sound_var = tk.StringVar()
        ctk.CTkLabel(
            settings_card,
            textvariable=self.custom_sound_var,
            text_color=COLOR_MUTED,
            anchor="w",
            justify="left",
            wraplength=360,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=3, column=1, columnspan=3, sticky="ew", padx=(0, 18), pady=(0, 18))

        self.test_sound_button = ctk.CTkButton(
            settings_card,
            text="Test",
            command=self.test_selected_sound,
            height=38,
            width=110,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        )
        self.test_sound_button.grid(
            row=2,
            column=3,
            sticky="w",
            padx=(0, 18),
            pady=(0, 8)
        )

    def build_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=56
        )
        self.main_header = header
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        logo_image = Image.open(
            Path(__file__).resolve().parent / "logo.png"
        ).convert("RGBA")
        self.header_logo = ctk.CTkImage(
            light_image=logo_image,
            dark_image=logo_image,
            size=(36, 36)
        )
        ctk.CTkLabel(header, image=self.header_logo, text="").grid(
            row=0, column=0, padx=(18, 10), pady=10
        )

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(
            title_row,
            text="AUTO BACKUP v2",
            text_color=COLOR_TEXT_LIGHT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).pack(side="left")
        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color=COLOR_BODY,
            segmented_button_fg_color=COLOR_BUTTON,
            segmented_button_selected_color=COLOR_HEADER,
            segmented_button_selected_hover_color=COLOR_HEADER,
            segmented_button_unselected_color=COLOR_BUTTON,
            segmented_button_unselected_hover_color=COLOR_BUTTON_HOVER
        )
        self.tabview.grid(row=1, column=0, sticky="nsew")
        self.tabview.add("Backup")
        self.tabview.add("Settings")
        self.tabview.add("Storage")

        self.tabview.configure(fg_color=COLOR_BODY)
        self.tabview._segmented_button.grid_forget()
        header.grid_columnconfigure(2, weight=0)
        header_nav = ctk.CTkFrame(header, fg_color="transparent")
        header_nav.grid(row=0, column=2, sticky="e", padx=(12, 16))
        self.header_nav_buttons = {}
        for tab_name in ("Backup", "Settings", "Storage"):
            nav_button = ctk.CTkButton(
                header_nav,
                text=tab_name,
                command=lambda name=tab_name: self.tabview.set(name),
                width=98,
                height=36,
                corner_radius=5,
                fg_color="transparent",
                hover_color=COLOR_BUTTON_HOVER,
                text_color=COLOR_TEXT_LIGHT,
                font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
            )
            nav_button.pack(side="left", padx=2)
            self.header_nav_buttons[tab_name] = nav_button

        backup_tab = self.tabview.tab("Backup")
        backup_tab.grid_columnconfigure(0, weight=1)
        backup_tab.grid_rowconfigure(0, weight=1)

        backup_tab.configure(fg_color=COLOR_BODY)
        body = ctk.CTkFrame(backup_tab, fg_color=COLOR_BODY, corner_radius=0)
        body.grid(row=0, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1, uniform="backup_columns")
        body.grid_columnconfigure(1, weight=1, uniform="backup_columns")
        body.grid_rowconfigure(0, weight=1)

        actions_bar = ctk.CTkFrame(
            backup_tab,
            fg_color=COLOR_BODY,
            corner_radius=0,
            height=54
        )
        actions_bar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 10))
        actions_bar.grid_propagate(False)
        actions_bar.grid_columnconfigure((0, 1), weight=1)

        left = ctk.CTkFrame(body, fg_color=COLOR_SURFACE, corner_radius=2)
        left.grid(row=0, column=0, sticky="nsew", padx=(24, 10), pady=(24, 16))
        left.grid_columnconfigure(0, weight=1)

        self._field_label(left, "Project", 0)
        project_row = ctk.CTkFrame(left, fg_color="transparent")
        project_row.grid(row=1, column=0, sticky="ew", pady=(4, 16))
        project_row.grid_columnconfigure(1, weight=1)
        project_row.grid_rowconfigure(1, weight=0)
        self.project_var = tk.StringVar()
        self.project_selector_arrow = ctk.CTkButton(
            project_row,
            text="▼",
            command=self.toggle_project_selector,
            width=34,
            height=40,
            corner_radius=2,
            fg_color=COLOR_BODY,
            hover_color=COLOR_BUTTON_HOVER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY, weight="bold")
        )
        self.project_selector_arrow.grid(row=0, column=0, sticky="w")
        self.project_combo = ctk.CTkButton(
            project_row,
            text="",
            command=self.toggle_project_selector,
            height=40,
            corner_radius=2,
            fg_color=COLOR_BODY,
            hover_color=COLOR_BUTTON_HOVER,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON),
            width=266
        )
        self.project_combo.grid(row=0, column=1, sticky="ew")
        self.project_selector_menu = ctk.CTkScrollableFrame(
            project_row,
            width=1,
            height=150,
            fg_color=COLOR_SURFACE,
            corner_radius=2,
            scrollbar_button_color=COLOR_BUTTON,
            scrollbar_button_hover_color=COLOR_BUTTON_HOVER
        )
        self.project_selector_menu.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(2, 0)
        )
        self.project_selector_menu.grid_remove()
        self.project_selector_open = False
        self.toggle_button = ctk.CTkButton(
            actions_bar,
            text="START",
            command=self.toggle_backup,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=BUTTON_BACKGROUND,
            hover_color=BUTTON_HOVER_BACKGROUND,
            text_color=BUTTON_TEXT_COLOR,
            font=ctk.CTkFont(
                family=FONT_LABEL,
                size=BUTTON_FONT_SIZE,
                weight=BUTTON_FONT_WEIGHT
            ),
            state="disabled"
        )
        self.toggle_button.bind(
            "<Enter>",
            self.on_toggle_button_enter
        )
        self.toggle_button.bind(
            "<Leave>",
            self.on_toggle_button_leave
        )
        self.toggle_button.configure(width=300)
        self.toggle_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 24), pady=(6, 16))
        right.grid_columnconfigure(0, weight=1)

        self.timer_canvas = tk.Canvas(
            right,
            width=375,
            height=375,
            bg=COLOR_BODY,
            highlightthickness=0,
            bd=0
        )
        self.timer_canvas.grid(row=0, column=0, pady=(0, 6))
        self.timer_ring_image_id = self.timer_canvas.create_image(0, 0, anchor="nw")
        self.timer_ring_photo = None
        self.draw_timer_ring(0.0)
        self.timer_text = self.timer_canvas.create_text(
            188, 188,
            text="STOPPED",
            fill=COLOR_FG,
            font=(FONT_TIMER, TIMER_STOPPED, "bold"),
            anchor="center"
        )

        self.manual_button = ctk.CTkButton(
            actions_bar,
            text="Create now",
            command=self.create_manual_backup,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=BUTTON_BACKGROUND,
            hover_color=BUTTON_HOVER_BACKGROUND,
            text_color=BUTTON_TEXT_COLOR,
            font=ctk.CTkFont(
                family=FONT_LABEL,
                size=BUTTON_FONT_SIZE,
                weight=BUTTON_FONT_WEIGHT
            )
        )
        manual_button = self.manual_button
        manual_button.bind(
            "<Enter>",
            lambda event, button=manual_button: button.configure(
                text_color=BUTTON_HOVER_TEXT_COLOR
            )
        )
        manual_button.bind(
            "<Leave>",
            lambda event, button=manual_button: button.configure(
                text_color=BUTTON_TEXT_COLOR
            )
        )
        self.manual_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.manual_button.configure(width=300)

        status_bar = ctk.CTkFrame(
            backup_tab,
            fg_color=COLOR_ENTRY_BG,
            corner_radius=0,
            height=38
        )
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_propagate(False)
        status_bar.grid_columnconfigure(0, weight=1)
        self.status_dot = ctk.CTkLabel(
            status_bar,
            text="",
            text_color=COLOR_MUTED,
            width=20,
            font=ctk.CTkFont(size=TEXT_SECONDARY)
        )
        self.status_dot.grid(row=0, column=0, sticky="w", padx=(14, 4), pady=7)
        ctk.CTkLabel(
            status_bar,
            textvariable=self.status_var,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).grid(row=0, column=0, sticky="w", padx=(38, 0), pady=7)
        ctk.CTkLabel(
            status_bar,
            text="CORROSION LABS",
            text_color=COLOR_MUTED,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=0, column=1, sticky="e", padx=(0, 14), pady=7)

        settings_tab = self.tabview.tab("Settings")
        settings_tab.grid_columnconfigure(0, weight=1)
        settings_tab.grid_rowconfigure(0, weight=1)
        settings_scroll = ctk.CTkScrollableFrame(
            settings_tab,
            fg_color=COLOR_BODY
        )
        settings_scroll.grid(row=0, column=0, sticky="nsew")
        self.build_settings_tab(settings_scroll)
        self.build_project_settings_controls(settings_scroll)
        self.build_storage_tab(self.tabview.tab("Storage"))

    def build_project_settings_controls(self, parent):
        project_card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SURFACE,
            corner_radius=8,
            border_width=0,
            border_color=COLOR_BORDER
        )
        project_card.grid(row=0, column=0, sticky="new", padx=24, pady=0)
        project_card.grid_columnconfigure(0, weight=1)

        project_actions = ctk.CTkFrame(project_card, fg_color="transparent")
        project_actions.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 14))
        project_actions.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            project_actions,
            textvariable=self.project_var,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        self.new_project_button = self._select_button(
            project_actions, self.create_project
        )
        self.new_project_button.configure(text="New")
        self.new_project_button.grid(row=0, column=1, padx=(8, 6))

        self.rename_project_button = self._select_button(
            project_actions, self.rename_project
        )
        self.rename_project_button.configure(text="Rename")
        self.rename_project_button.grid(row=0, column=2)

        self._field_label(project_card, "Source folder", 1, padx=18)
        source_row = ctk.CTkFrame(project_card, fg_color="transparent")
        source_row.grid(row=2, column=0, sticky="ew", padx=18, pady=(4, 10))
        source_row.grid_columnconfigure(0, weight=1)
        ctk.CTkEntry(
            source_row,
            textvariable=self.source_var,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self._select_button(source_row, self.select_source).grid(row=0, column=1)

        dest_row = ctk.CTkFrame(project_card, fg_color="transparent")
        dest_row.grid(row=4, column=0, sticky="ew", padx=18, pady=(4, 10))
        dest_row.grid_columnconfigure(0, weight=1)
        self.open_backup_folder_button = ctk.CTkButton(
            dest_row,
            text="Open backup folder",
            command=self.open_backup_folder,
            height=40,
            width=220,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.open_backup_folder_button.grid(row=0, column=1, sticky="e")

        options = ctk.CTkFrame(dest_row, fg_color="transparent")
        options.grid(row=0, column=0, sticky="w")
        options.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self._field_label(options, "Interval (minutes)", 0, column=0, padx=(0, 8))
        self._field_label(options, "Copies to keep", 0, column=2, padx=(18, 8))
        ctk.CTkEntry(
            options,
            textvariable=self.interval_var,
            width=80,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=0, column=1, sticky="w")
        ctk.CTkEntry(
            options,
            textvariable=self.max_backups_var,
            width=80,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON)
        ).grid(row=0, column=3, sticky="w")

        self.uninstall_button = ctk.CTkButton(
            parent,
            text="Uninstall",
            command=self.uninstall,
            height=32,
            width=110,
            corner_radius=6,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            border_width=1,
            border_color=COLOR_ACCENT,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        self.uninstall_button.grid(row=3, column=0, sticky="e", padx=24, pady=0)

    def build_storage_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        space_card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SURFACE,
            corner_radius=8,
            border_width=4,
            border_color=COLOR_BORDER
        )
        space_card.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 14))
        space_card.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            space_card,
            text="Storage",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 10))

        self.storage_total_var = tk.StringVar(value="Total: —")
        self.storage_used_var = tk.StringVar(value="Used: —")
        self.storage_free_var = tk.StringVar(value="Free: —")
        for column, variable in enumerate((
            self.storage_total_var,
            self.storage_used_var,
            self.storage_free_var
        )):
            ctk.CTkLabel(
                space_card,
                textvariable=variable,
                text_color=COLOR_MUTED,
                anchor="w",
                font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
            ).grid(
                row=1,
                column=column,
                sticky="w",
                padx=(18 if column == 0 else 8, 8),
                pady=(0, 6)
            )

        self.storage_bar = ctk.CTkFrame(
            space_card,
            height=18,
            fg_color=COLOR_ENTRY_BG,
            corner_radius=2
        )
        self.storage_bar.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=18,
            pady=(4, 8)
        )
        self.storage_bar.grid_propagate(False)
        self.storage_other_segment = ctk.CTkFrame(
            self.storage_bar,
            fg_color=COLOR_MUTED,
            corner_radius=0
        )
        self.storage_backup_segment = ctk.CTkFrame(
            self.storage_bar,
            fg_color=COLOR_ACCENT,
            corner_radius=0
        )
        self.storage_free_segment = ctk.CTkFrame(
            self.storage_bar,
            fg_color=COLOR_STATUS_OK,
            corner_radius=0
        )

        legend = ctk.CTkFrame(space_card, fg_color="transparent")
        legend.grid(row=5, column=0, columnspan=3, sticky="w", padx=18, pady=(0, 14))
        for column, (color, text) in enumerate((
            (COLOR_MUTED, "Other files"),
            (COLOR_ACCENT, "Project backups"),
            (COLOR_STATUS_OK, "Free")
        )):
            ctk.CTkFrame(
                legend,
                width=10,
                height=10,
                fg_color=color,
                corner_radius=2
            ).grid(row=0, column=column * 2, padx=(0 if column == 0 else 14, 4))
            ctk.CTkLabel(
                legend,
                text=text,
                text_color=COLOR_MUTED,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
            ).grid(row=0, column=column * 2 + 1, padx=(0, 0))

        history_card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SURFACE,
            corner_radius=8,
            border_width=4,
            border_color=COLOR_BORDER
        )
        history_card.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 18))
        history_card.grid_columnconfigure(0, weight=1)
        history_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            history_card,
            text="Backup history",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 10))

        self.history_table = ctk.CTkScrollableFrame(
            history_card,
            fg_color=COLOR_BODY,
            corner_radius=2
        )
        self.history_table.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        for column, weight in enumerate((2, 1, 3, 1, 1, 1)):
            self.history_table.grid_columnconfigure(column, weight=weight)

        headings = ("Date", "Type", "ZIP", "Size", "Result", "Error")
        for column, heading in enumerate(headings):
            ctk.CTkLabel(
                self.history_table,
                text=heading,
                text_color=COLOR_FG,
                anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY, weight="bold")
            ).grid(row=0, column=column, sticky="ew", padx=6, pady=(6, 8))

    def on_tab_changed(self, tab_name=None):
        if hasattr(self, "header_nav_buttons"):
            selected_tab = self.tabview.get()
            for name, button in self.header_nav_buttons.items():
                button.configure(
                    fg_color=COLOR_HEADER if name == selected_tab else "transparent"
                )
        if tab_name == "Storage" or self.tabview.get() == "Storage":
            self.refresh_storage()

    @staticmethod
    def format_storage_size(size):
        units = ("B", "KB", "MB", "GB", "TB")
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:.1f} {unit}"
            value /= 1024

    def history_file_path(self, project_name=None):
        project_name = project_name or self.selected_project_name
        if not self.workspace_path or not project_name:
            return None
        return self.workspace_path / "app_data" / "history" / f"{project_name}.json"

    def reset_backup_history(self):
        if not self.workspace_path:
            return

        history_dir = self.workspace_path / "app_data" / "history"
        if not history_dir.is_dir():
            return

        for history_path in history_dir.glob("*.json"):
            try:
                with history_path.open("w", encoding="utf-8") as history_file:
                    json.dump([], history_file)
            except OSError:
                continue

    def load_project_history(self):
        history_path = self.history_file_path()
        if not history_path or not history_path.is_file():
            return []
        try:
            with history_path.open("r", encoding="utf-8") as history_file:
                history = json.load(history_file)
            if not isinstance(history, list):
                return []
            return sorted(
                history,
                key=lambda record: (
                    str(record.get("date", "")),
                    str(record.get("time", ""))
                ),
                reverse=True
            )
        except (OSError, json.JSONDecodeError):
            return []

    def record_history(self, backup_type, zip_name, size, result, error=""):
        history_path = self.history_file_path()
        if not history_path:
            return

        now = datetime.now()
        record = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "type": backup_type,
            "zip": zip_name or "",
            "size": int(size or 0),
            "result": result,
            "error": str(error or "")
        }
        history = self.load_project_history()
        history.insert(0, record)
        try:
            history_path.parent.mkdir(parents=True, exist_ok=True)
            with history_path.open("w", encoding="utf-8") as history_file:
                json.dump(history, history_file, indent=2, ensure_ascii=False)
        except OSError:
            return

        self.root.after(0, self.refresh_storage)

    def project_backup_size(self, project):
        if not self.workspace_path or not project:
            return 0

        project_path = self.workspace_path / project["name"]
        total_size = 0
        for folder_name in ("Auto", "Manual"):
            folder_path = project_path / folder_name
            if not folder_path.is_dir():
                continue
            for file_path in folder_path.rglob("*"):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except OSError:
                        continue
        return total_size

    def update_storage_bar(self, total, used, free):
        total = max(0, int(total))
        used = max(0, int(used))
        free = max(0, int(free))
        other = max(0, total - free - used)

        if total > 0:
            other_ratio = other / total
            used_ratio = used / total
            free_ratio = free / total
        else:
            other_ratio = used_ratio = free_ratio = 0

        self.storage_other_segment.place(
            relx=0,
            rely=0,
            relwidth=other_ratio,
            relheight=1
        )
        self.storage_backup_segment.place(
            relx=other_ratio,
            rely=0,
            relwidth=used_ratio,
            relheight=1
        )
        self.storage_free_segment.place(
            relx=other_ratio + used_ratio,
            rely=0,
            relwidth=free_ratio,
            relheight=1
        )

    def refresh_storage(self):
        if not hasattr(self, "history_table"):
            return

        project = self.get_selected_project_settings()
        project_name = project["name"] if project else "No project selected"
        total = 0
        project_used = 0
        free = 0
        if self.workspace_path and self.workspace_path.exists():
            try:
                total, _, free = shutil.disk_usage(self.workspace_path)
                project_used = self.project_backup_size(project)
                self.storage_total_var.set(f"Total: {self.format_storage_size(total)}")
                self.storage_used_var.set(
                    f"Used: {self.format_storage_size(project_used)}"
                )
                self.storage_free_var.set(f"Free: {self.format_storage_size(free)}")
            except OSError:
                self.storage_total_var.set("Total: —")
                self.storage_used_var.set("Used: —")
                self.storage_free_var.set("Free: —")
        else:
            self.storage_total_var.set("Total: —")
            self.storage_used_var.set("Used: —")
            self.storage_free_var.set("Free: —")

        self.update_storage_bar(total, project_used, free)

        for child in self.history_table.winfo_children():
            if int(child.grid_info().get("row", 0)) > 0:
                child.destroy()

        if not project:
            return

        for row, record in enumerate(self.load_project_history(), start=1):
            values = (
                f"{record.get('date', '')} {record.get('time', '')}",
                record.get("type", ""),
                record.get("zip", ""),
                self.format_storage_size(record.get("size", 0)),
                record.get("result", ""),
                record.get("error", "")
            )
            for column, value in enumerate(values):
                text_color = COLOR_STATUS_OK if column == 4 and value == "OK" else COLOR_FG
                if column == 4 and value == "Error":
                    text_color = COLOR_ACCENT
                ctk.CTkLabel(
                    self.history_table,
                    text=str(value),
                    text_color=text_color,
                    anchor="w",
                    justify="left",
                    wraplength=220 if column in (2, 5) else 120,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
                ).grid(row=row, column=column, sticky="ew", padx=6, pady=4)

    def _field_label(self, parent, text, row, column=0, padx=0):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).grid(row=row, column=column, sticky="w", padx=padx)

    def _select_button(self, parent, command):
        return ctk.CTkButton(
            parent,
            text="Select",
            command=command,
            width=110,
            height=40,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )

    def draw_timer_ring(self, progress):
        progress = max(0.0, min(1.0, progress))

        size = 375
        scale = 4
        high_size = size * scale
        inset = 41 * scale
        width = 40 * scale

        image = Image.new("RGBA", (high_size, high_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        box = (inset, inset, high_size - inset, high_size - inset)

        draw.ellipse(
            box,
            outline=COLOR_RING_TRACK,
            width=width
        )

        if progress > 0:
            draw.arc(
                box,
                start=-90,
                end=-90 + (360 * progress),
                fill=COLOR_ACCENT,
                width=width
            )

        image = image.resize((size, size), Image.Resampling.LANCZOS)
        self.timer_ring_photo = ImageTk.PhotoImage(image)
        self.timer_canvas.itemconfigure(
            self.timer_ring_image_id,
            image=self.timer_ring_photo
        )

    def update_countdown(self):
        if not self.running:
            text = "STOPPED"
            ring_progress = 0.0
            timer_font = (FONT_TIMER, TIMER_STOPPED, "bold")
        elif self.backup_in_progress or self.next_backup_deadline is None:
            text = "BACKUP"
            ring_progress = 1.0
            timer_font = (FONT_TIMER, TIMER_STOPPED, "bold")
        else:
            remaining = max(0.0, self.next_backup_deadline - time.monotonic())
            total = max(1.0, self.current_interval_seconds)

            elapsed_progress = 1.0 - min(1.0, remaining / total)

            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            text = f"{minutes:02d}:{seconds:02d}"
            ring_progress = elapsed_progress
            timer_font = (FONT_TIMER, TIMER_RUNNING, "normal")

        self.draw_timer_ring(ring_progress)
        self.timer_canvas.itemconfigure(
            self.timer_text,
            text=text,
            font=timer_font
        )
        self.root.after(250, self.update_countdown)

    def update_start_button_state(self, *_):
        source_ok = bool(self.source_var.get().strip())
        project_ok = bool(
            self.selected_project_name
            and self.selected_project_name in self.projects
        )
        dest_ok = bool(
            project_ok
            and (self.workspace_path / self.selected_project_name).is_dir()
        )
        ready_to_start = source_ok and dest_ok and not self.project_operations_locked()

        if self.running:
            self.toggle_button.configure(
                text="STOP",
                command=self.stop_backup,
                state="normal",
                fg_color=BUTTON_BACKGROUND,
                hover_color=BUTTON_HOVER_BACKGROUND,
                text_color=BUTTON_ACTIVE_TEXT_COLOR,
                border_width=0
            )
        elif self.worker_thread and self.worker_thread.is_alive():
            self.toggle_button.configure(
                text="STOP",
                command=self.stop_backup,
                state="disabled",
                fg_color=BUTTON_BACKGROUND,
                hover_color=BUTTON_HOVER_BACKGROUND,
                text_color=BUTTON_ACTIVE_TEXT_COLOR,
                border_width=0
            )
        else:
            self.toggle_button.configure(
                text="START",
                command=self.start_backup,
                state="normal" if ready_to_start else "disabled",
                fg_color=BUTTON_BACKGROUND,
                hover_color=BUTTON_HOVER_BACKGROUND,
                text_color=BUTTON_TEXT_COLOR if ready_to_start else COLOR_MUTED,
                border_width=0 if ready_to_start else 1
            )

        if (
            self.toggle_button_hovered
            and self.toggle_button.cget("state") != "disabled"
        ):
            self.toggle_button.configure(text_color=BUTTON_HOVER_TEXT_COLOR)

        self.update_project_controls_state()

    def on_toggle_button_enter(self, _event=None):
        self.toggle_button_hovered = True
        if self.toggle_button.cget("state") != "disabled":
            self.toggle_button.configure(text_color=BUTTON_HOVER_TEXT_COLOR)

    def on_toggle_button_leave(self, _event=None):
        self.toggle_button_hovered = False
        self.update_start_button_state()

    def select_source(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta de origen")
        if path:
            self.source_var.set(path)

    def select_dest(self):
        if self.selected_project_name:
            self.dest_var.set(
                str(self.workspace_path / self.selected_project_name)
            )
        elif self.workspace_path:
            self.dest_var.set(str(self.workspace_path))

    @staticmethod
    def settings_path():
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "AutoBackup" / "settings.json"
        return Path.home() / "AppData" / "Local" / "AutoBackup" / "settings.json"

    def load_workspace_legacy(self):
        settings_path = self.settings_path()

        if settings_path.is_file():
            try:
                with settings_path.open("r", encoding="utf-8") as settings_file:
                    settings = json.load(settings_file)
                workspace_value = settings.get("workspace")
                if workspace_value:
                    workspace = Path(workspace_value).expanduser().resolve()
                    if workspace.is_dir():
                        return workspace

                    messagebox.showwarning(
                        APP_TITLE,
                        "La carpeta central configurada ya no existe. "
                        "Selecciona una nueva ubicación."
                    )
            except (OSError, json.JSONDecodeError, AttributeError, TypeError):
                messagebox.showwarning(
                    APP_TITLE,
                    "No se pudo leer la configuración de la carpeta central. "
                    "Selecciona una nueva ubicación."
                )

            return self.select_workspace()

        if not self.show_initial_setup_dialog():
            return None

        return self.select_workspace()

    def load_workspace(self):
        settings_path = self.settings_path()
        self.workspace_setup_message = (
            "Configura una carpeta central para guardar los proyectos y copias."
        )
        if not settings_path.is_file():
            return None

        try:
            with settings_path.open("r", encoding="utf-8") as settings_file:
                settings = json.load(settings_file)
            workspace_value = settings.get("workspace")
            if workspace_value:
                workspace = Path(workspace_value).expanduser().resolve()
                if workspace.is_dir():
                    return workspace
                self.workspace_setup_message = (
                    "La carpeta central configurada ya no existe. "
                    "Introduce una nueva ubicación."
                )
        except (OSError, json.JSONDecodeError, AttributeError, TypeError):
            self.workspace_setup_message = (
                "No se pudo leer la configuración de la carpeta central. "
                "Introduce una nueva ubicación."
            )
        return None

    def show_initial_setup_dialog(self):
        result = {"continue": False}
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Initial setup")
        dialog.geometry("540x300")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLOR_BODY)
        dialog.transient(self.root)
        dialog.grab_set()

        header = ctk.CTkFrame(
            dialog,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=54
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Initial setup",
            text_color=COLOR_TEXT_LIGHT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).pack(fill="both", padx=20)

        ctk.CTkLabel(
            dialog,
            text=(
                "Auto Backup needs a central folder to store your project backups "
                "and future configurations.\n\n"
                "Choose a location with enough free space. The folder will be "
                "remembered, so you won't need to select it again."
            ),
            text_color=COLOR_FG,
            justify="left",
            anchor="w",
            wraplength=480,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(fill="both", expand=True, padx=24, pady=(24, 18))

        actions = ctk.CTkFrame(dialog, fg_color="transparent")
        actions.pack(fill="x", padx=24, pady=(0, 20))
        actions.grid_columnconfigure((0, 1), weight=1)

        def cancel():
            dialog.grab_release()
            dialog.destroy()

        def continue_setup():
            result["continue"] = True
            dialog.grab_release()
            dialog.destroy()

        ctk.CTkButton(
            actions,
            text="Continue",
            command=continue_setup,
            height=38,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="Cancel",
            command=cancel,
            height=38,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", cancel)
        dialog.wait_window()
        return result["continue"]

    def show_workspace_setup(self):
        if hasattr(self, "main_header"):
            self.main_header.grid_forget()
        if hasattr(self, "tabview"):
            self.tabview.grid_forget()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.workspace_setup_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_BODY,
            corner_radius=0
        )
        self.workspace_setup_frame.grid(row=0, column=0, sticky="nsew", padx=48, pady=42)
        self.workspace_setup_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.workspace_setup_frame,
            text="CONFIGURACIÓN INICIAL",
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(20, 8))
        ctk.CTkLabel(
            self.workspace_setup_frame,
            text="Introduce la carpeta central donde se guardarán los proyectos y copias.",
            text_color=COLOR_MUTED,
            anchor="w",
            justify="left",
            wraplength=560,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).grid(row=1, column=0, sticky="ew", pady=(0, 16))

        self.workspace_setup_path_var = tk.StringVar()
        self.workspace_setup_error_var = tk.StringVar(
            value=getattr(self, "workspace_setup_message", "")
        )
        self.workspace_setup_location_var = tk.StringVar(
            value="Ubicación elegida: —"
        )
        self.workspace_setup_create_var = tk.BooleanVar(value=False)

        path_row = ctk.CTkFrame(
            self.workspace_setup_frame,
            fg_color="transparent"
        )
        path_row.grid(row=2, column=0, sticky="ew")
        path_row.grid_columnconfigure(0, weight=1)
        path_entry = ctk.CTkEntry(
            path_row,
            textvariable=self.workspace_setup_path_var,
            height=38,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(
            path_row,
            text="Seleccionar carpeta",
            command=self.select_workspace_folder,
            height=38,
            width=150,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=0, column=1, sticky="e")
        self.workspace_setup_path_var.trace_add(
            "write",
            lambda *_: self.workspace_setup_location_var.set(
                f"Ubicación elegida: {self.workspace_setup_path_var.get().strip() or '—'}"
            )
        )
        ctk.CTkLabel(
            self.workspace_setup_frame,
            textvariable=self.workspace_setup_location_var,
            text_color=COLOR_MUTED,
            anchor="w",
            justify="left",
            wraplength=560,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=3, column=0, sticky="ew", pady=(8, 10))
        ctk.CTkCheckBox(
            self.workspace_setup_frame,
            text="Confirmo que se puede crear la carpeta si no existe",
            variable=self.workspace_setup_create_var,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=4, column=0, sticky="w", pady=(0, 8))
        ctk.CTkLabel(
            self.workspace_setup_frame,
            textvariable=self.workspace_setup_error_var,
            text_color=COLOR_ACCENT,
            anchor="w",
            justify="left",
            wraplength=560,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).grid(row=5, column=0, sticky="ew", pady=(0, 12))
        ctk.CTkButton(
            self.workspace_setup_frame,
            text="Confirmar",
            command=self.confirm_workspace_setup,
            height=40,
            corner_radius=6,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).grid(row=6, column=0, sticky="ew")
        path_entry.focus_force()

    def select_workspace_folder(self):
        path = filedialog.askdirectory(
            parent=self.root,
            title="Seleccionar carpeta central de Auto Backup"
        )
        if path:
            self.workspace_setup_path_var.set(path)
            self.workspace_setup_error_var.set("")

    def confirm_workspace_setup(self):
        raw_path = self.workspace_setup_path_var.get().strip()
        if not raw_path:
            self.workspace_setup_error_var.set(
                "Introduce una ruta para la carpeta central."
            )
            return

        workspace = Path(raw_path).expanduser().resolve()
        if workspace.exists() and not workspace.is_dir():
            self.workspace_setup_error_var.set(
                "La ubicación indicada no es una carpeta válida."
            )
            return

        if not workspace.exists():
            if not self.workspace_setup_create_var.get():
                self.workspace_setup_error_var.set(
                    "Activa la confirmación para crear la carpeta si no existe."
                )
                return
            try:
                workspace.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                self.workspace_setup_error_var.set(
                    f"No se pudo crear la carpeta central: {exc}"
                )
                return

        if not workspace.is_dir():
            self.workspace_setup_error_var.set(
                "La ubicación indicada no es una carpeta válida."
            )
            return

        settings_path = self.settings_path()
        try:
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            with settings_path.open("w", encoding="utf-8") as settings_file:
                json.dump(
                    {"workspace": str(workspace)},
                    settings_file,
                    indent=2,
                    ensure_ascii=False
                )
        except OSError as exc:
            self.workspace_setup_error_var.set(
                f"No se pudo guardar la configuración: {exc}"
            )
            return

        self.workspace_path = workspace
        self.projects = self.load_projects()
        self.dest_var.set(str(workspace))
        self.status_var.set("Stopped")
        self.workspace_setup_frame.grid_forget()
        if hasattr(self, "main_header"):
            self.main_header.grid(row=0, column=0, sticky="ew")
        if hasattr(self, "tabview"):
            self.tabview.grid(row=1, column=0, sticky="nsew")
        self.refresh_project_controls()
        self.update_start_button_state()

    def select_workspace(self):
        while True:
            result = {"path": None, "confirmed": False}
            dialog = ctk.CTkToplevel(self.root)
            dialog.title("Carpeta central")
            dialog.geometry("560x250")
            dialog.resizable(False, False)
            dialog.configure(fg_color=COLOR_BODY)
            dialog.transient(self.root)
            dialog.grab_set()

            ctk.CTkLabel(
                dialog,
                text="Ubicación de la carpeta central",
                text_color=COLOR_FG,
                anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
            ).pack(fill="x", padx=24, pady=(22, 8))

            ctk.CTkLabel(
                dialog,
                text="Introduce la ruta donde se guardarán los proyectos y copias.",
                text_color=COLOR_MUTED,
                anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
            ).pack(fill="x", padx=24, pady=(0, 8))

            path_var = tk.StringVar()
            path_entry = ctk.CTkEntry(
                dialog,
                textvariable=path_var,
                height=38,
                corner_radius=6,
                border_width=1,
                border_color=COLOR_BORDER,
                fg_color=COLOR_ENTRY_BG,
                text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
            )
            path_entry.pack(fill="x", padx=24)

            location_var = tk.StringVar(value="Ubicación elegida: —")
            ctk.CTkLabel(
                dialog,
                textvariable=location_var,
                text_color=COLOR_MUTED,
                anchor="w",
                justify="left",
                wraplength=510,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
            ).pack(fill="x", padx=24, pady=(8, 12))

            def update_location(*_):
                value = path_var.get().strip()
                location_var.set(f"Ubicación elegida: {value or '—'}")

            def cancel():
                dialog.grab_release()
                dialog.destroy()

            def confirm():
                value = path_var.get().strip()
                if not value:
                    messagebox.showerror(
                        APP_TITLE,
                        "Introduce una ruta para la carpeta central.",
                        parent=dialog
                    )
                    return
                result["path"] = value
                result["confirmed"] = True
                dialog.grab_release()
                dialog.destroy()

            path_var.trace_add("write", update_location)
            actions = ctk.CTkFrame(dialog, fg_color="transparent")
            actions.pack(fill="x", padx=24, pady=(0, 18))
            actions.grid_columnconfigure((0, 1), weight=1)
            ctk.CTkButton(
                actions,
                text="Cancelar",
                command=cancel,
                height=36,
                corner_radius=6,
                fg_color=COLOR_BUTTON,
                hover_color=COLOR_BUTTON_HOVER,
                border_width=1,
                border_color=COLOR_BORDER,
                text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
            ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
            ctk.CTkButton(
                actions,
                text="Confirmar",
                command=confirm,
                height=36,
                corner_radius=6,
                fg_color=COLOR_ACCENT,
                hover_color=COLOR_ACCENT_HOVER,
                text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
            ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

            dialog.protocol("WM_DELETE_WINDOW", cancel)
            path_entry.focus_force()
            dialog.wait_window()

            if not result["confirmed"]:
                return None

            workspace = Path(result["path"]).expanduser().resolve()
            if not workspace.exists():
                create_workspace = messagebox.askyesno(
                    APP_TITLE,
                    f"La carpeta no existe. ¿Quieres crearla?\n\n{workspace}"
                )
                if not create_workspace:
                    continue
                try:
                    workspace.mkdir(parents=True, exist_ok=True)
                except OSError as exc:
                    messagebox.showerror(
                        APP_TITLE,
                        f"No se pudo crear la carpeta central:\n{exc}"
                    )
                    continue

            if not workspace.is_dir():
                messagebox.showerror(
                    APP_TITLE,
                    "La ubicación seleccionada no es una carpeta válida."
                )
                continue

            settings_path = self.settings_path()
            try:
                settings_path.parent.mkdir(parents=True, exist_ok=True)
                with settings_path.open("w", encoding="utf-8") as settings_file:
                    json.dump(
                        {"workspace": str(workspace)},
                        settings_file,
                        indent=2,
                        ensure_ascii=False
                    )
            except OSError as exc:
                messagebox.showerror(
                    APP_TITLE,
                    f"No se pudo guardar la configuración:\n{exc}"
                )
                return None

            return workspace

    def projects_path(self):
        return self.workspace_path / "app_data" / "projects.json"

    def load_projects(self):
        projects_path = self.projects_path()
        projects = {}
        missing_projects = []

        if projects_path.is_file():
            try:
                with projects_path.open("r", encoding="utf-8") as projects_file:
                    data = json.load(projects_file)
                records = data.get("projects", [])
                for record in records:
                    if not isinstance(record, dict):
                        continue
                    name = str(record.get("name", "")).strip()
                    source = str(record.get("source", "")).strip()
                    if not self.is_valid_project_name(name):
                        continue
                    if any(existing.lower() == name.lower() for existing in projects):
                        continue

                    project_path = (self.workspace_path / name).resolve()
                    if project_path.parent != self.workspace_path.resolve() or not project_path.is_dir():
                        missing_projects.append(name)
                        continue

                    project_path.joinpath("Auto").mkdir(exist_ok=True)
                    project_path.joinpath("Manual").mkdir(exist_ok=True)
                    sound_enabled = record.get("sound_enabled", True)
                    success_sound = record.get("success_sound", "01.wav")
                    custom_sound = record.get("custom_sound", "")
                    if success_sound not in BUILT_IN_SOUNDS and success_sound != CUSTOM_SOUND_OPTION:
                        success_sound = "01.wav"
                    projects[name] = {
                        "name": name,
                        "source": source,
                        "interval": record.get("interval", DEFAULT_INTERVAL_MIN),
                        "max_backups": record.get("max_backups", DEFAULT_MAX_BACKUPS),
                        "sound_enabled": bool(sound_enabled),
                        "success_sound": success_sound,
                        "custom_sound": str(custom_sound or "")
                    }
            except (OSError, json.JSONDecodeError, AttributeError, TypeError):
                messagebox.showwarning(
                    APP_TITLE,
                    "No se pudo leer la configuración de proyectos. "
                    "Se iniciará con una lista vacía."
                )

        if missing_projects:
            messagebox.showwarning(
                APP_TITLE,
                "Faltan las carpetas de estos proyectos y se eliminarán de la "
                f"configuración:\n\n{', '.join(missing_projects)}"
            )

        self.projects = projects
        self.save_projects()
        return projects

    def save_projects(self):
        if not self.workspace_path:
            return

        projects_path = self.projects_path()
        projects_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"projects": list(self.projects.values())}
        with projects_path.open("w", encoding="utf-8") as projects_file:
            json.dump(data, projects_file, indent=2, ensure_ascii=False)

    @staticmethod
    def is_valid_project_name(name):
        name = name.strip()
        if not name or name in {".", ".."} or name[-1] in ". ":
            return False
        if any(ord(char) < 32 for char in name):
            return False
        if any(char in '<>:"/\\|?*' for char in name):
            return False

        reserved = {"CON", "PRN", "AUX", "NUL"}
        reserved.update(f"COM{index}" for index in range(1, 10))
        reserved.update(f"LPT{index}" for index in range(1, 10))
        return name.split(".", 1)[0].upper() not in reserved

    def toggle_project_selector(self):
        if self.project_operations_locked():
            return
        if self.project_selector_open:
            self.project_selector_menu.grid_remove()
            self.project_selector_open = False
        else:
            self.project_selector_menu.grid()
            self.project_selector_open = True

    def open_project_selector_window(self):
        if self.project_operations_locked():
            return
        if hasattr(self, "project_selector_window") and self.project_selector_window.winfo_exists():
            self.project_selector_window.lift()
            return

        self.project_selector_window = ctk.CTkToplevel(self.root)
        self.project_selector_window.title("Seleccionar proyecto")
        self.project_selector_window.geometry("360x420")
        self.project_selector_window.resizable(False, False)
        self.project_selector_window.configure(fg_color=COLOR_BODY)
        self.project_selector_window.transient(self.root)
        self.project_selector_window.grab_set()

        ctk.CTkLabel(
            self.project_selector_window,
            text="PROYECTOS",
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).pack(fill="x", padx=18, pady=(18, 10))

        project_list = ctk.CTkScrollableFrame(
            self.project_selector_window,
            fg_color=COLOR_SURFACE,
            corner_radius=2,
            scrollbar_button_color=COLOR_BUTTON,
            scrollbar_button_hover_color=COLOR_BUTTON_HOVER
        )
        project_list.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        for project_name in self.projects:
            ctk.CTkButton(
                project_list,
                text=project_name,
                command=lambda name=project_name: self.select_project_from_window(name),
                height=38,
                corner_radius=2,
                fg_color=COLOR_SURFACE,
                hover_color=COLOR_BUTTON_HOVER,
                text_color=COLOR_FG,
                anchor="w",
                font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
            ).pack(fill="x", padx=4, pady=3)

        ctk.CTkButton(
            self.project_selector_window,
            text="Cancelar",
            command=self.close_project_selector_window,
            height=36,
            corner_radius=2,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(fill="x", padx=18, pady=(0, 18))
        self.project_selector_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_project_selector_window
        )

    def close_project_selector_window(self):
        if hasattr(self, "project_selector_window") and self.project_selector_window.winfo_exists():
            self.project_selector_window.grab_release()
            self.project_selector_window.destroy()

    def select_project_from_window(self, project_name):
        self.select_project(project_name)
        self.close_project_selector_window()

    def refresh_project_controls(self):
        if not hasattr(self, "project_combo"):
            return

        names = list(self.projects.keys())
        self.project_selector_menu.grid_remove()
        self.project_selector_open = False
        for child in self.project_selector_menu.winfo_children():
            child.destroy()
        for name in names:
            ctk.CTkButton(
                self.project_selector_menu,
                text=name,
                command=lambda project_name=name: self.select_project_from_menu(project_name),
                height=34,
                corner_radius=0,
                fg_color=COLOR_SURFACE,
                hover_color=COLOR_BUTTON_HOVER,
                text_color=COLOR_FG,
                anchor="w",
                font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
            ).pack(fill="x", padx=4, pady=2)
        if self.selected_project_name in self.projects:
            self.project_var.set(self.selected_project_name)
            self.project_combo.configure(text=self.selected_project_name)
        elif names:
            self.select_project(names[0])
        else:
            self.project_var.set("")
            self.selected_project_name = None
            self.project_combo.configure(text="")

        self.update_project_controls_state()

    def select_project_from_menu(self, project_name):
        self.project_selector_menu.grid_remove()
        self.project_selector_open = False
        self.project_var.set(project_name)
        self.select_project(project_name)

    def update_project_controls_state(self):
        locked = self.project_operations_locked()
        manual_backup_running = bool(
            self.manual_thread and self.manual_thread.is_alive()
        )
        self.project_combo.configure(state="disabled" if locked else "normal")
        self.project_selector_arrow.configure(state="disabled" if locked else "normal")
        if locked:
            self.project_selector_menu.grid_remove()
            self.project_selector_open = False
        self.new_project_button.configure(state="disabled" if locked else "normal")
        self.rename_project_button.configure(
            state="disabled" if locked or not self.selected_project_name else "normal"
        )
        self.manual_button.configure(
            state="disabled" if manual_backup_running else "normal"
        )
        self.uninstall_button.configure(state="disabled" if locked else "normal")
        self.update_sound_controls_state()

    def project_operations_locked(self):
        return (
            self.running
            or self.backup_in_progress
            or bool(self.worker_thread and self.worker_thread.is_alive())
            or bool(self.manual_thread and self.manual_thread.is_alive())
        )

    def select_project(self, project_name=None):
        if self.project_operations_locked():
            return

        self.save_current_project_settings()
        project_name = project_name or self.project_var.get().strip()
        project = self.projects.get(project_name)
        if not project:
            return

        self.selected_project_name = project_name
        self.project_var.set(project_name)
        self.project_combo.configure(text=project_name)
        self.source_var.set(project["source"])
        self.interval_var.set(str(project["interval"]))
        self.max_backups_var.set(str(project["max_backups"]))
        self.dest_var.set(str(self.workspace_path / project_name))
        self.load_sound_settings(project)
        self.update_sound_controls_state()
        self.refresh_storage()

    def save_current_project_settings(self):
        if not self.selected_project_name:
            return

        project = self.projects.get(self.selected_project_name)
        if not project:
            return

        source = self.source_var.get().strip()
        try:
            interval = float(self.interval_var.get())
            max_backups = int(self.max_backups_var.get())
        except ValueError:
            return

        if not source or interval <= 0 or max_backups <= 0:
            return

        project["source"] = str(Path(source).expanduser().resolve())
        project["interval"] = interval
        project["max_backups"] = max_backups
        if hasattr(self, "sound_enabled_var"):
            project["sound_enabled"] = bool(self.sound_enabled_var.get())
            project["success_sound"] = self.sound_var.get() or "01.wav"
            project["custom_sound"] = self.custom_sound_var.get()
        self.save_projects()

    def load_sound_settings(self, project):
        if not hasattr(self, "sound_enabled_var"):
            return

        sound_enabled = bool(project.get("sound_enabled", True))
        success_sound = project.get("success_sound", "01.wav")
        custom_sound = project.get("custom_sound", "")
        if success_sound not in BUILT_IN_SOUNDS and success_sound != CUSTOM_SOUND_OPTION:
            success_sound = "01.wav"

        self.sound_enabled_var.set(sound_enabled)
        self.sound_var.set(success_sound)
        self.custom_sound_var.set(custom_sound)
    def update_sound_controls_state(self):
        if not hasattr(self, "sound_switch"):
            return

        enabled = bool(self.selected_project_name in self.projects)
        state = "normal" if enabled else "disabled"
        self.sound_switch.configure(state=state)
        self.sound_combo.configure(state=state)
        self.custom_sound_button.configure(state=state)
        self.test_sound_button.configure(state=state)

    def on_sound_enabled_changed(self):
        self.save_current_project_settings()

    def on_sound_selected(self, sound_name):
        if sound_name == CUSTOM_SOUND_OPTION:
            if not self.custom_sound_var.get():
                self.select_custom_sound()
            else:
                self.save_current_project_settings()
            return

        self.save_current_project_settings()

    def select_custom_sound(self):
        if not self.selected_project_name:
            return

        path = filedialog.askopenfilename(
            title="Select custom WAV sound",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if not path:
            if not self.custom_sound_var.get():
                self.sound_var.set("01.wav")
            return

        self.custom_sound_var.set(str(Path(path).resolve()))
        self.sound_var.set(CUSTOM_SOUND_OPTION)
        self.save_current_project_settings()

    def open_backup_folder(self):
        if not self.workspace_path or not self.selected_project_name:
            return

        project_path = self.workspace_path / self.selected_project_name
        if project_path.is_dir():
            os.startfile(str(project_path))

    def integrated_sound_path(self, sound_name):
        resource_root = Path(
            getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
        )
        return resource_root / "assets" / "Audios" / sound_name

    def selected_sound_path(self, project):
        sound_name = project.get("success_sound", "01.wav")
        if sound_name == CUSTOM_SOUND_OPTION:
            custom_path = Path(project.get("custom_sound", ""))
            if custom_path.is_file():
                return custom_path
            return self.integrated_sound_path("01.wav")

        if sound_name not in BUILT_IN_SOUNDS:
            sound_name = "01.wav"
        return self.integrated_sound_path(sound_name)

    def get_selected_project_settings(self):
        if not self.selected_project_name:
            return None
        return self.projects.get(self.selected_project_name)

    def play_success_sound(self):
        project = self.get_selected_project_settings()
        if not project or not project.get("sound_enabled", True):
            return
        sound_path = self.selected_sound_path(project)
        self.play_wav_async(sound_path)

    def play_error_sound(self):
        project = self.get_selected_project_settings()
        if not project or not project.get("sound_enabled", True):
            return
        threading.Thread(
            target=lambda: winsound.MessageBeep(winsound.MB_ICONHAND),
            daemon=True
        ).start()

    @staticmethod
    def play_wav_async(sound_path):
        if not Path(sound_path).is_file():
            return

        threading.Thread(
            target=lambda: winsound.PlaySound(
                str(sound_path),
                winsound.SND_FILENAME | winsound.SND_ASYNC
            ),
            daemon=True
        ).start()

    def test_selected_sound(self):
        project = self.get_selected_project_settings()
        if not project or not project.get("sound_enabled", True):
            return
        self.play_wav_async(self.selected_sound_path(project))

    def prompt_project_name(self, title, prompt, initial_value=""):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("420x190")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLOR_BODY)
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text=prompt,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(fill="x", padx=24, pady=(24, 8))

        name_var = tk.StringVar(value=initial_value)
        name_entry = ctk.CTkEntry(
            dialog,
            textvariable=name_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        )
        name_entry.pack(fill="x", padx=24)

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(18, 20))

        result = {"value": None}

        def confirm():
            result["value"] = name_var.get()
            dialog.destroy()

        def cancel():
            dialog.destroy()

        ctk.CTkButton(
            buttons,
            text="OK",
            command=confirm,
            width=100,
            height=36,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(side="right")
        ctk.CTkButton(
            buttons,
            text="Cancel",
            command=cancel,
            width=100,
            height=36,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(side="right", padx=(0, 8))

        dialog.bind("<Return>", lambda event: confirm())
        dialog.bind("<Escape>", lambda event: cancel())
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        name_entry.focus_set()
        if initial_value:
            name_entry.select_range(0, "end")
        dialog.wait_window()
        return result["value"]

    def create_project(self):
        if self.project_operations_locked():
            return

        name = self.prompt_project_name("New project", "Project name:")
        if name is None:
            return
        name = name.strip()

        if not self.is_valid_project_name(name):
            messagebox.showerror(APP_TITLE, "El nombre del proyecto no es válido.")
            return
        if any(existing.lower() == name.lower() for existing in self.projects):
            messagebox.showerror(APP_TITLE, "Ya existe un proyecto con ese nombre.")
            return

        workspace = self.workspace_path.resolve()

        try:
            interval = float(self.interval_var.get())
            max_backups = int(self.max_backups_var.get())
            if interval <= 0 or max_backups <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                APP_TITLE,
                "El intervalo y el máximo de ZIP deben ser valores válidos."
            )
            return

        project_path = workspace / name
        try:
            project_path.mkdir(parents=True, exist_ok=False)
            project_path.joinpath("Auto").mkdir()
            project_path.joinpath("Manual").mkdir()
        except OSError as exc:
            messagebox.showerror(
                APP_TITLE,
                f"No se pudo crear el proyecto:\n{exc}"
            )
            return

        self.projects[name] = {
            "name": name,
            "source": "",
            "interval": interval,
            "max_backups": max_backups,
            "sound_enabled": True,
            "success_sound": "01.wav",
            "custom_sound": ""
        }
        self.save_projects()
        self.selected_project_name = name
        self.refresh_project_controls()
        self.project_var.set(name)
        self.source_var.set("")
        self.interval_var.set(str(interval))
        self.max_backups_var.set(str(max_backups))
        self.dest_var.set(str(project_path))
        self.load_sound_settings(self.projects[name])
        self.update_start_button_state()

    def rename_project(self):
        if self.project_operations_locked() or not self.selected_project_name:
            return

        old_name = self.selected_project_name
        new_name = self.prompt_project_name(
            "Rename project",
            "New project name:",
            initial_value=old_name
        )
        if new_name is None:
            return
        new_name = new_name.strip()

        if not self.is_valid_project_name(new_name):
            messagebox.showerror(APP_TITLE, "El nombre del proyecto no es válido.")
            return
        if new_name.lower() != old_name.lower() and any(
            existing.lower() == new_name.lower() for existing in self.projects
        ):
            messagebox.showerror(APP_TITLE, "Ya existe un proyecto con ese nombre.")
            return
        if new_name == old_name:
            return

        old_path = self.workspace_path / old_name
        new_path = self.workspace_path / new_name
        try:
            old_path.rename(new_path)
        except OSError as exc:
            messagebox.showerror(
                APP_TITLE,
                f"No se pudo renombrar el proyecto:\n{exc}"
            )
            return

        project = self.projects.pop(old_name)
        project["name"] = new_name
        self.projects[new_name] = project
        self.selected_project_name = new_name
        self.save_projects()
        self.refresh_project_controls()
        self.dest_var.set(str(new_path))

    def uninstall(self):
        if self.project_operations_locked():
            messagebox.showerror(
                APP_TITLE,
                "No se puede desinstalar mientras hay un backup en ejecución."
            )
            return

        self.show_uninstall_hold_dialog()

    def show_uninstall_hold_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Uninstall")
        dialog.geometry("500x360")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLOR_BODY)
        dialog.transient(self.root)
        dialog.grab_set()

        header = ctk.CTkFrame(
            dialog,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=54
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Uninstall",
            text_color=COLOR_TEXT_LIGHT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_TITLE, weight="bold")
        ).pack(fill="both", padx=20)

        ctk.CTkLabel(
            dialog,
            text=(
                "This operation will permanently delete the central Workspace, "
                "all projects, and all backups.\n\n"
                "Hold A + L simultaneously for 4 seconds."
            ),
            text_color=COLOR_TEXT_LIGHT,
            justify="center",
            wraplength=440,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(fill="x", padx=24, pady=(22, 12))

        countdown_label = ctk.CTkLabel(
            dialog,
            text="4.0 s",
            text_color=COLOR_ACCENT,
            font=ctk.CTkFont(family=FONT_TIMER, size=30, weight="bold")
        )
        countdown_label.pack(pady=(0, 8))

        confirmation_bar = ctk.CTkProgressBar(
            dialog,
            height=12,
            corner_radius=2,
            fg_color=COLOR_RING_TRACK,
            progress_color=COLOR_ACCENT
        )
        confirmation_bar.set(0)
        confirmation_bar.pack(fill="x", padx=24, pady=(0, 12))

        ctk.CTkLabel(
            dialog,
            text="Release either key to restart the countdown.",
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_SECONDARY)
        ).pack()

        ctk.CTkButton(
            dialog,
            text="Cancel",
            command=lambda: close_dialog(),
            width=120,
            height=34,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(pady=(14, 16))

        pressed_keys = set()
        hold_started_at = {"value": None}
        confirmation_shown = {"value": False}

        def reset_countdown():
            hold_started_at["value"] = None
            countdown_label.configure(text="4.0 s")
            confirmation_bar.set(0)

        def key_press(event):
            key = event.keysym.lower()
            if key in {"a", "l"}:
                pressed_keys.add(key)

        def key_release(event):
            key = event.keysym.lower()
            if key in {"a", "l"}:
                pressed_keys.discard(key)
                reset_countdown()

        def update_countdown():
            if not dialog.winfo_exists() or confirmation_shown["value"]:
                return

            if pressed_keys == {"a", "l"}:
                if hold_started_at["value"] is None:
                    hold_started_at["value"] = time.monotonic()

                elapsed = min(4.0, time.monotonic() - hold_started_at["value"])
                remaining = max(0.0, 4.0 - elapsed)
                countdown_label.configure(text=f"{remaining:.1f} s")
                confirmation_bar.set(elapsed / 4.0)
                if remaining <= 0:
                    confirmation_shown["value"] = True
                    dialog.grab_release()
                    dialog.destroy()
                    self.delete_all_data()
                    return

            dialog.after(100, update_countdown)

        def close_dialog():
            dialog.grab_release()
            dialog.destroy()

        dialog.bind("<KeyPress>", key_press)
        dialog.bind("<KeyRelease>", key_release)
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)
        dialog.focus_force()
        update_countdown()

    def delete_all_data(self):
        try:
            if self.workspace_path and self.workspace_path.exists():
                shutil.rmtree(self.workspace_path)

            settings_path = self.settings_path()
            if settings_path.exists():
                settings_path.unlink()
        except OSError as exc:
            messagebox.showerror(
                APP_TITLE,
                f"No se pudieron eliminar todos los datos:\n{exc}"
            )
            return

        self.root.destroy()

    def validate_paths(self):
        source = Path(self.source_var.get().strip())
        dest = (
            self.workspace_path / self.selected_project_name
            if self.workspace_path and self.selected_project_name
            else None
        )

        if not source.is_dir():
            messagebox.showerror(APP_TITLE, "La carpeta de origen no es válida.")
            return None

        if dest is None or not dest.is_dir():
            messagebox.showerror(
                APP_TITLE,
                "La carpeta central de Auto Backup no es válida."
            )
            return None

        source = source.resolve()
        dest = dest.resolve()

        if self.is_inside(dest, source):
            messagebox.showerror(
                APP_TITLE,
                "La carpeta central de Auto Backup debe estar fuera de la "
                "carpeta de origen."
            )
            return None

        return source, dest

    def validate_settings(self):
        paths = self.validate_paths()
        if not paths:
            return None

        source, dest = paths

        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "El intervalo debe ser mayor que 0.")
            return None

        try:
            max_backups = int(self.max_backups_var.get())
            if max_backups <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "El máximo de ZIP debe ser un entero mayor que 0.")
            return None

        project = self.projects.get(self.selected_project_name)
        if project:
            project["source"] = str(source)
            project["interval"] = interval
            project["max_backups"] = max_backups
            self.save_projects()

        return source, dest, interval, max_backups

    def start_backup(self):
        settings = self.validate_settings()
        if not settings:
            return

        _, dest_root, _, _ = settings
        if not self.acquire_project_lock(dest_root):
            return

        self.running = True
        self.stop_event.clear()
        self.update_start_button_state()
        self.status_var.set("Running")
        self.status_dot.configure(text_color=COLOR_STATUS_OK)
        self.backup_in_progress = True
        self.next_backup_deadline = None

        self.worker_thread = threading.Thread(
            target=self.backup_loop,
            args=settings,
            daemon=True
        )
        self.worker_thread.start()

    def show_project_in_use_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Project in use")
        dialog.geometry("430x190")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLOR_BODY)
        dialog.transient(self.root)
        dialog.grab_set()

        header = ctk.CTkFrame(
            dialog,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=50
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Project in use",
            text_color=COLOR_TEXT_LIGHT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_BUTTON, weight="bold")
        ).pack(fill="both", padx=18)

        ctk.CTkLabel(
            dialog,
            text="This project is already running in another Auto Backup instance.",
            text_color=COLOR_FG,
            justify="center",
            wraplength=370,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO)
        ).pack(fill="both", expand=True, padx=20, pady=(20, 10))

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=90,
            height=34,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(family=FONT_LABEL, size=TEXT_INFO, weight="bold")
        ).pack(pady=(0, 16))

        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        dialog.update_idletasks()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        dialog.geometry(
            f"+{root_x + (root_width - dialog_width) // 2}"
            f"+{root_y + (root_height - dialog_height) // 2}"
        )
        dialog.focus_force()
        dialog.wait_window()

    def acquire_project_lock(self, project_path):
        mutex_handle = self.acquire_project_mutex(project_path)
        if mutex_handle is None:
            return False

        try:
            return self.acquire_project_lock_locked(project_path)
        finally:
            self.release_project_mutex(mutex_handle)

    @staticmethod
    def project_mutex_name(project_path):
        project_key = str(project_path.resolve()).casefold().encode("utf-8")
        project_hash = hashlib.sha256(project_key).hexdigest()
        return f"Local\\AutoBackupProjectLock_{project_hash}"

    def acquire_project_mutex(self, project_path):
        if os.name != "nt":
            messagebox.showerror(
                APP_TITLE,
                "No se puede establecer la exclusión mutua del bloqueo en "
                "este sistema."
            )
            return None

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.argtypes = [
            wintypes.LPVOID,
            wintypes.BOOL,
            wintypes.LPCWSTR
        ]
        kernel32.CreateMutexW.restype = wintypes.HANDLE
        kernel32.WaitForSingleObject.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD
        ]
        kernel32.WaitForSingleObject.restype = wintypes.DWORD

        mutex_handle = kernel32.CreateMutexW(
            None,
            False,
            self.project_mutex_name(project_path)
        )
        if not mutex_handle:
            messagebox.showerror(
                APP_TITLE,
                "No se pudo crear la exclusión mutua del bloqueo."
            )
            return None

        wait_result = kernel32.WaitForSingleObject(mutex_handle, 0xFFFFFFFF)
        if wait_result not in (0x00000000, 0x00000080):
            kernel32.CloseHandle(mutex_handle)
            messagebox.showerror(
                APP_TITLE,
                "No se pudo obtener la exclusión mutua del bloqueo."
            )
            return None

        return mutex_handle

    @staticmethod
    def release_project_mutex(mutex_handle):
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.ReleaseMutex.argtypes = [wintypes.HANDLE]
        kernel32.ReleaseMutex.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        kernel32.ReleaseMutex(mutex_handle)
        kernel32.CloseHandle(mutex_handle)

    def acquire_project_lock_locked(self, project_path):
        lock_path = project_path / ".autobackup.lock"
        process_status, creation_time = self.get_process_creation_time(os.getpid())
        if process_status != "active" or creation_time is None:
            messagebox.showerror(
                APP_TITLE,
                "No se pudo determinar con seguridad la fecha de inicio del "
                "proceso actual."
            )
            return False

        identity = {
            "pid": os.getpid(),
            "creation_time": creation_time,
            "created_at": self.creation_time_to_iso(creation_time)
        }

        try:
            self.create_lock_file(lock_path, identity)
            self.project_lock_path = lock_path
            self.project_lock_identity = identity
            return True
        except FileExistsError:
            pass
        except OSError as exc:
            messagebox.showerror(
                APP_TITLE,
                f"No se pudo bloquear el proyecto:\n{exc}"
            )
            return False

        lock_metadata = self.read_lock_metadata(lock_path)
        if not lock_metadata:
            messagebox.showerror(
                APP_TITLE,
                "No se puede determinar con seguridad si el bloqueo existente "
                "está obsoleto."
            )
            return False

        owner_status, owner_creation_time = self.get_process_creation_time(
            lock_metadata["pid"]
        )
        same_process_instance = (
            owner_status == "active"
            and owner_creation_time == lock_metadata["creation_time"]
        )

        if same_process_instance:
            self.show_project_in_use_dialog()
            return False

        if owner_status == "unknown":
            messagebox.showerror(
                APP_TITLE,
                "No se puede determinar con seguridad si el bloqueo existente "
                "está obsoleto."
            )
            return False

        recovery_path = lock_path.with_name(
            f".autobackup.lock.recovery.{os.getpid()}.{uuid.uuid4().hex}"
        )
        try:
            os.rename(lock_path, recovery_path)
        except FileNotFoundError:
            return self.acquire_project_lock_locked(project_path)
        except OSError as exc:
            messagebox.showerror(
                APP_TITLE,
                f"No se pudo recuperar el bloqueo obsoleto:\n{exc}"
            )
            return False

        try:
            self.create_lock_file(lock_path, identity)
        except FileExistsError:
            try:
                recovery_path.unlink()
            except OSError:
                pass
            messagebox.showerror(
                APP_TITLE,
                "Otra instancia recuperó el bloqueo antes que esta instancia."
            )
            return False
        except OSError as exc:
            try:
                recovery_path.unlink()
            except OSError:
                pass
            messagebox.showerror(
                APP_TITLE,
                f"No se pudo crear el nuevo bloqueo:\n{exc}"
            )
            return False

        try:
            recovery_path.unlink()
        except OSError:
            pass

        self.project_lock_path = lock_path
        self.project_lock_identity = identity
        return True

    @staticmethod
    def create_lock_file(lock_path, identity):
        lock_fd = os.open(
            lock_path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY
        )
        try:
            with os.fdopen(lock_fd, "w", encoding="utf-8") as lock_file:
                json.dump(identity, lock_file, ensure_ascii=False)
        except Exception:
            try:
                lock_path.unlink()
            except OSError:
                pass
            raise

    @staticmethod
    def read_lock_metadata(lock_path):
        try:
            with lock_path.open("r", encoding="utf-8") as lock_file:
                metadata = json.load(lock_file)
            pid = int(metadata["pid"])
            creation_time = int(metadata["creation_time"])
            created_at = str(metadata["created_at"])
            if pid <= 0 or creation_time <= 0 or not created_at:
                return None
            return {
                "pid": pid,
                "creation_time": creation_time,
                "created_at": created_at
            }
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
            return None

    @staticmethod
    def get_process_creation_time(pid):
        if os.name != "nt":
            return "unknown", None

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        ERROR_INVALID_PARAMETER = 87
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD
        ]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.GetProcessTimes.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.FILETIME),
            ctypes.POINTER(wintypes.FILETIME),
            ctypes.POINTER(wintypes.FILETIME),
            ctypes.POINTER(wintypes.FILETIME)
        ]
        kernel32.GetProcessTimes.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        handle = kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            pid
        )
        if not handle:
            if ctypes.get_last_error() == ERROR_INVALID_PARAMETER:
                return "missing", None
            return "unknown", None

        try:
            creation_time = wintypes.FILETIME()
            exit_time = wintypes.FILETIME()
            kernel_time = wintypes.FILETIME()
            user_time = wintypes.FILETIME()
            if not kernel32.GetProcessTimes(
                handle,
                ctypes.byref(creation_time),
                ctypes.byref(exit_time),
                ctypes.byref(kernel_time),
                ctypes.byref(user_time)
            ):
                return "unknown", None

            ticks = (
                (creation_time.dwHighDateTime << 32)
                | creation_time.dwLowDateTime
            )
            return "active", ticks
        finally:
            kernel32.CloseHandle(handle)

    @staticmethod
    def creation_time_to_iso(creation_time):
        unix_seconds = (creation_time - 116444736000000000) / 10000000
        return datetime.fromtimestamp(
            unix_seconds,
            tz=timezone.utc
        ).isoformat()

    def release_project_lock(self):
        if not self.project_lock_path or not self.project_lock_identity:
            return

        lock_path = self.project_lock_path
        lock_identity = self.project_lock_identity
        self.project_lock_path = None
        self.project_lock_identity = None

        lock_metadata = self.read_lock_metadata(lock_path)
        if not lock_metadata or any(
            lock_metadata[key] != lock_identity[key]
            for key in ("pid", "creation_time")
        ):
            return

        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            pass
        self.root.after(0, self.update_project_controls_state)

    def toggle_backup(self):
        if self.running:
            self.stop_backup()
        else:
            self.start_backup()

    def stop_backup(self):
        self.running = False
        self.stop_event.set()
        self.update_start_button_state()
        self.status_var.set("Stopped")
        self.status_dot.configure(text_color=COLOR_MUTED)
        self.backup_in_progress = False
        self.next_backup_deadline = None

    def backup_loop(self, source, dest_root, interval, max_backups):
        try:
            auto_dir = dest_root / "Auto"
            auto_dir.mkdir(parents=True, exist_ok=True)

            while not self.stop_event.is_set():
                zip_path = None
                try:
                    zip_path = self.create_backup(
                        source=source,
                        target_dir=auto_dir,
                        filename_prefix=dest_root.name,
                        excluded_root=dest_root
                    )
                    self.rotate_backups(auto_dir, max_backups)
                    self.record_history(
                        "Auto",
                        zip_path.name,
                        zip_path.stat().st_size,
                        "OK"
                    )
                    self.play_success_sound()
                except Exception as exc:
                    failed_zip = getattr(exc, "zip_path", zip_path)
                    zip_name = failed_zip.name if failed_zip else ""
                    zip_size = 0
                    if failed_zip:
                        try:
                            zip_size = failed_zip.stat().st_size
                        except OSError:
                            pass
                    self.record_history(
                        "Auto",
                        zip_name,
                        zip_size,
                        "Error",
                        str(exc)
                    )
                    self.play_error_sound()
                    self.root.after(
                        0,
                        lambda e=exc: self.status_var.set(f"Error: {e}")
                    )

                self.root.after(0, self.refresh_storage)

                self.next_backup_deadline = time.monotonic() + (interval * 60)
                self.current_interval_seconds = interval * 60
                self.backup_in_progress = False

                if self.stop_event.wait(interval * 60):
                    break
        finally:
            self.running = False
            self.backup_in_progress = False
            self.worker_thread = None
            self.release_project_lock()
            self.root.after(0, self.update_start_button_state)

    def create_manual_backup(self):
        if self.manual_thread and self.manual_thread.is_alive():
            return

        paths = self.validate_paths()
        if not paths:
            return

        description = self.prompt_project_name(
            "Snapshot manual",
            "Descripción opcional para el nombre del backup:"
        )

        if description is None:
            return

        source, dest_root = paths
        description = self.sanitize_description(description)

        release_project_lock = False
        if not self.project_lock_path:
            if not self.acquire_project_lock(dest_root):
                return
            release_project_lock = True

        self.manual_button.configure(state="disabled")
        self.status_var.set("Creating manual snapshot…")

        self.manual_thread = threading.Thread(
            target=self.manual_backup_worker,
            args=(source, dest_root, description, release_project_lock),
            daemon=True
        )
        self.manual_thread.start()

    def manual_backup_worker(
        self,
        source,
        dest_root,
        description,
        release_project_lock
    ):
        zip_path = None
        try:
            manual_dir = dest_root / "Manual"
            manual_dir.mkdir(parents=True, exist_ok=True)

            zip_path = self.create_backup(
                source=source,
                target_dir=manual_dir,
                description=description,
                filename_prefix=dest_root.name,
                excluded_root=dest_root
            )
            self.record_history(
                "Manual",
                zip_path.name,
                zip_path.stat().st_size,
                "OK"
            )
            self.play_success_sound()

            self.root.after(
                0,
                lambda: self.status_var.set(
                    f"Manual snapshot created: {zip_path.name}"
                )
            )
        except Exception as exc:
            failed_zip = getattr(exc, "zip_path", zip_path)
            zip_name = failed_zip.name if failed_zip else ""
            zip_size = 0
            if failed_zip:
                try:
                    zip_size = failed_zip.stat().st_size
                except OSError:
                    pass
            self.record_history(
                "Manual",
                zip_name,
                zip_size,
                "Error",
                str(exc)
            )
            self.play_error_sound()
            self.root.after(
                0,
                lambda e=exc: self.status_var.set(f"Error: {e}")
            )
        finally:
            self.manual_thread = None
            if release_project_lock:
                self.release_project_lock()
            self.root.after(
                0,
                lambda: (
                    self.manual_button.configure(state="normal"),
                    self.update_start_button_state(),
                    self.refresh_storage()
                )
            )

    def create_backup(
        self,
        source,
        target_dir,
        description="",
        filename_prefix="Backup",
        excluded_root=None
    ):
        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        suffix = f"_{description}" if description else ""
        zip_path = target_dir / f"{filename_prefix}_{timestamp}{suffix}.zip"
        temp_path = target_dir / f".{filename_prefix}_{timestamp}{suffix}.tmp"

        excluded_root = excluded_root.resolve() if excluded_root else None
        source = source.resolve()

        with zipfile.ZipFile(
            temp_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6
        ) as zf:
            for root_dir, dirs, files in os.walk(source):
                root_path = Path(root_dir)

                if excluded_root:
                    dirs[:] = [
                        d for d in dirs
                        if not self.is_inside((root_path / d).resolve(), excluded_root)
                    ]

                for file_name in files:
                    file_path = root_path / file_name

                    if excluded_root and self.is_inside(file_path.resolve(), excluded_root):
                        continue

                    arcname = file_path.relative_to(source)
                    zf.write(file_path, arcname)

        temp_path.replace(zip_path)

        try:
            self.verify_backup(zip_path)
        except Exception as exc:
            exc.zip_path = zip_path
            raise

        self.root.after(
            0,
            lambda: self.status_var.set(
                f"Last backup: {zip_path.name}"
            )
        )

        return zip_path

    @staticmethod
    def verify_backup(zip_path):
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                files = [info for info in zf.infolist() if not info.is_dir()]
                if not files:
                    raise RuntimeError("El ZIP verificado no contiene archivos.")

                bad_file = zf.testzip()
                if bad_file is not None:
                    raise RuntimeError(
                        f"El ZIP contiene un archivo dañado: {bad_file}"
                    )
        except (OSError, zipfile.BadZipFile) as exc:
            raise RuntimeError(f"No se pudo verificar el ZIP: {exc}") from exc

    @staticmethod
    def is_inside(path, parent):
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_description(text):
        text = text.strip()
        if not text:
            return ""

        invalid = '<>:"/\\|?*'
        cleaned = "".join(
            "-" if char.isspace() else char
            for char in text
            if char not in invalid and ord(char) >= 32
        )

        while "--" in cleaned:
            cleaned = cleaned.replace("--", "-")

        return cleaned.strip(" .-_")

    def rotate_backups(self, auto_dir, max_backups):
        backups = sorted(
            auto_dir.glob("*.zip"),
            key=lambda p: p.stat().st_mtime
        )

        while len(backups) > max_backups:
            oldest = backups.pop(0)
            try:
                oldest.unlink()
            except OSError:
                break

    def on_close(self):
        self.save_current_project_settings()
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = AutoBackupApp(root)
    root.mainloop()
