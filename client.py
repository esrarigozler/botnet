import requests
import time
import platform
import json

C2_URL = "http://localhost:5000"
CLIENT_ID = f"client_{platform.node()}"

def register():
    try:
        response = requests.post(f"{C2_URL}/register",
                                 json={"id": CLIENT_ID}, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_command():
    try:
        response = requests.get(f"{C2_URL}/get_command",
                                params={"id": CLIENT_ID}, timeout=5)
        return response.json().get("command")
    except:
        return None

def execute_command(command):
    if command == "system_info":
        info = {
            "os": platform.system(),      # DÜZELTİLDİ: parantez eklendi
            "release": platform.release(), # DÜZELTİLDİ
            "version": platform.version(), # DÜZELTİLDİ
            "machine": platform.machine(), # DÜZELTİLDİ
            "processor": platform.processor() # DÜZELTİLDİ
        }
        print(f"Sistem Bilgisi: {json.dumps(info, indent=2)}")
    elif command == "ping":
        print("Pong! İstemci aktif.")
    else:
        print(f"Bilinmeyen komut: {command}")

def main():
    print(f"İstemci başlatılıyor: {CLIENT_ID}")

    if not register():
        print("Sunucuya bağlanılamadı!")
        return
    print("Kayıt başarılı. Komutlar bekleniyor...")

    while True:
        command = get_command()
        if command:
            print(f"Komut alındı: {command}")
            execute_command(command)
        time.sleep(5)

if __name__ == "__main__":
    main()
