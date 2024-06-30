import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import time
from mutagen.mp3 import MP3

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x200")

        # Set the background color or image
        self.background_color = "#000000"
        self.root.configure(bg=self.background_color)

        # Initialize Track State
        self.current_track = ""
        self.is_playing = False
        self.is_paused = False
        self.playlist = []

        # UI Components
        self.create_widgets()

        # Update the progress bar
        self.update_progress_bar()

    def create_widgets(self):
        # Frame for track label
        self.track_frame = tk.Frame(self.root, bg=self.background_color)
        self.track_frame.pack(pady=10)

        self.track_label = tk.Label(self.track_frame, text="No track loaded", font=("Helvetica", 12), fg="white", bg=self.background_color)
        self.track_label.pack()

        # Frame for control buttons
        self.controls_frame = tk.Frame(self.root, bg=self.background_color)
        self.controls_frame.pack(pady=10)

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_pause, width=10, bg="#edff08", fg="Red", font=("Times new roman", 10, "bold"))
        self.play_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop, width=10, bg="#edff08", fg="red", font=("Times new roman", 10, "bold"))
        self.stop_button.grid(row=0, column=2, padx=5)

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.prev_track, width=10, bg="#edff08", fg="black", font=("Times new roman", 10, "bold"))
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_track, width=10, bg="#edff08", fg="black", font=("Times new roman", 10, "bold"))
        self.next_button.grid(row=0, column=3, padx=5)

        # Frame for load button and volume slider
        self.bottom_frame = tk.Frame(self.root, bg=self.background_color)
        self.bottom_frame.pack(pady=10)

        self.load_button = tk.Button(self.bottom_frame, text="Load Track....", command=self.load_track, width=15, bg="#a8fe39", fg="black", font=("Times new roman", 10, "bold"))
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.volume_slider = tk.Scale(self.bottom_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, label="Volume", command=self.set_volume, bg=self.background_color, fg="white")
        self.volume_slider.set(0.5)
        self.volume_slider.grid(row=0, column=1, padx=3, pady=3)

        # Frame for progress bar and label
        self.progress_frame = tk.Frame(self.root, bg=self.background_color)
        self.progress_frame.pack(pady=10)

        self.progress_label = tk.Label(self.progress_frame, text="00:00", font=("Helvetica", 12), fg="white", bg=self.background_color)
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)

    def play_pause(self):
        if not self.current_track:
            messagebox.showerror("Error", "No track loaded")
            return
        
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.play_button.config(text="Pause")
            self.is_paused = False
        elif self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
            self.is_paused = True
        else:
            pygame.mixer.music.play(-1)
            self.play_button.config(text="Pause")
            self.is_playing = True
            self.is_paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.play_button.config(text="Play")
        self.is_playing = False
        self.is_paused = False

    def prev_track(self):
        if not self.playlist:
            return
        current_index = self.playlist.index(self.current_track)
        prev_index = (current_index - 1) % len(self.playlist)
        self.load_track_from_playlist(prev_index)

    def next_track(self):
        if not self.playlist:
            return
        current_index = self.playlist.index(self.current_track)
        next_index = (current_index + 1) % len(self.playlist)
        self.load_track_from_playlist(next_index)

    def load_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.playlist.append(file_path)
            self.load_track_from_playlist(len(self.playlist) - 1)

    def load_track_from_playlist(self, index):
        self.current_track = self.playlist[index]
        pygame.mixer.music.load(self.current_track)
        self.track_label.config(text=os.path.basename(self.current_track))
        self.is_playing = False
        self.is_paused = False
        self.play_pause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_progress_bar(self):
        if self.is_playing:
            try:
                track_length = MP3(self.current_track).info.length
                current_time = pygame.mixer.music.get_pos() / 1000
                self.progress_bar['value'] = (current_time / track_length) * 100
                self.progress_label.config(text=f"{time.strftime('%M:%S', time.gmtime(current_time))} / {time.strftime('%M:%S', time.gmtime(track_length))}")
            except:
                pass

        self.root.after(1000, self.update_progress_bar)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
