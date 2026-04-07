from bot import WebScraper
from ayarlar import HEDEF_SITELER
import time

def baslat():
    scraper = WebScraper()
    
    print("=== Veri Çekme İşlemi Başlıyor ===\n")
    
    for site in HEDEF_SITELER:
        sonuc = scraper.veri_getir(site)
        scraper.tum_veriler.append(sonuc)
        
        # Sitelere nazik davranalım, banlanmayalım
        time.sleep(2) 
    
    scraper.kaydet()
    print("\n=== İşlem Tamamlandı ===")

if __name__ == "__main__":
    baslat()