import requests
from datetime import datetime

class FutbolVeriMerkezi:
    def __init__(self, api_key):
        self.url = "https://v3.football.api-sports.io/fixtures"
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

    def bugunun_maclarini_getir(self):
        # Bugünün tarihini alıyoruz (YYYY-MM-DD formatında)
        bugun = datetime.now().strftime('%Y-%m-%d')
        
        parametreler = {
            'date': bugun,
            'timezone': 'Europe/Istanbul' # Saatleri Türkiye'ye göre ayarla
        }

        try:
            print(f"[*] {bugun} tarihli maçlar çekiliyor...")
            response = requests.get(self.url, headers=self.headers, params=parametreler)
            veri = response.json()

            if not veri['response']:
                print("[-] Hiç maç bulunamadı.")
                return []

            sonuclar = []
            for mac in veri['response']:
                detay = {
                    "lig": mac['league']['name'],
                    "ulke": mac['league']['country'],
                    "saat": mac['fixture']['date'].split('T')[1][:5],
                    "ev_sahibi": mac['teams']['home']['name'],
                    "deplasman": mac['teams']['away']['name'],
                    "durum": mac['fixture']['status']['long']
                }
                sonuclar.append(detay)
            
            return sonuclar

        except Exception as e:
            print(f"Hata oluştu: {e}")
            return []

# --- KULLANIM ---
if __name__ == "__main__":
    # BURAYA KENDİ API ANAHTARINI YAPIŞTIR
    MY_API_KEY = "BURAYA_API_KEY_GELECEK" 
    
    bot = FutbolVeriMerkezi(MY_API_KEY)
    mac_listesi = bot.bugunun_maclarini_getir()

    print(f"\n{'-'*50}")
    for m in mac_listesi:
        # Sadece önemli ligleri filtrelemek istersen buraya 'if' koyabilirsin
        # Örneğin: if m['lig'] == "Süper Lig":
        print(f"[{m['saat']}] {m['lig']} ({m['ulke']}): {m['ev_sahibi']} vs {m['deplasman']} | Durum: {m['durum']}")