import os
import threading
import platform
import subprocess
import webbrowser
import sys
from tkinter import messagebox
import customtkinter as ctk
from pytube import Playlist
from yt_dlp import YoutubeDL


class RedirectConsole:
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def write(self, message):
        if message.strip():
            self.log_widget.configure(state="normal")
            self.log_widget.insert("end", message + "\n")
            self.log_widget.see("end")
            self.log_widget.configure(state="disabled")

    def flush(self):
        pass


def run_gui():
    def log_message(message):
        log_textbox.configure(state="normal")
        log_textbox.insert("end", message + "\n")
        log_textbox.see("end")
        log_textbox.configure(state="disabled")

    def open_github(event=None):
        webbrowser.open("https://github.com/CyberByteCraft")

    def start_download():
        playlist_url = url_input.get().strip()

        if not playlist_url or not playlist_url.startswith("http"):
            messagebox.showerror("Invalid Input", "Please enter a valid YouTube playlist URL.")
            return

        def playlist_path_name(url):
            try:
                playlist = Playlist(url)
                playlist_title = playlist.title or "Unknown Playlist"
                log_message(f"Playlist detected: {playlist_title}")
                print(f"Playlist detected: {playlist_title}")
            except Exception as e:
                playlist_title = "Unknown Playlist"
                log_message(f"Error fetching playlist title: {str(e)}")
                print(f"Error fetching playlist title: {str(e)}")

            sanitized_title = "".join([c if c.isalnum() or c in " _-" else "_" for c in playlist_title])
            output_path = f"./output/{sanitized_title}"
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                log_message(f"Output folder created: {output_path}")
                print(f"Output folder created: {output_path}")
            return sanitized_title

        def progress_hook(d):
            if d["status"] == "downloading":
                percent = d.get("_percent_str", "N/A")
                log_message(f"Download progress: {percent}")
                print(f"Download progress: {percent}")
            elif d["status"] == "finished":
                log_message("Download finished!")
                print("Download finished!")
            elif d["status"] == "error":
                log_message(f"Error occurred: {d['filename']}")
                print(f"Error occurred: {d['filename']}")

        playlist_name = playlist_path_name(playlist_url)

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"output/{playlist_name}/%(title)s.%(ext)s",
            "noplaylist": False,
            "progress_hooks": [progress_hook],
            "download_archive": f"output/{playlist_name}/downloaded.txt",
            "ignoreerrors": True,
            "postprocessor_args": ["-i"],
        }

        def download():
            try:
                log_message("Download started...")
                print("Download started...")
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([playlist_url])
                messagebox.showinfo("Download Complete",
                                    "All videos in the playlist have been downloaded successfully!")
                log_message("All videos have been downloaded successfully!")
                print("All videos have been downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                log_message(f"Error during download: {str(e)}")
                print(f"Error during download: {str(e)}")

        threading.Thread(target=download).start()

    def open_save_dir():
        path = os.path.realpath("output")
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            log_message(f"Output folder opened: {path}")
            print(f"Output folder opened: {path}")
        except Exception as e:
            log_message(f"Error opening output folder: {str(e)}")
            print(f"Error opening output folder: {str(e)}")

    def window_center():
        w = 600
        h = 800
        s_w = app.winfo_screenwidth()
        s_h = app.winfo_screenheight()
        x = (s_w - w) / 2
        y = (s_h - h) / 2
        return app.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("YouTube Playlist Downloader")
    window_center()
    app.resizable(False, False)

    label_url = ctk.CTkLabel(app, text="Enter YouTube Playlist URL:")
    label_url.pack(pady=10)
    url_input = ctk.CTkEntry(app, width=500)
    url_input.pack(pady=5)

    download_btn = ctk.CTkButton(app, text="Start Download", command=start_download)
    download_btn.pack(pady=20)

    open_dir_btn = ctk.CTkButton(app, text="Open Output Folder", command=open_save_dir)
    open_dir_btn.pack(pady=5)

    log_label = ctk.CTkLabel(app, text="Log:")
    log_label.pack(pady=10)
    log_textbox = ctk.CTkTextbox(app, width=570, height=500, state="disabled")
    log_textbox.pack(pady=10, expand=True)

    label_footer = ctk.CTkLabel(app, text="Made by CyberByteCraft | github.com/CyberByteCraft | 2025 | Version 0.0.2",
                                font=("Arial", 12, "bold"), cursor="hand2")
    label_footer.pack(side="bottom")

    label_footer.bind("<Button-1>", open_github)

    sys.stdout = RedirectConsole(log_textbox)
    sys.stderr = RedirectConsole(log_textbox)

    app.mainloop()


if __name__ == "__main__":
    run_gui()