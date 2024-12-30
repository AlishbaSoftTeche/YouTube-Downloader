
import os
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox, ttk
import yt_dlp
import threading

def browse_path():
    download_path = filedialog.askdirectory()
    path_var.set(download_path)

def download_video():
    def start_download():
        try:
            url = url_var.get().strip()
            save_path = path_var.get().strip()
            file_type = format_var.get()

            if not url or not save_path:
                messagebox.showerror("Error", "Please enter a URL and select a save location.")
                return

            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best' if file_type == "Audio" else 'bestvideo+bestaudio',
                'merge_output_format': 'mp4' if file_type == "Video" else None,
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4'
                    } if file_type == "Video" else {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }
                ]
            }

            download_label.config(text="Downloading...")
            progress_var.set(0)
            progress_bar.update_idletasks()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            download_label.config(text="Download completed!")
            progress_var.set(100)
            progress_bar.update_idletasks()
            messagebox.showinfo("Success", f"{file_type} downloaded successfully!")
        except yt_dlp.utils.DownloadError as e:
            if "forbidden" in str(e).lower():
                messagebox.showerror("Error", "Forbidden error: Unable to download the video. Try using a different URL.")
            elif "ffmpeg" in str(e).lower():
                messagebox.showerror("Error", "FFmpeg is required but not installed. Please install FFmpeg.")
            else:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            download_label.config(text="")
            progress_var.set(0)

    threading.Thread(target=start_download).start()

root = Tk()
root.title("YouTube Downloader")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

Label(root, text="YouTube Downloader", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

url_var = StringVar()
Label(root, text="YouTube URL:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
Entry(root, textvariable=url_var, width=50, font=("Arial", 10)).pack(pady=5)

path_var = StringVar()
Label(root, text="Save Path:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
frame_path = ttk.Frame(root)
frame_path.pack(pady=5)
Entry(frame_path, textvariable=path_var, width=40, font=("Arial", 10)).pack(side="left", padx=5)
Button(frame_path, text="Browse", command=browse_path, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side="right")

format_var = StringVar(value="Video")
Label(root, text="Select Format:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
frame_format = ttk.Frame(root)
frame_format.pack(pady=5)
Button(frame_format, text="Video", command=lambda: format_var.set("Video"), width=10, bg="#2196F3", fg="white").pack(side="left", padx=5)
Button(frame_format, text="Audio", command=lambda: format_var.set("Audio"), width=10, bg="#FF5722", fg="white").pack(side="right", padx=5)

Button(root, text="Download", command=download_video, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=20)

progress_var = StringVar(value=0)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=10)

download_label = Label(root, text="", font=("Arial", 10), bg="#f0f0f0", fg="green")
download_label.pack(pady=5)

root.mainloop()
