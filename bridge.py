"""
AI Gesture Studio - Windows Audio Bridge
Connects the Gesture Studio web app to Windows System Master Audio using Pycaw.
"""

import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import ctypes

try:
    from pycaw.pycaw import AudioUtilities
except ImportError:
    print("Pycaw not found. Installing pycaw...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pycaw", "comtypes"])
    from pycaw.pycaw import AudioUtilities

# Initialize Windows Master Audio Device
device = AudioUtilities.GetSpeakers()
volume_control = device.EndpointVolume

PORT = 5005
BASE_DIR = Path(__file__).resolve().parent

class VolumeBridgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # API Endpoints
        if parsed.path == '/api/volume':
            try:
                level = float(params.get('level', [50])[0])
                scalar = max(0.0, min(1.0, level / 100.0))
                volume_control.SetMasterVolumeLevelScalar(scalar, None)
                self._send_json({"status": "ok", "volume": level})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, 500)
            return

        elif parsed.path == '/api/mute':
            try:
                current_mute = volume_control.GetMute()
                new_mute = 0 if current_mute else 1
                volume_control.SetMute(new_mute, None)
                self._send_json({"status": "ok", "muted": bool(new_mute)})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, 500)
            return

        elif parsed.path == '/api/playpause':
            try:
                VK_MEDIA_PLAY_PAUSE = 0xB3
                KEYEVENTF_KEYUP = 0x0002
                user32 = ctypes.windll.user32
                user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
                user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYUP, 0)
                self._send_json({"status": "ok", "action": "play_pause"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, 500)
            return

        elif parsed.path == '/api/status':
            try:
                current_vol = round(volume_control.GetMasterVolumeLevelScalar() * 100)
                is_muted = bool(volume_control.GetMute())
                self._send_json({"status": "ok", "volume": current_vol, "muted": is_muted, "device": device.FriendlyName})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, 500)
            return

        # Serve static files (index.html, models, etc.)
        super().do_GET()

    def _send_json(self, data, code=200):
        import json
        payload = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        pass  # Suppress console clutter for ultra-fast performance

def main():
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, VolumeBridgeHandler)
    url = f"http://127.0.0.1:{PORT}/index.html"
    print("=" * 60)
    print("  AI GESTURE STUDIO - WINDOWS AUDIO BRIDGE")
    print(f"  Connected Audio Device: {device.FriendlyName}")
    print(f"  Live Server: {url}")
    print("  Use Hand Gestures to control your Laptop's Master Volume!")
    print("  Press Ctrl+C in this terminal to stop.")
    print("=" * 60)

    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping audio bridge...")
        httpd.server_close()

if __name__ == "__main__":
    main()
