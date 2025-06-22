from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re

# Kullanıcıdan hedef URL alınır
user_url = input('[+] Enter Target URL To Scan: ').strip()
domain = urllib.parse.urlsplit(user_url).netloc

# Tarama için gerekli yapılar
urls = deque([user_url])
scraped_urls = set()
emails = set()

# User-Agent header (tarayıcı gibi görünmek için)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Maksimum ziyaret edilecek sayfa sayısı
max_visits = 100
count = 0

try:
    while urls and count < max_visits:
        url = urls.popleft()
        scraped_urls.add(url)
        count += 1

        print(f'[{count}] Scanning: {url}')

        try:
            # Artık headers ile gönderiliyor
            response = requests.get(url, headers=headers)
        except requests.RequestException as e:
            print(f'[!] Request failed: {e}')
            continue

        # E-posta adreslerini ayıkla
        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
            response.text, re.I
        ))
        if new_emails:
            print(f'[+] Found {len(new_emails)} new email(s).')
        emails.update(new_emails)

        # Sayfadaki bağlantıları sıraya ekle
        soup = BeautifulSoup(response.text, "lxml")
        for anchor in soup.find_all("a"):
            href = anchor.get("href")
            if not href:
                continue

            # Göreli bağlantıları tam bağlantıya dönüştür
            href = urllib.parse.urljoin(url, href)
            href_parsed = urllib.parse.urlsplit(href)

            # Domain dışı sayfalara geçme
            if href_parsed.netloc and domain not in href_parsed.netloc:
                continue

            if href not in scraped_urls and href not in urls:
                urls.append(href)

except KeyboardInterrupt:
    print('\n[-] Interrupted by user!')

# Bulunan e-posta adreslerini yazdır
print('\n[✓] Email addresses found:')
for email in sorted(emails):
    print(email)

# Kayıt sorusu
save = input('\n[?] Save results to "emails.txt"? (y/n): ').lower()
if save == 'y':
    with open('emails.txt', 'w') as f:
        for email in sorted(emails):
            f.write(email + '\n')
    print('[✓] Emails saved to emails.txt')
