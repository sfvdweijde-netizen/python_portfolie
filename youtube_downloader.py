import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import os
import threading


class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Media Downloader")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        # UI Colors (Dark theme)
        self.BG_DARK = "#1E1E24"
        self.BG_CARD = "#2A2A35"
        self.FG_WHITE = "#FFFFFF"
        self.ACCENT_RED = "#FF3333"

        self.root.configure(bg=self.BG_DARK)
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.BG_DARK, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame, text="YouTube Downloader", bg=self.BG_DARK, fg=self.ACCENT_RED,
                 font=("Arial", 16, "bold")).pack(pady=10)

        # URL Input
        tk.Label(main_frame, text="Enter YouTube URL:", bg=self.BG_DARK, fg=self.FG_WHITE, font=("Arial", 10)).pack(
            anchor=tk.W)
        self.url_entry = tk.Entry(main_frame, bg=self.BG_CARD, fg=self.FG_WHITE, insertbackground=self.FG_WHITE, bd=0,
                                  font=("Arial", 11), width=45)
        self.url_entry.pack(pady=5, ipady=5)

        # Format Dropdown (Video or Audio)
        drop_frame = tk.Frame(main_frame, bg=self.BG_DARK)
        drop_frame.pack(fill=tk.X, pady=10)

        tk.Label(drop_frame, text="Download Format:", bg=self.BG_DARK, fg=self.FG_WHITE).pack(side=tk.LEFT,
                                                                                              padx=(0, 10))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.BG_CARD, background=self.BG_CARD, foreground=self.FG_WHITE,
                        arrowcolor=self.FG_WHITE)

        self.format_combo = ttk.Combobox(drop_frame, values=["Video (MP4)", "Audio Only (MP3)"], width=18,
                                         state="readonly")
        self.format_combo.set("Video (MP4)")
        self.format_combo.pack(side=tk.LEFT)

        # Download Button
        self.download_btn = tk.Button(main_frame, text="Start Download", command=self.start_download_thread,
                                      bg=self.ACCENT_RED, fg=self.FG_WHITE, activebackground="#CC2222",
                                      activeforeground=self.FG_WHITE, relief=tk.FLAT, font=("Arial", 11, "bold"))
        self.download_btn.pack(fill=tk.X, pady=10)

        # Status Label
        self.status_label = tk.Label(main_frame, text="Status: Ready", bg=self.BG_DARK, fg=self.FG_WHITE,
                                     font=("Arial", 9, "italic"))
        self.status_label.pack(pady=5)

    def start_download_thread(self):
        """Starts the download process in a background thread to prevent the GUI from freezing."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a valid URL first!")
            return

        self.download_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Processing... Please wait.")

        # Threading zorgt ervoor dat je app niet vastloopt tijdens het downloaden
        download_thread = threading.Thread(target=self.download_media, args=(url,))
        download_thread.start()

    def download_media(self, url):
        fmt = self.format_combo.get()
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")  # Slaat op in je normale 'Downloads' map

        # Configureer de yt-dlp opties op basis van de keuze (Video of Audio)
        if fmt == "Audio Only (MP3)":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Status: Download Completed successfully!")
            messagebox.showinfo("Success", f"Media downloaded successfully to your Downloads folder!")
        except Exception as e:
            self.status_label.config(text="Status: Download Failed.")
            messagebox.showerror("Error", f"An error occurred during extraction. Make sure the link is valid.")
        finally:
            self.download_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()
