import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class MacBotuJSON:
    def __init__(self):
        chrome_options = Options()
        # DİKKAT: Hata çözülene kadar headless modu kapattım, tarayıcıyı izle!
        # chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.tum_veriler = {}

    def veri_cek(self, site_adi, url):
        print(f"[*] {site_adi} taranıyor: {url}")
        self.tum_veriler[site_adi] = []
        
        try:
            self.driver.get(url)
            
            # Sayfanın yüklenmesi için biraz esnek bir bekleme (Maçkolik ağır yüklenebilir)
            wait = WebDriverWait(self.driver, 20)
            
            # Maç satırlarının yüklenmesini bekle (Yeni tasarımda kapsayıcı div'ler değişebiliyor)
            # Genellikle canlı sonuçlarda 'match-row' veya 'widget-live-score' içinde bulunur.
            time.sleep(10) # Garanti olması için 10 saniye tam bekleme

            # Maç satırlarını bulmaya çalış (Farklı class isimlerini deniyoruz)
            maclar = self.driver.find_elements(By.CSS_SELECTOR, "[class*='match-row'], [class*='match-item']")
            
            if not maclar:
                # Eğer hala bulamadıysa sayfayı biraz aşağı kaydır (Lazy loading tetiklensin)
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(3)
                maclar = self.driver.find_elements(By.CSS_SELECTOR, "[class*='match-row'], [class*='match-item']")

            for mac in maclar:
                try:
                    # Daha esnek seçimler (Class contains mantığı)
                    saat = mac.find_element(By.CSS_SELECTOR, "[class*='time']").text.strip()
                    ev = mac.find_element(By.CSS_SELECTOR, "[class*='home-team']").text.strip()
                    dep = mac.find_element(By.CSS_SELECTOR, "[class*='away-team']").text.strip()
                    skor = mac.find_element(By.CSS_SELECTOR, "[class*='score']").text.strip()

                    if ev and dep:
                        self.tum_veriler[site_adi].append({
                            "saat": saat,
                            "ev_sahibi": ev,
                            "deplasman": dep,
                            "skor": skor
                        })
                except:
                    continue
            
            print(f"[+] {site_adi} bitti. Çekilen maç: {len(self.tum_veriler[site_adi])}")

        except Exception as e:
            print(f"[!] {site_adi} hatası: {str(e)[:100]}...")

    def json_kaydet(self, dosya_adi="mac_sonuclari.json"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(self.tum_veriler, f, ensure_ascii=False, indent=4)
        print(f"\n[OK] Dosya kaydedildi: {dosya_adi}")

    def kapat(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = MacBotuJSON()
    # Maçkolik ve Sahadan yapıları aynıdır, sadece birini denemek bile yeterli başlangıçta
    siteler = [
        {"isim": "MACKOLIK", "url": "https://www.mackolik.com/canli-sonuclar"}
    ]

    for site in siteler:
        bot.veri_cek(site['isim'], site['url'])
    
    bot.json_kaydet()
    bot.kapat()