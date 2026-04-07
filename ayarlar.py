# Her site için ayrı bir ayıklama mantığı kuruyoruz
def haber_sitesi_a(soup):
    # Örnek: Manşet başlıklarını liste olarak çek
    return [h.text.strip() for h in soup.select("h2.manset-baslik")]

def fiyat_sitesi_b(soup):
    # Örnek: Ürün adını ve fiyatını çek
    isim = soup.find("h1", id="product-name").text.strip()
    fiyat = soup.find("span", class_="price").text.strip()
    return {"urun": isim, "fiyat": fiyat}

# ... 10 siteye kadar böyle fonksiyonlar ekleyebilirsin ...

HEDEF_SITELER = [
    {"isim": "HaberTürk", "url": "https://www.haberturk.com", "parser": haber_sitesi_a},
    {"isim": "E-Ticaret-X", "url": "https://site-b.com/urun/1", "parser": fiyat_sitesi_b},
    # Buraya 10 tane eklediğini varsayıyoruz
]