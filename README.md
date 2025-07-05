# 📧 Email Scraper (Python)  
Tarayıcı gibi davranan, domain dışına çıkmayan, sade ama etkili bir e-posta bulucu.

Bu script, belirttiğiniz bir web sitesinde gezerek sayfalardaki geçerli e-posta adreslerini toplar. Sadece aynı domain altındaki bağlantılara tırmanır, her sayfayı bir kez ziyaret eder ve isteğe bağlı olarak verileri dosyaya kaydeder. Tarayıcı gibi görünmek için User-Agent desteği içerir.

---

## ✨ Özellikler

- 🔍 E-posta adreslerini HTML içinden tespit eder (regex)
- 🌍 Sadece aynı domain altında tarama yapar (dış linkleri filtreler)
- 🧭 Genişlik öncelikli bağlantı taraması (deque ile BFS)
- 🧠 Gereksiz tekrarları engeller (visited URL takibi)
- 🛡️ User-Agent desteği ile engellemeleri aşar (tarayıcı gibi görünür)
- 💾 Sonuçları `emails.txt` olarak kaydetme seçeneği

---

## 🧠 Nasıl Çalışır?

1. Sizden bir başlangıç URL’si ister.  
2. Bu sayfaya GET isteği gönderir (`requests`).
3. HTML içeriği `BeautifulSoup` ile parse edilir.
4. E-posta adresleri regex ile aranır.
5. Sayfadaki `<a href="...">` bağlantıları bulunur.
6. Sadece aynı domain içindeki sayfalar `deque` kuyruğuna eklenir.
7. Kuyruktaki her URL teker teker gezilir (maks. 100 sayfa).
8. Bulunan tüm e-posta adresleri terminale yazılır, isterseniz `.txt` olarak da kaydedilir.

---

## ⚙️ Kullanılan Teknolojiler

| Kütüphane      | Ne işe yarıyor?                               |
|----------------|------------------------------------------------|
| `requests`     | Sayfaya HTTP isteği gönderir                   |
| `bs4` (BeautifulSoup) | HTML içeriğini parçalar, bağlantıları bulur  |
| `re`           | E-posta desenini bulmak için regex kullanılır |
| `urllib.parse` | URL birleştirme ve domain kontrolü yapar       |
| `collections.deque` | Bağlantıları sırayla gezmek için kullanılır (FIFO) |

---

## 🛡️ User-Agent Nedir, Neden Kullanılır?

Bazı web siteleri Python gibi botlardan gelen istekleri engelleyebilir. Bunu anlamak için HTTP isteği içinde gönderilen `User-Agent` bilgisine bakarlar.

Bu scraper, User-Agent header’ı ekleyerek kendini bir tarayıcı gibi tanıtır:

```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36
```

## 🚀 Kullanım

### 1. Projeyi GitHub üzerinden klonlayın
```
git clone https://github.com/kullanici/email-scraper.git
```

### 2. Proje klasörüne geçin
```
cd email-scraper
```

### 3. Gerekli Python kütüphanelerini yükleyin
```
pip install requests beautifulsoup4 lxml
```

### 4. Script'i çalıştırın
```
python3 email_scraper.py
```


