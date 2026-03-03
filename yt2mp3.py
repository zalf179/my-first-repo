from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Lokasi download (Folder Music user)
DOWNLOAD_DIR = os.path.expanduser("~/Music")

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- TEMPLATE HTML ---
HTML_GUI = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 Downloader</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #1e1e1e; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 100%; max-width: 450px; text-align: center; }
        h2 { color: #ff0000; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: none; border-radius: 6px; background: #333; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; border: none; border-radius: 6px; background: #ff0000; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #cc0000; }
        button:disabled { background: #555; cursor: not-allowed; }
        #status { margin-top: 20px; padding: 10px; border-radius: 6px; font-size: 0.9em; min-height: 20px; }
        .success { background: #1b5e20; color: #c8e6c9; }
        .error { background: #b71c1c; color: #ffcdd2; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎵 YT to MP3</h2>
        <p>Masukkan URL Video YouTube untuk dikonversi</p>
        <input type="text" id="videoUrl" placeholder="https://youtube.com/watch?v=...">
        <button id="downloadBtn" onclick="startDownload()">Convert ke MP3</button>
        <div id="status"></div>
    </div>

    <script>
        async function startDownload() {
            const urlInput = document.getElementById('videoUrl');
            const btn = document.getElementById('downloadBtn');
            const statusDiv = document.getElementById('status');
            
            if (!urlInput.value) {
                alert("Paste dulu URL-nya!");
                return;
            }

            // UI State: Loading
            btn.disabled = true;
            statusDiv.className = '';
            statusDiv.innerText = "⏳ Sedang diproses... Cek terminal Python buat liat progress.";

            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlInput.value })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    statusDiv.className = 'success';
                    statusDiv.innerText = "✅ " + result.message;
                    urlInput.value = '';
                } else {
                    throw new Error(result.message);
                }
            } catch (err) {
                statusDiv.className = 'error';
                statusDiv.innerText = "❌ Gagal: " + err.message;
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

# --- ROUTES ---

@app.route('/')
def home():
    # Menampilkan HTML saat buka http://127.0.0.1:5000/
    return render_template_string(HTML_GUI)

@app.route('/download', methods=['POST'])
def handle_download():
    data = request.get_json()
    url = data.get('url')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"status": "success", "message": "MP3 berhasil disimpan di folder Music!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
