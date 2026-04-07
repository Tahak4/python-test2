import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CanliSkorBotu:
    def __init__(self):
        chrome_options = Options()
        # Görünür modda çalıştıralım ki hata varsa görelim
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Gerçek kullanıcı simülasyonu
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.veriler = []

    def veri_cek(self):
        # Flashscore veya benzeri bir alternatif site (Örn: Livescore.com)
        url = "https://www.flashscore.com.tr/" 
        print(f"[*] Siteye gidiliyor: {url}")
        
        try:
            self.driver.get(url)
            
            # Sayfanın ve maçların yüklenmesi için bekleme (Önemli!)
            print("[*] Maçların yüklenmesi bekleniyor (15 saniye)...")
            time.sleep(15)

            # Flashscore'da maçlar genellikle 'event__match' class'ı içinde olur
            # Eğer class ismi farklıysa genel bir tarama yapıyoruz
            maclar = self.driver.find_elements(By.CSS_SELECTOR, ".event__match")

            if len(maclar) == 0:
                print("[!] Standart metodla maç bulunamadı. Alternatif tarama yapılıyor...")
                # Daha genel bir seçici kullanıyoruz
                maclar = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'g_1_')]")

            print(f"[+] Toplam {len(maclar)} maç bulundu. Veriler ayıklanıyor...")

            for mac in maclar:
                try:
                    # Metni parçalara ayırarak veriyi çekme (En güvenli yol)
                    satir_metni = mac.text.replace("\n", " ")
                    parcalar = satir_metni.split()
                    
                    # Örnek format: "19:00 Fenerbahçe 2 - 1 İstanbulspor Bitti"
                    self.veriler.append({
                        "detay": satir_metni
                    })
                except:
                    continue

        except Exception as e:
            print(f"[!] Hata: {e}")

    def json_kaydet(self):
        if self.veriler:
            with open("canli_skorlar.json", "w", encoding="utf-8") as f:
                json.dump(self.veriler, f, ensure_ascii=False, indent=4)
            print(f"[OK] {len(self.veriler)} maç 'canli_skorlar.json' dosyasına kaydedildi.")
        else:
            print("[!] Kaydedilecek veri bulunamadı (Liste boş).")

    def kapat(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = CanliSkorBotu()
    bot.veri_cek()
    bot.json_kaydet()
    bot.kapat()