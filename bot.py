import requests
from bs4 import BeautifulSoup
import time
import json

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.tum_veriler = []

    def veri_getir(self, site_bilgisi):
        url = site_bilgisi['url']
        isim = site_bilgisi['isim']
        parser_fonksiyonu = site_bilgisi['parser']

        print(f"[*] {isim} taranıyor: {url}")
        
        try:
            # 10 saniye içinde cevap gelmezse pes et (timeout)
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status() # 404 veya 500 hatası varsa durdurur
            
            soup = BeautifulSoup(response.text, 'html.parser')
            veri = parser_fonksiyonu(soup)
            
            return {"site": isim, "durum": "Başarılı", "veri": veri}
            
        except Exception as e:
            return {"site": isim, "durum": "Hata", "mesaj": str(e)}

    def kaydet(self, dosya_adi="sonuclar.json"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(self.tum_veriler, f, ensure_ascii=False, indent=4)
        print(f"\n[+] Tüm veriler '{dosya_adi}' dosyasına kaydedildi.")