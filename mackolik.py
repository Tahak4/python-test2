from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def mackolik_canli_cek():
    # 1. Tarayıcı Ayarları
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Tarayıcıyı açmadan arka planda çalıştır
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Gerçek bir kullanıcı gibi görünmek için User-Agent ekliyoruz
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. Driver'ı Başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("[*] Maçkolik Canlı Sonuçlar sayfası açılıyor...")
        driver.get("https://www.mackolik.com/canli-sonuclar")
        
        # Sayfanın ve maçların yüklenmesi için 5 saniye bekle
        time.sleep(5) 

        # 3. Maç Satırlarını Bul
        # Maçkolik'te her maç genelde 'match-row' class'ı ile başlar
        mac_satirlari = driver.find_elements(By.CLASS_NAME, "match-row")

        print(f"[+] Toplam {len(mac_satirlari)} maç bulundu.\n")

        for mac in mac_satirlari:
            try:
                # Bilgileri ayıklıyoruz (Class isimleri değişmişse 'inspect' ile bakmalıyız)
                saat = mac.find_element(By.CLASS_NAME, "time").text
                ev_sahibi = mac.find_element(By.CLASS_NAME, "home-team").text
                deplasman = mac.find_element(By.CLASS_NAME, "away-team").text
                skor = mac.find_element(By.CLASS_NAME, "score").text

                print(f"[{saat}] {ev_sahibi} {skor} {deplasman}")
            except:
                # Bazı satırlar reklam veya başlık olabilir, onları atla
                continue

    except Exception as e:
        print(f"[!] Hata: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    mackolik_canli_cek()