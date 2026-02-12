import yt_dlp
import os

def download_yt_as_mp3():
    # Masukkan URL video YouTube di sini
    url = input("Masukkan URL YouTube: ")

    # Folder tujuan (akan otomatis tersimpan di folder 'Music' kamu)
    output_dir = os.path.expanduser("~/Music")

    ydl_opts = {
        'format': 'bestaudio/best',  # Ambil kualitas audio terbaik
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',   # Format tujuan
            'preferredquality': '192', # Kualitas (192kbps)
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s', # Penamaan file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Sedang memproses... Tunggu bentar ya.")
            ydl.download([url])
            print(f"\nSelesai! File disimpan di folder: {output_dir}")
    except Exception as e:
        print(f"Aduh, error nih: {e}")

if __name__ == "__main__":
    download_yt_as_mp3()
