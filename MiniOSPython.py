from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

import hashlib
import json
import os
import random
import time


# =========================================================
# PROCESS
# =========================================================

class Process:

    def __init__(self, pid, name, cpu):

        self.pid = pid
        self.name = name
        self.cpu = cpu
        self.status = "RUNNING"


# =========================================================
# FILE SYSTEM
# =========================================================

class FileSystem:

    def __init__(self):

        self.files = {
            "root": {
                "type": "folder",
                "children": {

                    "Documents": {
                        "type": "folder",
                        "children": {}
                    },

                    "Downloads": {
                        "type": "folder",
                        "children": {}
                    },

                    "Music": {
                        "type": "folder",
                        "children": {}
                    },
                }
            }
        }

    def create_folder(self, path, folder_name):

        current = self._get_folder(path)

        if current and folder_name not in current["children"]:

            current["children"][folder_name] = {
                "type": "folder",
                "children": {}
            }

            return True

        return False

    def create_file(self, path, file_name, content=""):

        current = self._get_folder(path)

        if current and file_name not in current["children"]:

            current["children"][file_name] = {
                "type": "file",
                "content": content
            }

            return True

        return False

    def get_contents(self, path):

        current = self._get_folder(path)

        if current:

            return current["children"]

        return {}

    def _get_folder(self, path):

        if path == "root":

            return self.files["root"]

        parts = path.split("/")

        current = self.files["root"]

        for part in parts[1:]:

            if part in current["children"]:

                current = current["children"][part]

            else:

                return None

        return current


# =========================================================
# MAIN APP
# =========================================================

