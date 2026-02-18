import pytest
import requests
from freakycat import GIF_URL

def test_gif_url_is_valid():
    # Memastikan URL yang kamu pakai itu string dan tipenya beneran URL
    assert GIF_URL.startswith("https://")
    assert "giphy.com" in GIF_URL

def test_network_request():
    # Mengetes apakah server Giphy merespon dengan baik (Status 200)
    # Kita pakai timeout biar test-nya gak macet kalau internet lemot
    try:
        response = requests.head(GIF_URL, timeout=5)
        assert response.status_code == 200
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Koneksi ke Giphy gagal: {e}")

def test_image_libraries():
    # Memastikan library Pillow sudah terinstall dengan benar
    try:
        from PIL import Image
        assert True
    except ImportError:
        assert False, "Library Pillow (PIL) tidak ditemukan"
