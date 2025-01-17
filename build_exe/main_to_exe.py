import subprocess
from time import sleep

import customtkinter as ctk


def version_list():
    version_list = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                version_list.append(f"{i}.{j}.{k}")
    return version_list


def pyinstaller(version):
    subprocess.run([
        "pyinstaller",
        "--noconfirm",
        "--onefile",  # Einzelne ausführbare Datei
        "--windowed",  # Verhindert die Konsolenausgabe
        "--name", f"YouTube Playlist Downloader {version}",
        "--clean",  # Löscht alte Build-Dateien
        "--distpath", "..",  # Ergebnisverzeichnis festlegen
        "--workpath", "./build",  # Arbeitsverzeichnis für temporäre Dateien
        "--specpath", "./build",  # Speicherort der .spec Datei
        #"--icon", "app.ico",  # Benutzerdefiniertes Icon hinzufügen
        "--hidden-import", "customtkinter",  # Versteckten Import hinzufügen
        #"--add-data", "app.ico;.",  # Zusätzliche Ressourcen einbinden (z.B. Bilder)
        "../main.py"
    ])
    subprocess.run(["rmdir", "/s", "/q", "build"], shell=True)
    print("Build complete!")
    print("Exiting...")
    sleep(1)
    exit()


def window_center():
    w = 300
    h = 150
    s_w = app.winfo_screenwidth()
    s_h = app.winfo_screenheight()
    x = (s_w - w) / 2
    y = (s_h - h) / 2
    return app.geometry(f"{w}x{h}+{int(x)}+{int(y)}")


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Main.py to EXE")
window_center()
app.resizable(False, False)

label_version = ctk.CTkLabel(app, text="Enter the versions Number:")
label_version.pack(pady=10)
versions_box = ctk.CTkComboBox(app, values=version_list(), width=80)
versions_box.pack(pady=5)
start_btn = ctk.CTkButton(app, text="Start Script", command=lambda: pyinstaller(versions_box.get()))
start_btn.pack(pady=20)


app.mainloop()