class NeonOS:

    def __init__(self, root):

        self.root = root

        self.root.title("NEON OS")

        self.root.geometry("1280x720")

        self.root.configure(bg="#140018")

        self.root.resizable(False, False)

        # =====================================================
        # COLORS
        # =====================================================

        self.bg = "#140018"
        self.bg2 = "#1d0224"
        self.bg3 = "#2a0632"

        self.panel = "#220028"

        self.accent = "#7a2cff"
        self.accent_hover = "#914dff"

        self.text = "#efe7ff"
        self.dark = "#0a000d"

        self.border = "#4b1f70"

        # =====================================================
        # DATA
        # =====================================================

        self.processes = []

        self.pid_counter = 3000

        self.cpu_usage = tk.IntVar(value=10)

        self.logs = []

        self.windows = {}

        self.filesystem = FileSystem()

        # =====================================================
        # USERS
        # =====================================================

        self.users_file = "users.json"

        self.current_user = "Guest"

        self.users = self.load_users()

        # =====================================================
        # STYLE
        # =====================================================

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.panel,
            foreground=self.text,
            fieldbackground=self.panel,
            rowheight=28,
            bordercolor=self.border,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.accent,
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        # =====================================================
        # START LOGIN ONLY
        # =====================================================

        self.show_login()

    # =========================================================
    # USERS
    # =========================================================

    def hash_password(self, password):

        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):

        if not os.path.exists(self.users_file):

            default = {
                "admin": self.hash_password("admin")
            }

            with open(self.users_file, "w") as f:

                json.dump(default, f, indent=4)

            return default

        try:

            with open(self.users_file, "r") as f:

                return json.load(f)

        except:

            return {}

    def save_users(self):

        with open(self.users_file, "w") as f:

            json.dump(self.users, f, indent=4)

    # =========================================================
    # LOGIN SCREEN
    # =========================================================

    def show_login(self):

        self.login_frame = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.login_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            self.login_frame,
            bg=self.bg,
            highlightthickness=0
        )

        canvas.place(relwidth=1, relheight=1)

        for i in range(25):

            x = random.randint(-400, 1400)

            y = random.randint(-400, 900)

            r = random.randint(80, 300)

            color = random.choice([
                "#240030",
                "#2d0837",
                "#3b0c4d",
                "#4d1461",
                "#2a0632"
            ])

            canvas.create_oval(
                x,
                y,
                x + r,
                y + r,
                fill=color,
                outline=""
            )

        panel = tk.Frame(
            self.login_frame,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=2
        )

        panel.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=420,
            height=380
        )

        title = tk.Label(
            panel,
            text="NEON OS",
            bg=self.panel,
            fg=self.accent,
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=25)

        subtitle = tk.Label(
            panel,
            text="LOGIN SYSTEM",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 11)
        )

        subtitle.pack(pady=5)

        user_entry = tk.Entry(
            panel,
            bg=self.bg3,
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 12)
        )

        user_entry.pack(fill="x", padx=40, pady=15)

        user_entry.insert(0, "Username")

        pass_entry = tk.Entry(
            panel,
            bg=self.bg3,
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 12),
            show="*"
        )

        pass_entry.pack(fill="x", padx=40, pady=10)

        def login_user():

            username = user_entry.get().strip()

            password = pass_entry.get().strip()

            hashed = self.hash_password(password)

            if username in self.users:

                if self.users[username] == hashed:

                    self.current_user = username

                    self.log(f"User login: {username}")

                    self.login_frame.destroy()

                    self.build_desktop()

                    return

            self.log(f"Failed login: {username}")

            messagebox.showerror(
                "Error",
                "Invalid username or password"
            )

        def register_user():

            username = user_entry.get().strip()

            password = pass_entry.get().strip()

            if not username or not password:

                messagebox.showerror(
                    "Error",
                    "Fill all fields"
                )

                return

            if username in self.users:

                messagebox.showerror(
                    "Error",
                    "User already exists"
                )

                return

            self.users[username] = self.hash_password(password)

            self.save_users()

            self.log(f"Created user: {username}")

            messagebox.showinfo(
                "Success",
                "User created successfully"
            )

        login_btn = tk.Button(
            panel,
            text="LOGIN",
            command=login_user,
            bg=self.accent,
            fg="white",
            activebackground=self.accent_hover,
            bd=0,
            font=("Segoe UI", 12, "bold"),
            pady=10
        )

        login_btn.pack(fill="x", padx=40, pady=15)

        reg_btn = tk.Button(
            panel,
            text="REGISTER",
            command=register_user,
            bg=self.bg3,
            fg="white",
            activebackground=self.accent,
            bd=0,
            font=("Segoe UI", 11),
            pady=10
        )

        reg_btn.pack(fill="x", padx=40)

    # =========================================================
    # BUILD DESKTOP AFTER LOGIN
    # =========================================================

    def build_desktop(self):

        # =====================================================
        # DESKTOP
        # =====================================================

        self.desktop = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.desktop.pack(fill="both", expand=True)

        self.draw_wallpaper()

        # =====================================================
        # TASKBAR
        # =====================================================

        self.taskbar = tk.Frame(
            self.root,
            bg=self.dark,
            height=44
        )

        self.taskbar.pack(fill="x", side="bottom")

        self.menu_btn = tk.Button(
            self.taskbar,
            text="MENU",
            command=self.toggle_menu,
            bg=self.accent,
            fg="white",
            activebackground=self.accent_hover,
            bd=0,
            font=("Segoe UI", 11, "bold")
        )

        self.menu_btn.pack(side="left", padx=10, pady=6)

        self.process_frame = tk.Frame(
            self.taskbar,
            bg=self.dark
        )

        self.process_frame.pack(side="left", padx=10)

        self.clock = tk.Label(
            self.taskbar,
            bg=self.dark,
            fg=self.text,
            font=("Consolas", 11)
        )

        self.clock.pack(side="right", padx=20)

        self.user_label = tk.Label(
            self.taskbar,
            text=self.current_user,
            bg=self.dark,
            fg=self.text,
            font=("Segoe UI", 10)
        )

        self.user_label.pack(side="right", padx=10)

        # =====================================================
        # MENU
        # =====================================================

        self.menu = tk.Frame(
            self.desktop,
            bg=self.panel,
            width=260,
            height=370,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.menu_visible = False

        self.build_menu()

        # =====================================================
        # ICONS
        # =====================================================

        self.build_icons()

        # =====================================================
        # START SYSTEM
        # =====================================================

        self.update_clock()

        self.update_cpu()

        self.log("Desktop loaded")

    # =========================================================
    # WALLPAPER
    # =========================================================

    def draw_wallpaper(self):

        self.wallpaper = tk.Canvas(
            self.desktop,
            bg=self.bg,
            highlightthickness=0
        )

        self.wallpaper.place(relwidth=1, relheight=1)

        for i in range(20):

            x = random.randint(-400, 1400)

            y = random.randint(-400, 900)

            r = random.randint(100, 300)

            color = random.choice([
                "#240030",
                "#2d0837",
                "#3b0c4d",
                "#4d1461",
                "#2a0632"
            ])

            self.wallpaper.create_oval(
                x,
                y,
                x + r,
                y + r,
                fill=color,
                outline=""
            )

    # =========================================================
    # MENU
    # =========================================================

    def build_menu(self):

        title = tk.Label(
            self.menu,
            text="NEON OS",
            bg=self.panel,
            fg=self.accent,
            font=("Segoe UI", 20, "bold")
        )

        title.pack(pady=18)

        buttons = [

            ("Task Manager", self.open_task_manager),
            ("Monitor", self.open_monitor),
            ("Logs", self.open_logs),
            ("Browser", self.open_browser),
            ("Calculator", self.open_calculator),
            ("File Manager", self.open_file_manager),
        ]

        for text, cmd in buttons:

            btn = tk.Button(
                self.menu,
                text=text,
                command=cmd,
                bg=self.bg3,
                fg="white",
                bd=0,
                height=2,
                font=("Segoe UI", 11)
            )

            btn.pack(fill="x", padx=14, pady=5)

    def toggle_menu(self):

        if self.menu_visible:

            self.menu.place_forget()

            self.menu_visible = False

        else:

            self.menu.place(x=12, y=250)

            self.menu.lift()

            self.menu_visible = True

    # =========================================================
    # ICONS
    # =========================================================

    def build_icons(self):

        icons = [

            ("📊", "Task Manager", self.open_task_manager),
            ("📈", "Monitor", self.open_monitor),
            ("📜", "Logs", self.open_logs),
            ("🌐", "Browser", self.open_browser),
            ("🧮", "Calculator", self.open_calculator),
            ("📁", "File Manager", self.open_file_manager),
        ]

        y = 40

        for icon, text, cmd in icons:

            frame = tk.Frame(
                self.desktop,
                bg=self.bg
            )

            frame.place(x=35, y=y)

            lbl1 = tk.Label(
                frame,
                text=icon,
                bg=self.bg,
                fg=self.accent,
                font=("Segoe UI Emoji", 28)
            )

            lbl1.pack()

            lbl2 = tk.Label(
                frame,
                text=text,
                bg=self.bg,
                fg=self.text,
                font=("Segoe UI", 10)
            )

            lbl2.pack()

            frame.bind("<Double-Button-1>", lambda e, c=cmd: c())
            lbl1.bind("<Double-Button-1>", lambda e, c=cmd: c())
            lbl2.bind("<Double-Button-1>", lambda e, c=cmd: c())

            y += 110

    # =========================================================
    # PROCESS
    # =========================================================

    def start_process(self, name):

        self.pid_counter += 1

        process = Process(
            self.pid_counter,
            name,
            random.randint(1, 15)
        )

        self.processes.append(process)

        self.refresh_taskbar()

        return process

    def stop_process(self, pid):

        self.processes = [
            p for p in self.processes
            if p.pid != pid
        ]

        self.refresh_taskbar()

    # =========================================================
    # WINDOWS
    # =========================================================

    def create_window(self, key, title, w=700, h=400, pid=None):

        if key in self.windows:

            try:

                self.windows[key].lift()

                return self.windows[key]

            except:

                del self.windows[key]

        win = tk.Toplevel(self.root)

        win.title(title)

        win.geometry(f"{w}x{h}")

        win.configure(bg=self.panel)

        self.windows[key] = win

        def on_close():

            if pid:

                self.stop_process(pid)

            if key in self.windows:

                del self.windows[key]

            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        return win

    # =========================================================
    # TASKBAR
    # =========================================================

    def refresh_taskbar(self):

        for widget in self.process_frame.winfo_children():

            widget.destroy()

        for process in self.processes:

            btn = tk.Button(
                self.process_frame,
                text=process.name,
                bg=self.bg3,
                fg="white",
                bd=0,
                font=("Segoe UI", 9)
            )

            btn.pack(side="left", padx=4)

    # =========================================================
    # TASK MANAGER
    # =========================================================

    def open_task_manager(self):

        proc = self.start_process("Task Manager")

        win = self.create_window(
            "task_manager",
            "Task Manager",
            700,
            400,
            proc.pid
        )

        tree = ttk.Treeview(
            win,
            columns=("PID", "NAME", "CPU"),
            show="headings"
        )

        tree.heading("PID", text="PID")
        tree.heading("NAME", text="PROCESS")
        tree.heading("CPU", text="CPU")

        tree.pack(fill="both", expand=True)

        def refresh():

            try:

                tree.delete(*tree.get_children())

                for p in self.processes:

                    tree.insert(
                        "",
                        "end",
                        values=(
                            p.pid,
                            p.name,
                            f"{p.cpu}%"
                        )
                    )

                win.after(1000, refresh)

            except:

                pass

        refresh()

    # =========================================================
    # MONITOR
    # =========================================================

    def open_monitor(self):

        proc = self.start_process("Monitor")

        win = self.create_window(
            f"monitor_{proc.pid}",
            "Monitor",
            500,
            300,
            proc.pid
        )

        title = tk.Label(
            win,
            text="SYSTEM MONITOR",
            bg=self.panel,
            fg=self.accent,
            font=("Segoe UI", 18, "bold")
        )

        title.pack(pady=20)

        cpu = tk.Label(
            win,
            bg=self.panel,
            fg="white",
            font=("Consolas", 30)
        )

        cpu.pack()

        def update():

            try:

                cpu.config(
                    text=f"CPU: {self.cpu_usage.get()}%"
                )

                win.after(1000, update)

            except:

                pass

        update()

    # =========================================================
    # LOGS
    # =========================================================

    def open_logs(self):

        proc = self.start_process("Logs")

        win = self.create_window(
            "logs",
            "Logs",
            700,
            350,
            proc.pid
        )

        text = tk.Text(
            win,
            bg="#09000d",
            fg="#d9b3ff",
            font=("Consolas", 10),
            bd=0
        )

        text.pack(fill="both", expand=True)

        text.insert(
            "1.0",
            "\n".join(self.logs)
        )

    # =========================================================
    # BROWSER
    # =========================================================

    def open_browser(self):

        proc = self.start_process("Browser")

        win = self.create_window(
            f"browser_{proc.pid}",
            "Browser",
            700,
            400,
            proc.pid
        )

        label = tk.Label(
            win,
            text="NEON BROWSER",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 20)
        )

        label.pack(pady=50)

    # =========================================================
    # CALCULATOR
    # =========================================================

    def open_calculator(self):

        proc = self.start_process("Calculator")

        win = self.create_window(
            f"calc_{proc.pid}",
            "Calculator",
            320,
            420,
            proc.pid
        )

        display = tk.Entry(
            win,
            font=("Consolas", 20),
            justify="right",
            bg="#0d0011",
            fg="white",
            insertbackground="white"
        )

        display.pack(fill="x", padx=10, pady=10)

        def press(v):

            if v == "=":

                try:

                    result = eval(display.get())

                    display.delete(0, "end")

                    display.insert(0, str(result))

                except:

                    display.delete(0, "end")

                    display.insert(0, "ERROR")

                return

            if v == "C":

                display.delete(0, "end")

                return

            display.insert("end", v)

        buttons = [

            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", "C", "=", "+"
        ]

        frame = tk.Frame(
            win,
            bg=self.panel
        )

        frame.pack(expand=True)

        r = 0
        c = 0

        for b in buttons:

            btn = tk.Button(
                frame,
                text=b,
                command=lambda x=b: press(x),
                bg=self.bg3,
                fg="white",
                width=5,
                height=2,
                bd=0,
                font=("Segoe UI", 14)
            )

            btn.grid(
                row=r,
                column=c,
                padx=5,
                pady=5
            )

            c += 1

            if c > 3:

                c = 0
                r += 1

    # =========================================================
    # FILE MANAGER
    # =========================================================

    def open_file_manager(self):

        proc = self.start_process("File Manager")

        win = self.create_window(
            f"fm_{proc.pid}",
            "File Manager",
            700,
            500,
            proc.pid
        )

        listbox = tk.Listbox(
            win,
            bg=self.bg2,
            fg=self.text,
            font=("Consolas", 10)
        )

        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        contents = self.filesystem.get_contents("root")

        for name, item in contents.items():

            icon = "📁" if item["type"] == "folder" else "📄"

            listbox.insert(
                "end",
                f"{icon} {name}"
            )

    # =========================================================
    # CPU
    # =========================================================

    def update_cpu(self):

        active = sum(p.cpu for p in self.processes)

        value = max(
            1,
            min(
                100,
                active + random.randint(-5, 5)
            )
        )

        self.cpu_usage.set(value)

        self.root.after(1500, self.update_cpu)

    # =========================================================
    # CLOCK
    # =========================================================

    def update_clock(self):

        self.clock.config(
            text=time.strftime("%H:%M:%S")
        )

        self.root.after(1000, self.update_clock)

    # =========================================================
    # LOGS
    # =========================================================

    def log(self, text):

        stamp = time.strftime("%H:%M:%S")

        self.logs.append(
            f"[{stamp}] {text}"
        )


# =========================================================
# START
# =========================================================

root = tk.Tk()

app = NeonOS(root)

root.mainloop()