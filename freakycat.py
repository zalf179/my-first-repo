import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO

GIF_URL = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnJuOWRjOXljM2x0dXp3bG01aWxtYTZ6c3l2cWhyZGg0cXRpaGdtZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vPzbDN4rBxuvtpSpzF/giphy.gif"

def start_app():
    # Ambil GIF dari internet
    resp = requests.get(GIF_URL, timeout=5)
    gif_bytes = BytesIO(resp.content)
    pil_gif = Image.open(gif_bytes)

    # Setup window
    root = tk.Tk()
    root.title("FREAKYYY CATTT 🤪🤪")
    root.geometry("400x400")
    root.configure(bg="black")

    label = tk.Label(root, bg="black")
    label.pack(expand=True)

    frames = []
    for frame in ImageSequence.Iterator(pil_gif):
        frames.append(ImageTk.PhotoImage(frame))

    def animate(index):
        label.config(image=frames[index])
        root.after(100, animate, (index + 1) % len(frames))

    root.after(0, animate, 0)
    root.mainloop()

# INI KUNCINYA: Kode di bawah ini GAK AKAN jalan pas di-import buat testing
if __name__ == "__main__":
    start_app()
