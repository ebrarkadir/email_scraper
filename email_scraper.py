from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re

user_url = input('[+] Enter Target URL To Scan: ').strip()

domain = urllib.parse.urlsplit(user_url).netloc

urls = deque([user_url])
scraped_urls = set()
emails = set()

max_visits = 100
count = 0

try:
    while urls and count < max_visits:
        url = urls.popleft()
        scraped_urls.add(url)
        count += 1

        print(f'[{count}] Scanning: {url}')

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            print(f'[!] Request failed: {e}')
            continue

        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
            response.text, re.I
        ))
        if new_emails:
            print(f'[+] Found {len(new_emails)} new email(s).')
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, "lxml")
        for anchor in soup.find_all("a"):
            href = anchor.get("href")
            if not href:
                continue

            href = urllib.parse.urljoin(url, href)
            href_parsed = urllib.parse.urlsplit(href)

            if href_parsed.netloc and domain not in href_parsed.netloc:
                continue

            if href not in scraped_urls and href not in urls:
                urls.append(href)

except KeyboardInterrupt:
    print('\n[-] Interrupted by user!')

print('\n[✓] Email addresses found:')
for email in sorted(emails):
    print(email)

save = input('\n[?] Save results to "emails.txt"? (y/n): ').lower()
if save == 'y':
    with open('emails.txt', 'w') as f:
        for email in sorted(emails):
            f.write(email + '\n')
    print('[✓] Emails saved to emails.txt')
