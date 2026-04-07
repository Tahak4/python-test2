import requests
from datetime import datetime

# Senin API Anahtarın
MY_API_KEY = "86b943b453120bc6bb1c77a189f09fe8" 

class FutbolBotu:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

    def baglanti_test_et(self):
        """API kotasını ve bağlantı durumunu kontrol eder."""
        try:
            response = requests.get(f"{self.base_url}/status", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                kalan = data['response']['requests']['remaining']
                isim = data['response']['account']['firstname']
                print(f"[+] Bağlantı Başarılı! Merhaba {isim}. Kalan Hakkın: {kalan}")
                return True
            return False
        except:
            return False

    def bugunun_maclarini_getir(self):
        """Bugünün tüm maçlarını çeker ve listeler."""
        bugun = datetime.now().strftime('%Y-%m-%d')
        endpoint = f"{self.base_url}/fixtures"
        params = {'date': bugun, 'timezone': 'Europe/Istanbul'}

        print(f"[*] {bugun} tarihli maçlar hazırlanıyor...\n")
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            maclar = response.json().get('response', [])

            if not maclar:
                print("[!] Bugün için maç bulunamadı.")
                return

            print(f"{'SAAT':<7} | {'LİG':<20} | {'MAÇ':<40} | {'DURUM'}")
            print("-" * 85)

            for mac in maclar:
                saat = mac['fixture']['date'].split('T')[1][:5]
                lig = mac['league']['name']
                ev = mac['teams']['home']['name']
                dep = mac['teams']['away']['name']
                durum = mac['fixture']['status']['short'] # FT: Bitti, NS: Başlamadı, 1H: İlk Yarı

                # Sadece önemli ligleri görmek istersen buraya filtre ekleyebiliriz
                print(f"{saat:<7} | {lig[:20]:<20} | {ev:>18} vs {dep:<18} | {durum}")

        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

if __name__ == "__main__":
    bot = FutbolBotu(MY_API_KEY)
    
    # Önce testi yap, sonra maçları çek
    if bot.baglanti_test_et():
        print("-" * 30)
        bot.bugunun_maclarini_getir()
    else:
        print("[!] API anahtarın hatalı veya kotan dolmuş olabilir.")